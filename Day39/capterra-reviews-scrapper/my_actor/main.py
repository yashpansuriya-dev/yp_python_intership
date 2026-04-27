from __future__ import annotations

import asyncio
import os
import random
import sys
from urllib.parse import urljoin

from apify import Actor, Request
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

# ──────────────────────────────────────────────────────────────────────────────
# STEALTH SCRIPT
# ──────────────────────────────────────────────────────────────────────────
STEALTH_SCRIPT = """
(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

    const pluginData = [
        { name: 'Chrome PDF Plugin',  filename: 'internal-pdf-viewer',             description: 'Portable Document Format' },
        { name: 'Chrome PDF Viewer',  filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: '' },
        { name: 'Native Client',      filename: 'internal-nacl-plugin',             description: '' },
    ];
    const pluginArray = pluginData.map(p => {
        const plugin = Object.create(Plugin.prototype);
        Object.defineProperties(plugin, {
            name:        { value: p.name },
            filename:    { value: p.filename },
            description: { value: p.description },
            length:      { value: 0 },
        });
        return plugin;
    });
    Object.defineProperty(pluginArray, '__proto__', { value: PluginArray.prototype });
    Object.defineProperty(navigator, 'plugins', { get: () => pluginArray });

    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });

    window.chrome = {
        app: { isInstalled: false },
        runtime: { connect: () => {}, sendMessage: () => {}, id: 'nkbihfbeogaeaoehlefnkodbefgpgknn' },
        loadTimes: () => ({}),
        csi: () => ({}),
    };

    const origQuery = window.navigator.permissions && window.navigator.permissions.query;
    if (origQuery) {
        window.navigator.permissions.__proto__.query = function(parameters) {
            return parameters.name === 'notifications'
                ? Promise.resolve({ state: Notification.permission, onchange: null })
                : origQuery.call(this, parameters);
        };
    }

    Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    Object.defineProperty(navigator, 'deviceMemory',        { get: () => 8 });
    Object.defineProperty(navigator, 'platform',            { get: () => 'Win32' });

    const getParam = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(param) {
        if (param === 37445) return 'Google Inc. (Intel)';
        if (param === 37446) return 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)';
        return getParam.call(this, param);
    };
    if (typeof WebGL2RenderingContext !== 'undefined') {
        const getParam2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(param) {
            if (param === 37445) return 'Google Inc. (Intel)';
            if (param === 37446) return 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)';
            return getParam2.call(this, param);
        };
    }

    Object.defineProperty(window, 'outerWidth',  { get: () => window.innerWidth        });
    Object.defineProperty(window, 'outerHeight', { get: () => window.innerHeight + 80  });
    Object.defineProperty(screen, 'availWidth',  { get: () => window.screen.width      });
    Object.defineProperty(screen, 'availHeight', { get: () => window.screen.height - 40});

    Object.defineProperty(navigator, 'connection', {
        get: () => ({ rtt: 50, downlink: 10, effectiveType: '4g', saveData: false })
    });

    if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
        navigator.mediaDevices.enumerateDevices = async () => [{
            deviceId: 'default', kind: 'audioinput', label: '', groupId: 'default'
        }];
    }

    [
        '__webdriver_script_fn','__driver_evaluate','__webdriver_evaluate',
        '__selenium_evaluate','__fxdriver_evaluate','__driver_unwrapped',
        '__webdriver_unwrapped','__selenium_unwrapped','__fxdriver_unwrapped',
        '_Selenium_IDE_Recorder','_selenium','calledSelenium',
        '$chrome_asyncScriptInfo','$cdc_asdjflasutopfhvcZLmcfl_',
        '_WEBDRIVER_ELEM_CACHE','ChromeDriverw',
    ].forEach(p => {
        try { Object.defineProperty(window, p, { get: () => undefined, set: () => {} }); } catch(e) {}
    });

    const origIframe = HTMLIFrameElement.prototype.__lookupGetter__('contentWindow');
    if (origIframe) {
        Object.defineProperty(HTMLIFrameElement.prototype, 'contentWindow', {
            get: function() {
                const win = origIframe.call(this);
                if (!win) return win;
                try { Object.defineProperty(win.navigator, 'webdriver', { get: () => undefined }); } catch(e) {}
                return win;
            }
        });
    }
})();
"""

# ──────────────────────────────────────────────────────────────────────────────
# Human-like helpers
# ──────────────────────────────────────────────────────────────────────────────
async def human_delay(min_s=1.5, max_s=4.0):
    await asyncio.sleep(random.uniform(min_s, max_s))

