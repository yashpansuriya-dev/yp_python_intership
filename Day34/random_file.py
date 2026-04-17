'''
proxy_configuration = await Actor.create_proxy_configuration(
    //DATACENTER OR RESIDENTIAL
    groups=['DATACENTER'] 
)

proxy_info = await proxy_configuration.new_proxy_info()

context = await browser.new_context(
    proxy={
        "server": proxy_info.url,
        "username": proxy_info.username,
        "password": proxy_info.password,
    }
)
'''

from __future__ import annotations
from urllib.parse import urljoin
from apify import Actor, Request
from playwright.async_api import async_playwright
import asyncio
import random

async def main() -> None:

    async with Actor:
        actor_input = await Actor.get_input() or {}
        job_role = actor_input.get('job_role', "Java Developer")
        role_query = job_role.replace(" ", "%20")

        if not job_role:
            Actor.log.info('No Job role specified, exiting...')
            return

        start_url = f"https://in.linkedin.com/jobs/search?keywords={role_query}"
        request_queue = await Actor.open_request_queue()

        await request_queue.add_request(
            Request.from_url(start_url, user_data={'depth': 0})
        )

        total_jobs = actor_input.get('total_jobs_to_scrape', 20)
        count = 0
        stop_scrapping = False

        async with async_playwright() as playwright:

            proxy_configuration = await Actor.create_proxy_configuration(
                groups=["RESIDENTIAL"]
            )

            browser = await playwright.chromium.launch(headless=True)

            while not stop_scrapping and (request := await request_queue.fetch_next_request()):
                url = request.url
                depth = int(request.user_data['depth'])

                Actor.log.info(f'Scraping {url} (depth={depth}) ...')

                # ROTATE PROXY PER REQUEST
                proxy_info = await proxy_configuration.new_proxy_info()

                context = await browser.new_context(
                    proxy={
                        "server": proxy_info.url,
                        "username": proxy_info.username,
                        "password": proxy_info.password,
                    },
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

                    try:
                        await page.locator("button[aria-label='Dismiss']").first.click(timeout=2000)
                    except:
                        pass

                    if depth == 0:
                        jobs_links = await page.locator(".base-card__full-link").all()

                        for job in jobs_links:
                            link_href = await job.get_attribute('href')

                            if link_href:
                                await request_queue.add_request(
                                    Request.from_url(link_href, user_data={'depth': 1})
                                )

                    elif depth == 1:
                        job_role = await page.locator("h1.topcard__title").inner_text()
                        company = await page.locator(".topcard__org-name-link").inner_text()
                        location = await page.locator(".topcard__flavor--bullet").first.inner_text()
                        apply_link = page.url

                        app_starting_date = await page.locator(".posted-time-ago__text").inner_text()

                        data = {
                            "job_role": job_role,
                            "company": company,
                            "location": location,
                            "apply_link": apply_link,
                            "application_started_date": app_starting_date,
                        }

                        count += 1
                        await Actor.push_data(data)

                        if count >= total_jobs:
                            stop_scrapping = True

                except Exception as e:
                    Actor.log.exception(f'Error on {url}: {e}')

                finally:
                    await page.close()
                    await context.close()
                    await request_queue.mark_request_as_handled(request)

# ---------------------------------------------------
{
    "$schema": "https://apify.com/schemas/v1/input.ide.json",
    "title": "Python Playwright Scraper",
    "type": "object",
    "schemaVersion": 1,
    "properties": {
        "job_role" : {
            "title":"Job Role",
            "type":"string",
            "description":"which Role Do you want",
            "default": "Java Developer",
            "editor": "textfield"
        },
        "total_jobs_to_scrape":{
            "title": "Total No. Jobs To scrape",
            "type":"integer",
            "description": "Defines Total no. of Books to want",
            "default":5,
            "minimum":1,
            "maximum":50
        },
        "max_depth": {
            "title": "Maximum depth",
            "type": "integer",
            "description": "Depth to which to scrape to",
            "default": 1
        }
    },
    "required": ["job_role"]
}
