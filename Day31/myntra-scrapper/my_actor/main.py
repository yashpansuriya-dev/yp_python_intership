from __future__ import annotations
from urllib.parse import urljoin
from apify import Actor, Request
from playwright.async_api import async_playwright
import asyncio
import random

async def main() -> None:

    async with Actor:
        actor_input = await Actor.get_input() or {}
        start_url = "https://test.dupagecircuitclerk.gov/"
        request_queue = await Actor.open_request_queue()

        await request_queue.add_request(
            Request.from_url(start_url, user_data={'depth': 0})
        )

        MAX_RETRIES = 3
        async with async_playwright() as playwright:
            # proxy_configuration = await Actor.create_proxy_configuration(
            #     groups=["RESIDENTIAL"]
            # )

            browser = await playwright.chromium.launch(headless=False)

            while request := await request_queue.fetch_next_request():
                url = request.url
                depth = int(request.user_data['depth'])

                Actor.log.info(f'Scraping {url} (depth={depth}) ...')
                success = False

                for attempt in range( 1, MAX_RETRIES+1 ):

                # ROTATE PROXY PER REQUEST
                    # proxy_info = await proxy_configuration.new_proxy_info()

                    context = await browser.new_context(
                        # proxy={
                        #     "server": proxy_info.url,
                        #     "username": proxy_info.username,
                        #     "password": proxy_info.password,
                        # },
                        user_agent=random.choice([
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                        ]),
                        viewport={"width": 1280, "height": 800}
                    )

                    page = await context.new_page()

                    try:
                        # 🧪 DEBUG IP
                        await page.goto("https://httpbin.org/ip", timeout=60000)
                        ip = await page.text_content("body")
                        print("Current IP:", ip)

                        # 🌐 OPEN TARGET
                        await page.goto(url, timeout=60000)
                        await asyncio.sleep(random.uniform(2, 4))
                        await page.mouse.move(100, 200)
                        Actor.log.info(f"Scrapping {url} with {attempt}th Attempt")


                        if depth == 0 or depth == 1:
                            all_links = await page.locator("a").all()

                            # for job in all_links:
                            #     link_href = await job.get_attribute('href')
                                # full_url = urljoin(url, link_href)
                                # if link_href:
                                #     await request_queue.add_request(
                                #         Request.from_url(full_url, user_data={'depth': depth+1})
                                #     )
                            for link in all_links:
                                link_href = await link.get_attribute('href')

                                if not link_href:
                                    continue

                                if link_href.startswith(("javascript:", "mailto:", "tel:")):
                                    continue

                                full_url = urljoin(url, link_href)

                                if not full_url.startswith(("http://", "https://")):
                                    continue

                                if "dupagecircuitclerk.gov" not in full_url:
                                    continue

                                await request_queue.add_request(
                                    Request.from_url(full_url, user_data={'depth': depth+1})
                                )

                        # elif depth == 1:
                            # content_section = await page.locator("section").first.inner_text()

                        # locator = page.locator("section").first
                        # if await locator.count() > 0:
                        #     content_section = await locator.inner_text()
                        # else:
                        #     content_section = "No section found"
                        try:
                            content = await page.text_content("section")
                        except:
                            try:
                                content = await page.locator("main")
                            except:
                                content ="No Content found"


                        data = {
                            "url": page.url,
                            "text": content
                        }

                        await Actor.push_data(data)

                        success = True
                        break

                    except Exception as e:
                        Actor.log.warning(f'Error on {url} with {attempt}th Attempt : {e}')

                    finally:
                        await page.close()
                        await context.close()
                
                if not success:
                    Actor.log.error(f"Failed After {MAX_RETRIES} retries : {url}")
                    
                await request_queue.mark_request_as_handled(request)