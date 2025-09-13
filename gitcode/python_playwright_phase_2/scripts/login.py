import os
from dotenv import load_dotenv

load_dotenv()


async def login(page, expect, env, user_id, idx):
    # Import necessary libraries
    try:
        await page.goto(f"{os.getenv("WEBSITE_URL")}/{env.split("-")[1]}/login.htmld")

        # LOGIN
        await page.fill('input[aria-label="Username"]', os.getenv("_USERNAME"))
        await page.wait_for_timeout(1000)  # Wait for 1 second
        await page.wait_for_selector('input[aria-label="Password"]:not([disabled])')
        await page.fill('input[aria-label="Password"]', os.getenv("_PASSWORD"))
        await page.click('button[data-automation-id="goButton"]')
        await page.wait_for_timeout(3000)

        # Search Supervisory Organization
        await page.wait_for_timeout(3000)
        await expect(page.locator('input[type="search"]')).to_be_visible(timeout=60000)

    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/login_error_{idx}.png"
        )
        print(error)
        return False
