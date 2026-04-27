from __future__ import annotations

import asyncio
import hashlib
import json
import os
import random
import re
import sys
from urllib.parse import urljoin

from apify import Actor, Request
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")


CF_TITLES = {
    "just a moment",
    "attention required!",
    "please wait...",
    "checking your browser",
    "one more step",
    "security check",
    "access denied",
}

VIEWPORTS = [
    {"width": 1280, "height": 720, "device_scale_factor": 1},
    {"width": 1366, "height": 768, "device_scale_factor": 1},
    {"width": 1440, "height": 900, "device_scale_factor": 1},
    {"width": 1536, "height": 864, "device_scale_factor": 1},
    {"width": 1920, "height": 1080, "device_scale_factor": 1},
]

FINGERPRINTS = [
    {
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "platform": "Win32",
        "timezone_id": "America/New_York",
        "locale": "en-US",
        "languages": ["en-US", "en"],
        "webgl_vendor": "Google Inc. (Intel)",
        "webgl_renderer": "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "hardware_concurrency": 8,
        "device_memory": 8,
    },
    {
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        ),
        "platform": "Win32",
        "timezone_id": "America/Chicago",
        "locale": "en-US",
        "languages": ["en-US", "en"],
        "webgl_vendor": "Google Inc. (NVIDIA)",
        "webgl_renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "hardware_concurrency": 12,
        "device_memory": 8,
    },
    {
        "user_agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "platform": "MacIntel",
        "timezone_id": "America/Los_Angeles",
        "locale": "en-US",
        "languages": ["en-US", "en"],
        "webgl_vendor": "Google Inc. (Apple)",
        "webgl_renderer": "ANGLE (Apple, Apple M1 Pro, OpenGL 4.1)",
        "hardware_concurrency": 10,
        "device_memory": 8,
    },
]


async def human_delay(min_s=1.0, max_s=2.5):
    await asyncio.sleep(random.uniform(min_s, max_s))


async def human_mouse_wander(page, fingerprint):
    viewport = fingerprint["viewport"]
    try:
        for _ in range(random.randint(3, 6)):
            if page.is_closed():
                return
            await page.mouse.move(
                random.randint(40, max(80, viewport["width"] - 80)),
                random.randint(60, max(100, viewport["height"] - 80)),
                steps=random.randint(10, 25),
            )
            await asyncio.sleep(random.uniform(0.08, 0.25))
    except Exception as e:
        Actor.log.debug(f"Human mouse movement skipped: {e}")


async def random_scroll(page):
    try:
        for i in range(random.randint(3, 6)):
            if page.is_closed():
                return
            distance = random.randint(220, 680)
            if i and random.random() < 0.2:
                distance = -random.randint(80, 220)
            await page.mouse.wheel(0, distance)
            await asyncio.sleep(random.uniform(0.45, 1.25))
    except Exception as e:
        Actor.log.debug(f"Human scroll skipped: {e}")


async def human_settle(page, fingerprint, min_s=0.8, max_s=1.8):
    await human_delay(min_s, max_s)
    if random.random() < 0.85:
        await human_mouse_wander(page, fingerprint)
    if random.random() < 0.65:
        await random_scroll(page)


async def soft_refresh_challenge(page, fingerprint):
    try:
        if page.is_closed():
            return
        await human_mouse_wander(page, fingerprint)
        if random.random() < 0.4:
            await page.mouse.wheel(0, random.randint(80, 180))
        await human_delay(1.5, 3.5)
    except Exception as e:
        Actor.log.debug(f"Challenge interaction skipped: {e}")


async def safe_close_page(page):
    try:
        if not page.is_closed():
            await page.close()
    except Exception:
        pass