async def human_mouse_wander(page):
    for _ in range(random.randint(4, 8)):
        x = random.randint(80, 1200)
        y = random.randint(80, 700)
        await page.mouse.move(x, y, steps=random.randint(15, 30))
        await asyncio.sleep(random.uniform(0.08, 0.35))

async def random_scroll(page):
    for _ in range(random.randint(3, 5)):
        await page.evaluate(f"window.scrollBy(0, {random.randint(200, 600)})")
        await asyncio.sleep(random.uniform(0.4, 1.0))

# ──────────────────────────────────────────────────────────────────────────────
# Cloudflare challenge waiter
# ──────────────────────────────────────────────────────────────────────────────
CF_TITLES = {
    "just a moment", "attention required!", "please wait...",
    "checking your browser", "one more step", "ddos-guard",
    "security check", "access denied",
}

async def wait_for_cloudflare(page, timeout_s=45, *, allow_manual=False) -> bool:
    deadline = asyncio.get_event_loop().time() + timeout_s
    manual_notice_shown = False
    while asyncio.get_event_loop().time() < deadline:
        try:
            title = (await page.title()).lower().strip()
        except Exception:
            title = ""

        Actor.log.info(f"[CF] title='{title}'")

        captcha = await page.locator(
            "iframe[src*='challenges.cloudflare.com'],"
            "iframe[src*='hcaptcha.com'],"
            "div#challenge-form,"
            "div#cf-challenge-running"
        ).count()
        if captcha:
            if allow_manual:
                if not manual_notice_shown:
                    Actor.log.warning("[CF] Manual checkbox detected. Click it in the opened browser; the actor will wait.")
                    manual_notice_shown = True
                await asyncio.sleep(2)
                continue
            Actor.log.warning("[CF] CAPTCHA/Turnstile detected — will retry with new proxy.")
            return False

        if not any(kw in title for kw in CF_TITLES):
            Actor.log.info("[CF] Challenge cleared ✓")
            return True

        await human_mouse_wander(page)
        await asyncio.sleep(2)

    Actor.log.warning("[CF] Timed out waiting for challenge to clear.")
    return False

# ──────────────────────────────────────────────────────────────────────────────
# Build hardened browser context
# ──────────────────────────────────────────────────────────────────────────────
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
]
VIEWPORTS = [
    {"width": 1280, "height": 720},
    {"width": 1366, "height": 768},
    {"width": 1440, "height": 900},
    {"width": 1920, "height": 1080},
]

async def make_context(browser, *, use_stealth: bool = False):
    vp = random.choice(VIEWPORTS)
    context = await browser.new_context(
        viewport=vp,
        screen=vp,
        locale="en-US",
        timezone_id="America/New_York",
        color_scheme="light",
        java_script_enabled=True,
        accept_downloads=False,
    )
    if use_stealth:
        await context.add_init_script(STEALTH_SCRIPT)
    return context


async def launch_browser(playwright, *, headless: bool):
    args = [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled",
        "--window-size=1366,768",
    ]

    if os.name == "nt" and not headless:
        try:
            Actor.log.info("Launching installed Google Chrome")
            return await playwright.chromium.launch(
                channel="chrome",
                headless=headless,
                args=args,
            )
        except Exception as e:
            Actor.log.warning(f"Could not launch Chrome channel, falling back to bundled Chromium: {e}")

    Actor.log.info("Launching bundled Chromium")
    return await playwright.chromium.launch(
        headless=headless,
        args=args,
    )

