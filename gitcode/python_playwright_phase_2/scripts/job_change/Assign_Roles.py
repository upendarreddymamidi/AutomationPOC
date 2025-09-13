from ..login import login
import os
import re


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Rescind"] == "Yes":
        return True
    if row["Correction"] == "Yes":
        return True
    if row["Different Country Lateral Move"] != "Yes":
        return True

    await login(page, expect, env, user_id, idx)
    try:

        # Approval by manager
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").fill("start proxy")
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("link", name="Start Proxy").click()

        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="User to Proxy As").fill(
            "Aimbyl Ava Guillermo"
        )
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="User to Proxy As").press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()

        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=15000)
        await page.get_by_role("button", name="My Tasks Items").click()
        await page.wait_for_timeout(3000)

        # Extract the word before colon in `Why making this changes?`
        process = "Assign Roles for"

        # Find the button with full WWID and static word before colon

        button = page.get_by_text(f"{row['WWID']}").filter(has_text=process)
        await button.click()
        await page.wait_for_timeout(5000)

        # settings
        await page.get_by_role("radio", name="Remove role assignments").check()
        await page.wait_for_timeout(3000)

        # submit
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(10000)

        # if row enabled
        remove_row = page.locator(
            '[data-automation-id="icon"]:has(.wd-icon-minus)'
        ).first
        if await remove_row.is_visible():
            await page.wait_for_timeout(3000)
            await remove_row.click()
            await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)

        event_locator = page.locator("#bpSlimConclusionHeaderText")
        await event_locator.wait_for(state="visible", timeout=15000)

        if await event_locator.is_visible():
            await page.wait_for_timeout(5000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_Assign_Roles_{idx}.png"
            )
            print("Submission confirmation popup is visible and screenshot taken.")
            return True

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").first.is_visible()
        ):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(5000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_Assign_Roles_{idx}.png"
            )
            print("Error widget appeared with errors after submission.")
            return False
        else:
            await page.wait_for_timeout(10000)
            popup_header_selector = page.get_by_role("dialog").first

            if await popup_header_selector.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_Assign_Roles_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")

                return True
    except Exception as error:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_Assign_Roles_{idx}.png"
        )
        print(f"Error: {error}")
        return False