async def wait_for_cloudflare(page, timeout_s=180, *, allow_manual=True) -> bool:
    deadline = asyncio.get_event_loop().time() + timeout_s
    manual_notice_shown = False

    while asyncio.get_event_loop().time() < deadline:
        try:
            title = (await page.title()).lower().strip()
        except Exception:
            title = ""

        Actor.log.info(f"[CF] title='{title}'")

        try:
            challenge_count = await page.locator(
                "iframe[src*='challenges.cloudflare.com'],"
                "iframe[src*='hcaptcha.com'],"
                "div#challenge-form,"
                "div#cf-challenge-running"
            ).count()
        except Exception as e:
            Actor.log.warning(f"[CF] Browser/page closed while checking challenge: {e}")
            return False

        if challenge_count:
            if not allow_manual:
                Actor.log.warning("[CF] Checkbox/challenge found. Run headed to verify manually.")
                return False
            if not manual_notice_shown:
                Actor.log.warning("[CF] Click the checkbox in the opened browser; the actor will continue.")
                manual_notice_shown = True
            await asyncio.sleep(2)
            continue

        if not any(keyword in title for keyword in CF_TITLES):
            Actor.log.info("[CF] Challenge cleared")
            return True

        await soft_refresh_challenge(page, getattr(page, "_fingerprint", build_fingerprint("fallback")))

    Actor.log.warning("[CF] Timed out waiting for challenge to clear.")
    return False


def is_apify_cloud() -> bool:
    return os.getenv("APIFY_IS_AT_HOME") == "1"


def proxy_to_playwright(proxy_info):
    if not proxy_info:
        return None
    return {
        "server": proxy_info.url,
        "username": proxy_info.username,
        "password": proxy_info.password,
    }


def build_fingerprint(seed: str) -> dict:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    base = dict(FINGERPRINTS[int(digest[:2], 16) % len(FINGERPRINTS)])
    viewport = dict(VIEWPORTS[int(digest[2:4], 16) % len(VIEWPORTS)])
    base["viewport"] = viewport
    base["screen"] = {
        "width": viewport["width"],
        "height": viewport["height"],
    }
    base["device_scale_factor"] = viewport["device_scale_factor"]
    return base


def sanitize_proxy_session_id(value: str, *, max_length: int = 50) -> str:
    cleaned = re.sub(r"[^\w._~]+", "_", value.strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("._")
    if not cleaned:
        cleaned = "capterra_session"
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:8]
    prefix_max_length = max(1, max_length - len(digest) - 1)
    return f"{cleaned[:prefix_max_length].rstrip('._')}_{digest}"


async def new_proxy_info_safe(proxy_configuration, session_id: str):
    if not proxy_configuration:
        return None
    safe_session_id = sanitize_proxy_session_id(session_id)
    Actor.log.info(f"Using proxy session_id='{safe_session_id}'")
    return await proxy_configuration.new_proxy_info(session_id=safe_session_id)


async def align_user_agent_with_browser(browser, fingerprint: dict) -> dict:
    try:
        browser_version = browser.version.split("/", 1)[-1]
        chrome_major = browser_version.split(".", 1)[0]
        if chrome_major.isdigit():
            fingerprint = dict(fingerprint)
            os_part = (
                "Macintosh; Intel Mac OS X 10_15_7"
                if fingerprint["platform"] == "MacIntel"
                else "Windows NT 10.0; Win64; x64"
            )
            fingerprint["user_agent"] = (
                f"Mozilla/5.0 ({os_part}) AppleWebKit/537.36 "
                f"(KHTML, like Gecko) Chrome/{chrome_major}.0.0.0 Safari/537.36"
            )
    except Exception as e:
        Actor.log.warning(f"Could not align user agent with browser version: {e}")
    return fingerprint


async def launch_browser(playwright, *, headless: bool, proxy_info=None, fingerprint=None):
    fingerprint = fingerprint or build_fingerprint("fallback")
    viewport = fingerprint["viewport"]
    args = [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled",
        f"--window-size={viewport['width']},{viewport['height']}",
        "--lang=en-US,en",
    ]

    launch_options = {
        "headless": headless,
        "args": args,
    }
    proxy = proxy_to_playwright(proxy_info)
    if proxy:
        launch_options["proxy"] = proxy

    if os.name == "nt" and not headless:
        try:
            Actor.log.info(f"Launching installed Google Chrome headless={headless}")
            return await playwright.chromium.launch(channel="chrome", **launch_options)
        except Exception as e:
            Actor.log.warning(f"Chrome channel failed, using bundled Chromium: {e}")

    Actor.log.info(f"Launching bundled Chromium headless={headless}")
    return await playwright.chromium.launch(**launch_options)


