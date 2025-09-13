from ..login import login
import os
import re


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Rescind"] == "Yes":
        return True
    if row["Correction"] == "Yes":
        return True
    if (
        "demotion" not in row["Why making this changes?"].lower()
        and "promotion" not in row["Why making this changes?"].lower()
        and "lateral" not in row["Why making this changes?"].lower()
    ):
        return True
    await login(page, expect, env, user_id, idx)
    try:

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
        process = row["Why making this changes?"].split(":")[0]
        # Find the button with full WWID and static word before colon
        button = page.get_by_text(f"{row['WWID']}").filter(has_text=process)
        await button.click()
        await page.wait_for_timeout(3000)

        # Employee classification
        await expect(
            page.get_by_role(
                "heading", name="Mexico Employee Classification"
            ).get_by_label("Mexico Employee Classification")
        ).to_be_visible(timeout=15000)

        # submit
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)
        if (
            await page.get_by_role("button", name="Submit").is_visible()
            and await page.get_by_role("button", name=button).first.is_visible()
        ):
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(10000)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").first.is_visible()
        ):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_edit_additional_data_5{idx}.png"
            )
            print("Error widget appeared with errors after submission.")
            return False
        else:
            await page.wait_for_timeout(10000)
            popup_header_selector = page.get_by_role("dialog").first

            if await popup_header_selector.is_visible():
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_edit_additional_data_5{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")

                return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_edit_additional_data_5{idx}.png"
        )
        print(f"Error: {error}")
        return False
