from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://quotes.toscrape.com/")

    quotes = page.locator(".quote")

    for i in range(quotes.count()):
        name = quotes.nth(i).locator(".text").inner_text()
        author_name = quotes.nth(i).locator(".author").inner_text()
        print(f" {name} - {author_name}")