def stealth_init_script(fingerprint: dict) -> str:
    return f"""
(() => {{
  const fingerprint = {json.dumps(fingerprint)};
  const defineGetter = (obj, prop, value) => {{
    try {{ Object.defineProperty(obj, prop, {{ get: () => value, configurable: true }}); }} catch (e) {{}}
  }};

  defineGetter(Navigator.prototype, 'webdriver', undefined);
  defineGetter(Navigator.prototype, 'platform', fingerprint.platform);
  defineGetter(Navigator.prototype, 'languages', fingerprint.languages);
  defineGetter(Navigator.prototype, 'hardwareConcurrency', fingerprint.hardware_concurrency);
  defineGetter(Navigator.prototype, 'deviceMemory', fingerprint.device_memory);
  defineGetter(Navigator.prototype, 'plugins', [1, 2, 3, 4, 5]);
  defineGetter(Navigator.prototype, 'mimeTypes', [1, 2, 3]);

  window.chrome = window.chrome || {{}};
  window.chrome.runtime = window.chrome.runtime || {{}};
  window.chrome.app = window.chrome.app || {{}};

  const originalQuery = window.navigator.permissions && window.navigator.permissions.query;
  if (originalQuery) {{
    window.navigator.permissions.query = (parameters) => (
      parameters && parameters.name === 'notifications'
        ? Promise.resolve({{ state: Notification.permission }})
        : originalQuery.call(window.navigator.permissions, parameters)
    );
  }}

  const getParameter = WebGLRenderingContext.prototype.getParameter;
  WebGLRenderingContext.prototype.getParameter = function(parameter) {{
    if (parameter === 37445) return fingerprint.webgl_vendor;
    if (parameter === 37446) return fingerprint.webgl_renderer;
    return getParameter.call(this, parameter);
  }};
  if (window.WebGL2RenderingContext) {{
    const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
    WebGL2RenderingContext.prototype.getParameter = function(parameter) {{
      if (parameter === 37445) return fingerprint.webgl_vendor;
      if (parameter === 37446) return fingerprint.webgl_renderer;
      return getParameter2.call(this, parameter);
    }};
  }}

  defineGetter(screen, 'width', fingerprint.screen.width);
  defineGetter(screen, 'height', fingerprint.screen.height);
  defineGetter(screen, 'availWidth', fingerprint.screen.width);
  defineGetter(screen, 'availHeight', fingerprint.screen.height - 40);
}})();
"""


async def make_context(browser, *, fingerprint, cookies=None, storage_state=None):
    viewport = fingerprint["viewport"]
    context_options = {
        "viewport": {"width": viewport["width"], "height": viewport["height"]},
        "screen": fingerprint["screen"],
        "device_scale_factor": fingerprint["device_scale_factor"],
        "user_agent": fingerprint["user_agent"],
        "locale": fingerprint["locale"],
        "timezone_id": fingerprint["timezone_id"],
        "color_scheme": "light",
        "java_script_enabled": True,
        "accept_downloads": False,
        "extra_http_headers": {
            "Accept-Language": ",".join(fingerprint["languages"]) + ";q=0.9",
        },
    }
    if storage_state:
        context_options["storage_state"] = storage_state

    context = await browser.new_context(**context_options)
    await context.add_init_script(stealth_init_script(fingerprint))
    if cookies:
        await context.add_cookies(cookies)
    return context


async def goto_verified(
    page,
    url: str,
    *,
    allow_manual: bool,
    fingerprint: dict,
    cf_wait_seconds: int,
) -> bool:
    page._fingerprint = fingerprint
    await human_delay(0.3, 1.2)
    response = await page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    Actor.log.info(f"HTTP {response.status if response else '?'} {url}")
    await human_settle(page, fingerprint, 0.6, 1.6)
    return await wait_for_cloudflare(
        page,
        timeout_s=cf_wait_seconds,
        allow_manual=allow_manual,
    )


def parse_cookies(raw_cookies):
    if not raw_cookies:
        return []
    if isinstance(raw_cookies, list):
        return raw_cookies
    try:
        parsed = json.loads(raw_cookies)
    except json.JSONDecodeError:
        Actor.log.warning("cloudflare_cookies was not valid JSON, ignoring it.")
        return []
    return parsed if isinstance(parsed, list) else []


async def optional_inner_text(locator, default="") -> str:
    try:
        if await locator.count() == 0:
            return default
        return " ".join((await locator.first.inner_text()).split())
    except Exception:
        return default


