from __future__ import annotations
from urllib.parse import urljoin
from apify import Actor, Request
from playwright.async_api import async_playwright

async def main() -> None:

    async with Actor:
        # retruve actor's input
        actor_input = await Actor.get_input() or {}
        job_role = actor_input.get('job_role', "Java Developer")
        role_query = job_role.replace(" ", "%20")
        start_url = f"https://in.linkedin.com/jobs/search?keywords={role_query}"

        # if job role is empty
        if not job_role:
            Actor.log.info('No Job role specified in Actor input, exiting...')
            await Actor.exit()

        request_queue = await Actor.open_request_queue()

        # Enqueue the start URLs with an initial crawl depth of 0.
        Actor.log.info('Launching Playwright...')

        start_url = f"https://in.linkedin.com/jobs/search?keywords={role_query}"
        new_request = Request.from_url(start_url, user_data={'depth': 0})
        await request_queue.add_request(new_request)
   
        total_jobs = actor_input.get('total_jobs_to_scrape',20)
        count = 0
        stop_scrapping = False

        async with async_playwright() as playwright:
            proxy_configuration  = await Actor.create_proxy_configuration(
                groups = ["RESIDENTIAL"]
            )      

            browser = await playwright.chromium.launch(headless = False)

            context = await browser.new_context(
                proxy = {
                    "server":proxy_configuration.new_url()
                }
            )

            while not stop_scrapping and (request := await request_queue.fetch_next_request()):
                url = request.url

                if not isinstance(request.user_data['depth'], (str, int)):
                    raise TypeError('Request.depth is an unexpected type.')

                depth = int(request.user_data['depth'])
                Actor.log.info(f'Scraping {url} (depth={depth}) ...')

                try:
                    # Open a new page in the browser context and navigate to the URL.
                    page = await context.new_page()
                    await page.goto(url)
                    
                    ip = await page.text_content("body")
                    print("Current IP:", ip)

                    try:
                        await page.locator("button[aria-label='Dismiss']").first.click(timeout=2000)
                    except:
                        pass

                    if depth == 0:
                        jobs_links = await page.locator(".base-card__full-link").all()

                        for job in jobs_links:
                            link_href = await job.get_attribute('href')
                            # link_url = urljoin(url, link_href)

                            new_request = Request.from_url(
                                link_href,
                                user_data={'depth': 1}
                            )
                            await request_queue.add_request(new_request)

                    elif depth == 1:
                        job_role = await page.locator("h1.topcard__title").inner_text()
                        company = await page.locator(".topcard__org-name-link").inner_text()
                        location = await page.locator(".topcard__flavor--bullet").first.inner_text()
                        apply_link = page.url  # best fallback (real apply needs login)
                        app_starting_date = await page.locator(".posted-time-ago__text").inner_text()

                        criteria = page.locator(".description__job-criteria-item")
                        seniority = ""
                        employment_type = ""
                        job_function = ""
                        industries = ""

                        count_criterias = await criteria.count()

                        for i in range(count_criterias):
                            item = criteria.nth(i)

                            key = await item.locator("h3").inner_text()
                            value = await item.locator("span").inner_text()

                            if "Seniority level" in key:
                                seniority = value
                            elif "Employment type" in key:
                                employment_type = value
                            elif "Job function" in key:
                                job_function = value
                            elif "Industries" in key:
                                industries = value

                        data = {
                            "job_role": job_role,
                            "company": company,
                            "location": location,
                            "apply_link": apply_link,
                            "application_started_date": app_starting_date,
                            "seniority_level": seniority,
                            "employment_type": employment_type,
                            "job_function": job_function,
                            "industries": industries,
                        }
                        count += 1
                        await Actor.push_data(data)

                        if (count >= total_jobs):
                            stop_scrapping = True
                  
                except Exception:
                    Actor.log.exception(f'Cannot extract data from {url}.')

                finally:
                    await page.close()
                    await request_queue.mark_request_as_handled(request)
