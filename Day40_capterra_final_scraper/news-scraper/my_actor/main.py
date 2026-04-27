from __future__ import annotations
from urllib.parse import urljoin
from apify import Actor, Request
from playwright.async_api import async_playwright
import asyncio
import random

def build_url(base_url , query , from_date, to_date, sort_by,api_key):
    if query:
        base_url.append(f"?q={query}")
    if from_date:
        base_url.append(f"&from={from_date}")
    if to_date:
        base_url.append(f"&to={to_date}")
    if sort_by:
        base_url.append(f"&sortBy={sort_by}")
    if api_key:
        base_url.append(f"&apiKey={api_key}")

    return base_url


async def main() -> None:

    async with Actor:
        actor_input = await Actor.get_input() or {}
        query = actor_input.get('query', "war").lower()
        from_date = actor_input.get('fromDate', "")
        to_date = actor_input.get('toDate', "")
        sort_by = actor_input.get('sortBy', "")
        API_KEY = actor_input.get('apiKey', "")
        # city_query = city_name.lower()


        if (not API_KEY):
            Actor.log.info('No API KEY specified, exiting...')
            return

        # start_url = f"https://in.bookmyshow.com/explore/events-{city_query}?cat=CT"
        base_url = f"https://newsapi.org/v2/everything"
        start_url = build_url(base_url)
        request_queue = await Actor.open_request_queue()

        await request_queue.add_request(
            Request.from_url(start_url, user_data={'depth': 0})
        )

        # total_events = actor_input.get('total_events_to_scrape', 20)
        # count_events = 0
        # stop_scrapping = False

        async with async_playwright() as playwright:

            # proxy_configuration = await Actor.create_proxy_configuration(
            #     groups=["RESIDENTIAL"]
            # )

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
                    await page.goto(url, timeout=60000)
                    await asyncio.sleep(random.uniform(2, 4))

                    if depth == 0:
                        events_links = await page.locator(".sc-133848s-11.sc-1ljcxl3-1").all()

                        for event in events_links:
                            link_href = await event.get_attribute('href')

                            if link_href:
                                await request_queue.add_request(
                                    Request.from_url(link_href, user_data={'depth': 1})
                                )

                    elif depth == 1:
                        title = await page.locator("h1.sc-7o7nez-0").inner_text()

                        date = await get_field(page, "calendar")
                        time = await get_field(page, "time")
                        duration = await get_field(page, "duration")
                        age = await get_field(page, "age_limit")
                        language = await get_field(page, "language")
                        venue = await get_field(page, "location")
                        genre = await get_field(page, "genre")

                        # price
                        price_locator = page.locator("span:has-text('₹')")

                        if await price_locator.count() > 0:
                            price = await price_locator.first.inner_text()
                            price.replace("\u20b9", "₹")
                        
                        # how many interested
                        interested_card = page.locator("div.sc-7o7nez-0", has_text="are interested")
                        how_many_interested = await interested_card.inner_text()

                        # About event
                        about_section = page.locator("a.sc-133848s-11.sc-1ljcxl3-1")
                        paragraphs = about_section.locator("p")
                        texts = []
                        for i in range(await paragraphs.count()):
                            txt = await paragraphs.nth(i).inner_text()
                            if txt.strip(): 
                                texts.append(txt)

                        about_text = "\n".join(texts)
                        print(about_text)

                        data = {
                            "title": title,
                            "date": date,
                            "time": time,
                            "age": age,
                            "duration": duration,
                            "language": language,
                            "venue": venue,
                            "genre":genre,
                            "price": price,
                            "url":url,
                            "How many interested":how_many_interested,
                            "About the Event" : about_text
                        }
                        # Actor.log.info(f"data----------------{data}")

                        count_events += 1
                        await Actor.push_data(data)

                        if count_events >= total_events:
                            stop_scrapping = True

                except Exception as e:
                    Actor.log.exception(f'Error on {url}: {e}')

                finally:
                    await page.close()
                    await context.close()
                    await request_queue.mark_request_as_handled(request)