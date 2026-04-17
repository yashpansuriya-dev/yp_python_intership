from __future__ import annotations

import asyncio
import random
import sys
from typing import Any
from urllib.parse import quote_plus

from apify import Actor, Request
from playwright.async_api import Browser, BrowserContext, Page, async_playwright


sys.stdout.reconfigure(encoding='utf-8')

# https://in.bookmyshow.com/explore/events-ahmedabad?
# categories=workshops|performances
# &daygroups=tomorrow
# &languages=hindi|malayalam
# &tags=outdoor-events
# &priceGroup=0to500
# https://in.bookmyshow.com/explore/events-ahmedabad?daygroups=custom:20260420-20260430&priceGroup=0to500

def build_url(city, filters):
    base_url = f"https://in.bookmyshow.com/explore/events-{city}?cat=CT"
    params = []

    if filters.get('categories'):
        params.append("&categories="+(filters.get('categories')))
    
    if filters.get('from_date') and filters.get('to_date'):
        params.append(f"&daygroups=custom:{filters.get('from_date').replace("-", "")}-{filters.get('to_date').replace("-","")}")

    if filters.get('languages'):
        params.append("&languages="+"|".join(filters.get('languages')))

    if filters.get('from_price') and filters.get('to_price'):
        params.append(f"&priceGroup={filters.get('from_price')}to{filters.get('to_price')}")
    
    url = base_url + "".join(params)
    return url

        
async def get_field(page, icon_name):
    try:
        locator = page.locator(f"img[src*='{icon_name}']").first
        card = locator.locator("xpath=ancestor::a")

        text = await card.locator(".sc-7o7nez-0").inner_text()
        return text

    except:
        return None

async def main() -> None:

    async with Actor:
        actor_input = await Actor.get_input() or {}
        city_name = actor_input.get('city_name', "Ahmedabad")
        city_query = city_name.lower()

        if not city_name:
            Actor.log.info('No City name specified, exiting...')
            return
        
        filters = {
            "categories": actor_input.get("categories"),
            "from_date" : actor_input.get("from_date"),
            "to_date" : actor_input.get("to_date"),
            "from_price" : actor_input.get("from_price"),
            "to_price" : actor_input.get("to_price"),
            "languages": actor_input.get("languages")
        }

        start_url = build_url(city_query, filters)

        # start_url = f"https://in.bookmyshow.com/explore/events-{city_query}?cat=CT
        request_queue = await Actor.open_request_queue(name=None)

        await request_queue.add_request(
            Request.from_url(start_url, user_data={'depth': 0})
        )

        total_events_string = actor_input.get('total_events_to_scrape', 20)
        total_events = int(total_events_string)
        count_events = 0
        stop_scrapping = False

        async with async_playwright() as playwright:

            # proxy_configuration = await Actor.create_proxy_configuration(
            #     groups=["RESIDENTIAL"]
            # )

            browser = await playwright.chromium.launch(headless=False)

            while not stop_scrapping and (request := await request_queue.fetch_next_request()):
                url = request.url
                depth = int(request.user_data['depth'])

                Actor.log.info(f'Scraping {url} (depth={depth}) ...')

                # ROTATE PROXY PER REQUEST
                # proxy_info = await proxy_configuration.new_proxy_info()

                context = await browser.new_context(
                    # proxy={
                    #     "server": proxy_info.url,
                    #     "username": proxy_info.username,
                    #     "password": proxy_info.password,
                    # },
                    # user_agent=random.choice([
                    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                    # ]),
                    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                )

                page = await context.new_page()

                try:
                    await page.goto(url, timeout=60000)
                    Actor.log.info(f'-----Scraping {url} (depth={depth}) ...')

                    await asyncio.sleep(random.uniform(2, 4))

                    if depth == 0:
                        Actor.log.info(f'-------------------Scraping {url} (depth={depth}) ...')
                        await asyncio.sleep(7)  # wait 5 seconds

                        events_links = await page.locator(".sc-133848s-11.sc-1ljcxl3-1").all()
                        Actor.log.info(f"Events found: {len(events_links)}")

                        for event in events_links:
                            link_href = await event.get_attribute('href')
                            # Actor.log.info("linkkkkkkktitle: "+link_href)

                            if link_href:
                                await request_queue.add_request(
                                    Request.from_url(link_href, user_data={'depth': 1})
                                )
                            

                    elif depth == 1:

                        # await page.wait_for_load_state("domcontentloaded")
                        # await page.wait_for_selector("h1", timeout=10000)

                        # title = await page.locator("h1").first.inner_text()
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
                        # interested_card = page.locator("div.sc-7o7nez-0", has_text="are interested")
                        # how_many_interested = await interested_card.inner_text()
                        interested_card = page.locator("text=are interested")

                        if await interested_card.count() > 0:
                            how_many_interested = await interested_card.first.inner_text()
                        else:
                            how_many_interested = None


                        # About event
                        about_section = page.locator("a.sc-133848s-11.sc-1ljcxl3-1")
                        paragraphs = about_section.locator("p")
                        texts = []
                        for i in range(await paragraphs.count()):
                            txt = await paragraphs.nth(i).inner_text()
                            if txt.strip(): 
                                texts.append(txt)

                        about_text = "\n".join(texts)
                        # print(about_text)

                        data = {
                            "title": title,
                            "event_date": date,
                            "event_time": time,
                            "age_limit": age,
                            "duration": duration,
                            "language": language,
                            "venue": venue,
                            "genre":genre,
                            "price": price,
                            "event_url":url,
                            "interested_people_count":how_many_interested.replace("are interested","").strip(),
                            "description" : about_text
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