# ──────────────────────────────────────────────────────────────────────────────
# Scrape reviews on a single page
# Returns: (reviews_list, has_more)
#   has_more = False → page had 0 reviews, stop paginating for this product
# ──────────────────────────────────────────────────────────────────────────────
async def scrape_review_page(page) -> tuple[list[dict], bool]:
    reviews = []

    await random_scroll(page)
    await human_delay(1.5, 3)


    container = page.locator('div[data-test-id="review-cards-container"]')
    review_cards = container.locator("div.e1xzmg0z.c1ofrhif.typo-10")
    reviews_count = await review_cards.count()

    Actor.log.info(f"  Reviews on this page: {reviews_count}")

    # 0 reviews = page doesn't exist (product has fewer pages than requested)
    if reviews_count == 0:
        return [], False

    for i in range(reviews_count):
        review = review_cards.nth(i)

        try:
            # 👤 AUTHOR INFO
            author_card = review.locator("div.typo-10.text-neutral-90")
            full_text = (await author_card.inner_text()).strip()
            lines     = [l.strip() for l in full_text.split("\n") if l.strip()]

            a_name     = lines[0]   # "Gunther C."
            a_prof      = lines[1]   # "Software Engineer"
            a_industry = lines[2]   # "Computer Software"
            a_duration = lines[3]   # "Used the software for: 2+ years"

            # 📝 TITLE
            r_title = (await review.locator("h3").inner_text()).strip().replace('"', '')

            # ⭐ RATING
            r_stars = (await review.locator("span.sr2r3oj").nth(0).inner_text()).strip()

            # 📅 DATEbb
            r_date = (await review.locator("div.typo-0").inner_text()).strip()

            # 📄 DESCRIPTION
            desc_locator = review.locator("div.space-y-6 > p")
            r_desc = (await desc_locator.inner_text()).strip() if await desc_locator.count() else ""

            # 👍 PROS
            pros_locator = review.locator("span:has-text('Pros') >> xpath=../following-sibling::p")
            r_pros = (await pros_locator.inner_text()).strip() if await pros_locator.count() else ""

            # 👎 CONS
            cons_locator = review.locator("span:has-text('Cons') >> xpath=../following-sibling::p")
            r_cons = (await cons_locator.inner_text()).strip() if await cons_locator.count() else ""

            reviews.append({
                "review_title": r_title,
                "author_name": a_name,
                "author_profession": a_prof,
                "author_industry": a_industry,
                "author_duratiion":a_duration,
                "review_stars": r_stars,
                "review_date": r_date,
                "review_description": r_desc,
                "review_pros": r_pros,
                "review_cons": r_cons,
            })

        except Exception as e:
            Actor.log.warning(f"Review {i} parse error: {e}")

    return reviews, True


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
async def main() -> None:
    async with Actor:
        actor_input      = await Actor.get_input() or {}
        category_name    = actor_input.get('software_category', "website-security")
        category_query   = category_name.lower().replace(" ", "-")
        start_url        = f"https://www.capterra.com/{category_query}-software/"
        # start_url = "https://www.g2.com/categories/conversational-intelligence"

        total_products   = int(actor_input.get('total_products_to_scrape', 5))
        max_review_pages = int(actor_input.get('review_pages_per_product', 10))
        max_retries      = int(actor_input.get('max_cf_retries', 4))
        headless         = False
        use_stealth      = bool(actor_input.get('use_stealth', False))

        # Enforce bounds — min 1, max 100
        max_review_pages = max(1, min(100, max_review_pages))

        count_products   = 0
        stop_scrapping   = False

        request_queue = await Actor.open_request_queue(name=None)
        await request_queue.add_request(
            Request.from_url(start_url, user_data={'depth': 0, 'retries': 0})
        )

        # proxy_configuration = await Actor.create_proxy_configuration(
        #     groups=["RESIDENTIAL"],
        #     country_code="US",
        # )

        async with async_playwright() as playwright:
            browser = await launch_browser(playwright, headless=False)
            context = await make_context(browser, use_stealth=use_stealth)

            while not stop_scrapping and (request := await request_queue.fetch_next_request()):
                url     = request.url
                depth   = int(request.user_data.get('depth', 0))
                retries = int(request.user_data.get('retries', 0))

                Actor.log.info(f"→ {url}  depth={depth}  retry={retries}/{max_retries}")

                # proxy_info = await proxy_configuration.new_proxy_info()
                page       = await context.new_page()

                try:
                    response = await page.goto(url, wait_until="domcontentloaded", timeout=60_000)
                    Actor.log.info(f"HTTP {response.status if response else '?'}")

                    cf_ok = await wait_for_cloudflare(
                        page,
                        timeout_s=180 if not headless else 45,
                        allow_manual=not headless,
                    )

                    if not cf_ok:
                        if retries < max_retries:
                            wait_time = (2 ** retries) * 3
                            Actor.log.warning(f"CF not cleared — retrying in {wait_time}s …")
                            await asyncio.sleep(wait_time)
                            await request_queue.add_request(
                                Request.from_url(
                                    url,
                                    unique_key=f"{url}#cf-retry-{retries + 1}-{random.random()}",
                                    user_data={'depth': depth, 'retries': retries + 1},
                                ),
                                forefront=True,
                            )
                        else:
                            Actor.log.error(f"Gave up on {url} after {max_retries} CF retries.")
                        continue

                    await human_delay(2, 4)
                    await human_mouse_wander(page)
                    await random_scroll(page)
                    await human_delay(1, 2)

                    # ══════════════════════════════════════════════════════
                    # DEPTH 0 — listing page
                    # ══════════════════════════════════════════════════════
                    if depth == 0:
                        title = await page.title()
                        Actor.log.info(f"Listing title: {title}")

                        try:
                            await page.wait_for_selector('div[id^="product-card-container-"]', timeout=20_000)
                        except Exception:
                            Actor.log.warning("Product cards not found — re-queuing.")
                            if retries < max_retries:
                                await request_queue.add_request(
                                    Request.from_url(
                                        url,
                                        unique_key=f"{url}#cards-retry-{retries + 1}-{random.random()}",
                                        user_data={'depth': 0, 'retries': retries + 1},
                                    ),
                                    forefront=True,
                                )
                            continue

                        cards       = page.locator('div[id^="product-card-container-"]')
                        count_cards = await cards.count()
                        Actor.log.info(f"Cards on page: {count_cards}")

                        added = 0
                        for i in range(min(total_products, count_cards)):
                            card = cards.nth(i)
                            link = card.locator('a[href*="/p/"]')
                            if await link.count() == 0:
                                Actor.log.warning(f"No /p/ link for card {i}")
                                continue
                            try:
                                href = await link.first.get_attribute('href', timeout=5_000)
                            except Exception:
                                Actor.log.warning(f"Timeout on card {i}")
                                continue
                            if not href:
                                continue

                            # Strip trailing slash then build /reviews/?page=1
                            base_product_url = urljoin(start_url, href).rstrip("/")
                            first_review_url = f"{base_product_url}/reviews/?page=1"

                            await request_queue.add_request(
                                Request.from_url(
                                    first_review_url,
                                    user_data={
                                        'depth':            1,
                                        'retries':          0,
                                        'current_page':     1,
                                        'base_product_url': base_product_url,
                                        'all_reviews':      [],
                                        'product_title':    '',
                                        'overview':         '',
                                    }
                                )
                            )
                            added += 1
                            Actor.log.info(f"  Queued [{added}]: {first_review_url}")

                    # ══════════════════════════════════════════════════════
                    # DEPTH 1 — review page (paginated)
                    # ══════════════════════════════════════════════════════
                    elif depth == 1:
                        current_page     = int(request.user_data.get('current_page', 1))
                        base_product_url = request.user_data.get('base_product_url', '')
                        all_reviews      = request.user_data.get('all_reviews', [])
                        product_title    = request.user_data.get('product_title', '')
                        overview         = request.user_data.get('overview', '')

                        Actor.log.info(f"  Review page {current_page}/{max_review_pages}")

                        # Grab title + overview only on page 1
                        if current_page == 1:
                            try:
                                await page.wait_for_selector("h1", timeout=20_000)
                                product_title = " ".join((await page.locator("h1").first.inner_text()).split())
                                ov_loc        = page.locator("section#key-takeaways div.lg\\:w-7\\/12")
                                overview      = " ".join((await ov_loc.inner_text()).split()) if await ov_loc.count() > 0 else ""
                                Actor.log.info(f"  Product: {product_title}")
                            except Exception as e:
                                Actor.log.warning(f"  Could not get title/overview: {e}")

                        # Scrape this page's reviews
                        page_reviews, has_more = await scrape_review_page(page)
                        all_reviews.extend(page_reviews)

                        Actor.log.info(
                            f"  Page {current_page}: +{len(page_reviews)} reviews "
                            f"| total so far: {len(all_reviews)}"
                        )

                        next_page       = current_page + 1
                        should_paginate = (
                            has_more                        # this page had reviews
                            and len(page_reviews) > 0       # safety double-check
                            and next_page <= max_review_pages  # within user limit
                        )

                        if should_paginate:
                            next_url = f"{base_product_url}/reviews/?page={next_page}"
                            await request_queue.add_request(
                                Request.from_url(
                                    next_url,
                                    user_data={
                                        'depth':            1,
                                        'retries':          0,
                                        'current_page':     next_page,
                                        'base_product_url': base_product_url,
                                        'all_reviews':      all_reviews,
                                        'product_title':    product_title,
                                        'overview':         overview,
                                    }
                                ),
                                forefront=True,  # finish this product before moving to next
                            )
                            Actor.log.info(f"  → Queued page {next_page}: {next_url}")

                        else:
                            # Done with this product — push all collected data
                            reason = "no more reviews" if not has_more else f"page limit reached ({max_review_pages})"
                            Actor.log.info(f"  ✓ Done ({reason}) — pushing {len(all_reviews)} total reviews.")

                            await Actor.push_data({
                                "title":                 product_title,
                                # "overview":              overview,
                                "total_reviews_scraped": len(all_reviews),
                                "reviews":               all_reviews,
                            })

                            count_products += 1
                            if count_products >= total_products:
                                stop_scrapping = True

                except Exception as e:
                    Actor.log.exception(f"Error on {url}: {e}")

                finally:
                    await page.close()
                    await request_queue.mark_request_as_handled(request)

            await context.close()
            await browser.close()
