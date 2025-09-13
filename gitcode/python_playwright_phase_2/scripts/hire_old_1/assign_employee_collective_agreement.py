from ..login import login
import os
from helpers.encoding import safe_print

async def run_script(page, expect, row, env, user_id, country, idx):
    if country == "United States of America":
        await login(page, expect, env, user_id, idx)
        try:
            await page.get_by_role("combobox", name="Search Workday").fill(
                "Start Proxy"
            )
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
            agreement_button = f"Assign Employee Collective Agreement: {row["First Name"]} {row["Last Name"]}"
            await expect(
                page.get_by_role("button", name=agreement_button).first
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name=agreement_button).first.click()
            await page.wait_for_timeout(3000)
            await expect(page.get_by_role("button", name="Task Actions")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("button", name="Task Actions").click()
            await expect(
                page.get_by_role("menuitem", name="Skip This Task")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("menuitem", name="Skip This Task").click()
            await expect(page.get_by_text("You have opted to Skip this")).to_be_visible(
                timeout=60000
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="OK").click()
            await page.wait_for_timeout(3000)
            await expect(
                page.get_by_role("heading", name="Event skipped")
            ).to_be_visible(timeout=60000)

            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/employee_collective_agreement_{idx}.png"
            )
            safe_print("Submission confirmation popup is visible and screenshot taken.")
            return True
        except Exception as error:
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/employee_collective_agreement_{idx}.png",
                full_page=True,
            )
            safe_print(error)
            return False
    else:
        return True
