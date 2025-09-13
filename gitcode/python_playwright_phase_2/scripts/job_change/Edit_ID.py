from ..login import login
import os
import re


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Rescind"] == "Yes":
        return True
    if row["Correction"] == "Yes":
        return True

    if "lateral" not in row["Why making this changes?"].lower():
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
        button_name = f"Edit ID: Lateral Move: {row['Full Name']}"

        # settings
        await page.get_by_role("button", name=button_name).click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Edit IDs").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Person").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Person").fill(row["WWID"])
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Person").press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(3000)
        await page.locator(".WEEG").first.click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Country").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Country").fill(
            row["Identification Country 1"]
        )
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Country").press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="National ID Type").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="National ID Type").fill(
            row["National ID Type1"]
        )
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="National ID Type").press("Enter")
        await page.wait_for_timeout(3000)
        await page.locator('input[type="text"]').click()
        await page.wait_for_timeout(3000)
        await page.locator('input[type="text"]').press("ControlOrMeta+a")
        await page.wait_for_timeout(3000)
        await page.locator('input[type="text"]').fill(row["ID value1"])
        await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(20000)
        alert_element = await page.query_selector(
            '[data-automation-id="errorWidgetBarMessageCountCanvas"]'
        )
        alert_text = await alert_element.inner_text() if alert_element else ""
        if "Alert" in alert_text or "Alerts" in alert_text:
            # Handle Alert
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(20000)

        await page.get_by_role("button", name=button_name).click()
        await page.wait_for_timeout(3000)

        # submit
        # submit
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(20000)

        # check for Alert
        alert_element = await page.query_selector(
            '[data-automation-id="errorWidgetBarMessageCountCanvas"]'
        )
        alert_text = await alert_element.inner_text() if alert_element else ""
        if "Alert" in alert_text or "Alerts" in alert_text:
            # Handle Alert
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(20000)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").first.is_visible()
        ):
            await page.wait_for_timeout(5000)
            await page.click(error_widget_selector)
            await page.wait_for_timeout(5000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_edit_ID{idx}.png"
            )
            print("Error widget appeared with errors after submission.")
            return False
        else:
            event_locator = page.locator("#bpSlimConclusionHeaderText")
            await event_locator.wait_for(state="visible", timeout=15000)

            if await event_locator.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_edit_ID{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True

    except Exception as error:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_edit_ID{idx}.png"
        )
        print(f"Error: {error}")
        return False