async def optional_raw_inner_text(locator, default="") -> str:
    try:
        if await locator.count() == 0:
            return default
        return (await locator.first.inner_text()).strip()
    except Exception:
        return default


async def scrape_product_card(card, start_url: str) -> dict | None:
    try:
        product_name = await optional_inner_text(card.locator("h2"))
        partial_url = await card.locator('a[href*="/p/"]').first.get_attribute("href")
        product_url = urljoin(start_url, partial_url).rstrip("/") if partial_url else ""

        rating_text = await optional_inner_text(card.locator("span.sr2r3oj").first)
        rating = rating_text.split("(")[0].strip() if rating_text else ""
        no_of_reviews = ""
        if "(" in rating_text and ")" in rating_text:
            no_of_reviews = rating_text.split("(", 1)[1].split(")", 1)[0].strip()

        description = await optional_inner_text(card.locator("p.text-neutral-99").first)

        # included_features = []
        # not_included_features = []
        # feature_items = card.locator(
        #     '[data-testid="product-card-category-features"] div.flex.items-center,'
        #     '[data-test-id="product-card-category-features"] div.flex.items-center'
        # )
        # for i in range(await feature_items.count()):
        #     feature = feature_items.nth(i)
        #     text = await optional_inner_text(feature)
        #     icon_class = await feature.locator("i").first.get_attribute("class") or ""
        #     if "icon-check" in icon_class:
        #         included_features.append(text)
        #     elif "icon-x" in icon_class:
        #         not_included_features.append(text)

        if not product_url:
            return None

        return {
            "name": product_name,
            "url": product_url,
            "rating": rating,
            "reviews_count": no_of_reviews,
            "description": description,
        }
    except Exception as e:
        Actor.log.warning(f"Product card parse error: {e}")
        return None


async def scrape_review_page(page) -> tuple[list[dict], bool]:
    await random_scroll(page)
    await human_delay(1.0, 2.0)

    container = page.locator('div[data-test-id="review-cards-container"]')
    review_cards = container.locator("div.e1xzmg0z.c1ofrhif.typo-10")
    reviews_count = await review_cards.count()
    Actor.log.info(f"  Reviews on this page: {reviews_count}")

    if reviews_count == 0:
        return [], False

    reviews = []
    for i in range(reviews_count):
        review = review_cards.nth(i)
        try:
            author_text = await optional_raw_inner_text(review.locator("div.typo-10.text-neutral-90"))
            lines = [line.strip() for line in author_text.split("\n") if line.strip()]

            pros_locator = review.locator("span:has-text('Pros') >> xpath=../following-sibling::p")
            cons_locator = review.locator("span:has-text('Cons') >> xpath=../following-sibling::p")

            reviews.append({
                "review_title": (await optional_inner_text(review.locator("h3"))).replace('"', ""),
                "author_name": lines[0] if len(lines) > 0 else "",
                "author_profession": lines[1] if len(lines) > 1 else "",
                "author_industry": lines[2] if len(lines) > 2 else "",
                "author_duration": lines[3] if len(lines) > 3 else "",
                "review_stars": await optional_inner_text(review.locator("span.sr2r3oj").nth(0)),
                "review_date": await optional_inner_text(review.locator("div.typo-0")),
                "review_description": await optional_inner_text(review.locator("div.space-y-6 > p")),
                "review_pros": await optional_inner_text(pros_locator),
                "review_cons": await optional_inner_text(cons_locator),
            })
        except Exception as e:
            Actor.log.warning(f"Review {i} parse error: {e}")

    return reviews, True


async def load_storage_state(key: str):
    try:
        state = await Actor.get_value(key)
        if isinstance(state, dict):
            Actor.log.info(f"Loaded persistent browser storage state from key '{key}'")
            return state
    except Exception as e:
        Actor.log.warning(f"Could not load browser storage state: {e}")
    return None


async def save_storage_state(context, key: str):
    try:
        state = await context.storage_state()
        await Actor.set_value(key, state)
        Actor.log.info(f"Saved persistent browser storage state to key '{key}'")
    except Exception as e:
        Actor.log.warning(f"Could not save browser storage state: {e}")


