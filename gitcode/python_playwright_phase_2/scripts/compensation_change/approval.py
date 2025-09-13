from ..login import login
import os, re


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Want to rescind?"] == "Yes" or row["Want to correct?"] == "Yes":
        return True
    await login(page, expect, env, user_id, idx)
    try:
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("combobox", name="Search Workday").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["WWID"])
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("link", name=f"({row["WWID"]})").click()
        await expect(page.get_by_text("Actions")).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await expect(
            page.locator("div")
            .filter(has_text=re.compile(r"^Manager"))
            .nth(1)
            .get_by_role("button", name="Related Actions")
        ).to_be_visible(timeout=60000)
        await page.locator("div").filter(has_text=re.compile(r"^Manager")).nth(
            1
        ).get_by_role("button", name="Related Actions").click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_text("Start Proxy")).to_be_visible(timeout=60000)
        await page.get_by_text("Start Proxy").click()
        await expect(page.get_by_role("button", name="OK")).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="OK").click()
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="My Tasks Items").click()
        await expect(
            page.get_by_role("button", name=f"({row["WWID"]})")
            .filter(has_text=re.compile(r"^Compensation Change:"))
            .first
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name=f"({row["WWID"]})").filter(
            has_text=re.compile(r"^Compensation Change:")
        ).first.click()
        await expect(page.get_by_role("button", name="Approve")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Approve").click()
        await page.wait_for_timeout(10000)
        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if (
            await page.is_visible(error_widget_selector)
            and not await page.get_by_role("dialog").first.is_visible()
        ):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/approval_{idx}.png"
            )
            print("Widget error")
            return False
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/approval_{idx}.png"
        )
        print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/approval_{idx}.png",
            full_page=True,
        )
        print(error)
        return False
