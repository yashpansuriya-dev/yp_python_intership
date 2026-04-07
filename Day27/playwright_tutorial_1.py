from playwright.sync_api import sync_playwright
import httpx
import time

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto("https://playwright.dev/")

    title = page.title()
    print(title)

    about_us = page.locator("h1.hero__title").inner_text()
    print("\nAbout us : ",about_us)
    
    more_text = page.locator(".heroSubtitle_GKHc").inner_text()
    print("More text : ",more_text)

    # testing features
    print("-"*50)
    print("Built for testing ")
    names = page.locator(".featureSectionContent_DG7g h4")
    desc = page.locator(".featureSectionContent_DG7g p")

    for i in range(0,4):
        print(f"\n {names.nth(i).inner_text()} :- ")
        print(f" {desc.nth(i).inner_text()}")

    # Built for AI Agents
    print("-"*50)
    print("Built for AI agents ")

    for i in range(4,8):
        print(f"\n {names.nth(i).inner_text()} :- ")
        print(f" {desc.nth(i).inner_text()}")
    
    # Powerful rooling
    print("-"*50)
    print("Poweful Tooling ")
    for i in range(8,11):
        print(f"\n {names.nth(i).inner_text()} :- ")
        print(f" {desc.nth(i).inner_text()}")

    page.click("a.getStarted_Sjon")
    print(page.title())

    about_playwright = page.locator(".theme-doc-markdown p").nth(0).inner_text()
    print("-"*50)
    print("Playwright is : ", about_playwright)
    page.get_by_role()

    browser.close()


# if __name__ == "__main__":
#     print("hello")