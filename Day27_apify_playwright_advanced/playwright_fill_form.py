from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless = False)

    page = browser.new_page()
    page.goto("https://techforceglobal.com/contact-us/", wait_until="domcontentloaded")

    #filling form
    page.locator("input[name = 'First Name']").fill("Yash")
    page.locator("input[name = 'Last Name']").fill("Pansuriya")
    page.locator("input[name = 'Email']").fill("yash@gmail.com")
    page.locator("input[name = 'Phone']").fill("9856324715")

    page.locator("select[name='LEADCF10']").select_option(index = 1) 
    page.locator("select[name='LEADCF9']").select_option(label = "Fintech Solution")       

    page.locator("textarea[name='Description']").fill("hi random fill")

    # page.get_by_role("button",name="submit").click()

    page.wait_for_timeout(5000)
    browser.close()

