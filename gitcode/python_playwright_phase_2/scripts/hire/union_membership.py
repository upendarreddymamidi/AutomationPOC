from ..login import login
import os
from helpers.encoding import safe_print


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Want to Rescind?"] == "Yes" or row["Want to correct?"] == "Yes":
        return True
    if country in ["United States of America", "Brazil"]:
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
            union_membership_button = f"Manage Union Membership for Worker:  - Hire: {row["First Name"]} {row["Last Name"]} - {row["Job Posting Title"]}"
            await expect(
                page.get_by_role("button", name=union_membership_button).first
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name=union_membership_button).first.click()
            await page.wait_for_timeout(3000)
            await expect(page.get_by_role("textbox", name="Union")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("textbox", name="Union").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Union Membership"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="OK").click()
            await page.wait_for_timeout(3000)
            await expect(page.get_by_role("spinbutton", name="Month")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("spinbutton", name="Month").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Union Seniority Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Union Seniority Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Union Seniority Date"][4:])
            await page.wait_for_timeout(3000)
            await page.get_by_role("row", name="row", exact=True).get_by_role(
                "cell"
            ).nth(1).click()

            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Start Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Start Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Start Date"][4:])
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Type").click()
            await page.wait_for_timeout(3000)
            await page.get_by_text(row["Union Type"]).click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(10000)
            error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
            if await page.is_visible(error_widget_selector) and not (
                await page.get_by_role("dialog").first.is_visible()
            ):
                await page.click(error_widget_selector)
                await page.wait_for_timeout(2000)
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/union_membership_{idx}.png"
                )
                safe_print("Error widget appeared with errors after submission.")
                return False
            await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
            await page.wait_for_timeout(3000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/union_membership_{idx}.png"
            )
            safe_print("Submission confirmation popup is visible and screenshot taken.")
            return True
        except Exception as error:
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/union_membership_{idx}.png",
                full_page=True,
            )
            safe_print(error)
            return False
    else:
        return True