async def requeue_request(request_queue, request, retries: int, reason: str):
    retry_url = request.url
    await request_queue.add_request(
        Request.from_url(
            retry_url,
            unique_key=f"{retry_url}#retry-{retries + 1}-{random.random()}",
            user_data={**request.user_data, "retries": retries + 1, "last_retry_reason": reason},
        ),
        forefront=True,
    )


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        category_name = actor_input.get("software_category", "Application Development")
        total_products = int(actor_input.get("total_products_to_scrape", 5))
        max_review_pages = max(1, min(100, int(actor_input.get("review_pages_per_product", 1))))
        max_cf_retries = int(actor_input.get("max_cf_retries", 2))
        cf_wait_seconds = max(45, min(300, int(actor_input.get("cf_wait_seconds", 150))))
        headless = bool(actor_input.get("headless", False))
        use_apify_proxy = bool(actor_input.get("use_apify_proxy", True))
        proxy_groups = actor_input.get("proxy_groups") or ["RESIDENTIAL"]
        proxy_country = actor_input.get("proxy_country", "US")
        cloudflare_cookies = parse_cookies(actor_input.get("cloudflare_cookies"))
        session_id = str(actor_input.get("session_id") or f"capterra_{category_name}_{proxy_country}")
        profile_seed = str(actor_input.get("fingerprint_seed") or session_id)
        fingerprint = build_fingerprint(profile_seed)
        storage_state_key = "BROWSER_STORAGE_STATE_" + hashlib.sha1(session_id.encode("utf-8")).hexdigest()[:16]
        allow_manual_cf = (not headless) and (not is_apify_cloud())
        Actor.log.info(f"Cloudflare manual verification allowed: {allow_manual_cf}")
        Actor.log.info(
            "Using stable browser profile "
            f"session_id='{session_id}' viewport={fingerprint['viewport']['width']}x{fingerprint['viewport']['height']} "
            f"timezone={fingerprint['timezone_id']}"
        )

        category_query = category_name.lower().replace(" ", "-")
        start_url = f"https://www.capterra.com/{category_query}-software/"

        request_queue = await Actor.open_request_queue(name=None)
        await request_queue.add_request(Request.from_url(start_url, user_data={"depth": 0, "retries": 0}))

        products_done = 0
        proxy_configuration = None
        if use_apify_proxy:
            try:
                proxy_configuration = await Actor.create_proxy_configuration(
                    groups=proxy_groups,
                    country_code=proxy_country,
                )
                Actor.log.info(f"Using Apify Proxy groups={proxy_groups} country={proxy_country}")
            except Exception as e:
                Actor.log.warning(f"Apify Proxy is not available in this environment: {e}")

        async with async_playwright() as playwright:
            proxy_info = await new_proxy_info_safe(proxy_configuration, session_id)
            storage_state = await load_storage_state(storage_state_key)
            browser = await launch_browser(
                playwright,
                headless=headless,
                proxy_info=proxy_info,
                fingerprint=fingerprint,
            )
            fingerprint = await align_user_agent_with_browser(browser, fingerprint)
            context = await make_context(
                browser,
                fingerprint=fingerprint,
                cookies=cloudflare_cookies,
                storage_state=storage_state,
            )

            while products_done < total_products and (request := await request_queue.fetch_next_request()):
                page = await context.new_page()
                url = request.url
                depth = int(request.user_data.get("depth", 0))
                retries = int(request.user_data.get("retries", 0))
                Actor.log.info(f"-> {url} depth={depth} retry={retries}/{max_cf_retries}")

                try:
                    if not await goto_verified(
                        page,
                        url,
                        allow_manual=allow_manual_cf,
                        fingerprint=fingerprint,
                        cf_wait_seconds=cf_wait_seconds,
                    ):
                        if retries < max_cf_retries:
                            try:
                                storage_state = await context.storage_state()
                                await save_storage_state(context, storage_state_key)
                            except Exception:
                                pass
                            await safe_close_page(page)
                            await requeue_request(request_queue, request, retries, "cloudflare_not_cleared")
                        else:
                            title = ""
                            body_sample = ""
                            try:
                                title = await page.title()
                                body_sample = (await page.locator("body").inner_text(timeout=5_000))[:1000]
                            except Exception:
                                pass
                            await Actor.push_data({
                                "status": "blocked_by_cloudflare",
                                "url": url,
                                "page_title": title,
                                "headless": headless,
                                "proxy_groups": proxy_groups if use_apify_proxy else [],
                                "proxy_country": proxy_country if use_apify_proxy else "",
                                "message": (
                                    "Cloudflare did not clear after retries. "
                                    "In Apify cloud, headless=false runs inside a virtual display and cannot click human checks. "
                                    "Use a stronger residential proxy or provide fresh manually solved cookies."
                                ),
                                "body_sample": body_sample,
                            })
                            products_done = total_products
                        continue

                    await human_settle(page, fingerprint, 1.5, 3.0)
                    await save_storage_state(context, storage_state_key)

                    if depth == 0:
                        await page.wait_for_selector('div[id^="product-card-container-"]', timeout=30_000)
                        cards = page.locator('div[id^="product-card-container-"]')
                        count_cards = await cards.count()
                        Actor.log.info(f"Cards on page: {count_cards}")

                        for i in range(min(total_products, count_cards)):
                            product = await scrape_product_card(cards.nth(i), start_url)
                            if not product:
                                continue

                            review_url = f"{product['url']}/reviews/?page=1"
                            await request_queue.add_request(
                                Request.from_url(
                                    review_url,
                                    user_data={
                                        "depth": 1,
                                        "retries": 0,
                                        "current_page": 1,
                                        "product": product,
                                        "all_reviews": [],
                                    },
                                )
                            )
                            Actor.log.info(f"Queued reviews: {review_url}")

                    elif depth == 1:
                        current_page = int(request.user_data.get("current_page", 1))
                        product = request.user_data.get("product", {})
                        all_reviews = request.user_data.get("all_reviews", [])

                        if current_page == 1:
                            page_title = await optional_inner_text(page.locator("h1"))
                            overview = await optional_inner_text(page.locator("section#key-takeaways div.lg\\:w-7\\/12"))
                            product["review_page_title"] = page_title
                            product["overview"] = overview
                  

                        page_reviews, has_more = await scrape_review_page(page)
                        all_reviews.extend(page_reviews)

                        next_page = current_page + 1
                        if has_more and page_reviews and next_page <= max_review_pages:
                            base_url = product["url"]
                            await request_queue.add_request(
                                Request.from_url(
                                    f"{base_url}/reviews/?page={next_page}",
                                    user_data={
                                        "depth": 1,
                                        "retries": 0,
                                        "current_page": next_page,
                                        "product": product,
                                        "all_reviews": all_reviews,
                                    },
                                ),
                                forefront=True,
                            )
                        else:
                            await Actor.push_data({
                                **product,
                                "total_reviews_scraped": len(all_reviews),
                                "reviews": all_reviews,
                            })
                            await save_storage_state(context, storage_state_key)
                            products_done += 1
                            Actor.log.info(f"Done {products_done}/{total_products}: {product.get('name')}")

                except Exception as e:
                    Actor.log.exception(f"Error on {url}: {e}")
                    if retries < max_cf_retries:
                        try:
                            storage_state = await context.storage_state()
                        except Exception:
                            pass
                        try:
                            await context.close()
                        except Exception:
                            pass
                        try:
                            await browser.close()
                        except Exception:
                            pass
                        retry_session_id = f"{session_id}_exception_{retries + 1}"
                        retry_fingerprint = build_fingerprint(f"{profile_seed}-exception-{retries + 1}")
                        proxy_info = await new_proxy_info_safe(proxy_configuration, retry_session_id)
                        browser = await launch_browser(
                            playwright,
                            headless=headless,
                            proxy_info=proxy_info,
                            fingerprint=retry_fingerprint,
                        )
                        retry_fingerprint = await align_user_agent_with_browser(browser, retry_fingerprint)
                        context = await make_context(
                            browser,
                            fingerprint=retry_fingerprint,
                            cookies=cloudflare_cookies,
                            storage_state=storage_state,
                        )
                        fingerprint = retry_fingerprint
                        await requeue_request(request_queue, request, retries, str(e)[:200])
                    else:
                        await Actor.push_data({
                            "status": "failed_after_retries",
                            "url": url,
                            "depth": depth,
                            "retries": retries,
                            "error": str(e),
                        })

                finally:
                    await safe_close_page(page)
                    await request_queue.mark_request_as_handled(request)

            await save_storage_state(context, storage_state_key)
            await context.close()
            await browser.close()
