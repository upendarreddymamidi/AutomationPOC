from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    await login(page, expect, env, user_id, idx)
    try:
        await page.get_by_role("combobox", name="Search Workday").fill("Start Proxy")
        await page.keyboard.press("Enter")
        await expect(page.get_by_role("link", name="Start Proxy")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("link", name="Start Proxy").click()
        await page.get_by_role("textbox", name="User to Proxy As").click()
        await page.get_by_role("textbox", name="User to Proxy As").fill(
            "Aimbyl Ava Guillermo"
        )
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=60000)

        await page.get_by_role("button", name="My Tasks Items").click()
        probation_button_name = (
            f"Manage Probation Period: {row["First Name"]} {row["Last Name"]}"
        )
        await expect(
            page.get_by_role("button", name=probation_button_name).first
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name=probation_button_name).first.click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Submit").click()
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/add_probation_period_confirmation_{idx}.png"
        )
        print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/add_probation_period_error_{idx}.png",
            full_page=True,
        )
        print(error)  # Reraise the error after taking the screenshot
        return False
