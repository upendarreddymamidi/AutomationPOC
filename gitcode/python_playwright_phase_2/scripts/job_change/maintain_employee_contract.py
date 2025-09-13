from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Rescind"] == "Yes":
        return True
    if row["Correction"] == "Yes":
        return True
    if (
        "add" in row["Why making this changes?"].lower()
        or "close" in row["Why making this changes?"].lower()
    ):
        return True
    if (
        "demotion" not in row["Why making this changes?"].lower()
        and "promotion" not in row["Why making this changes?"].lower()
        and "lateral" not in row["Why making this changes?"].lower()
        and "contract" not in row["Why making this changes?"].lower()
    ):
        return True
    if row["Different Country Lateral Move"] == "Yes":
        return True

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

        work_authorisation_name = f"Contract: {row["Full Name"]}"

        await expect(
            page.get_by_role("button", name=work_authorisation_name).first
        ).to_be_visible(timeout=15000)
        await page.get_by_role("button", name=work_authorisation_name).first.click()
        await page.wait_for_timeout(3000)

        # Fill contract page
        # Contract type
        if row["Contract Type"] != "nan":
            await page.get_by_role("textbox", name="Contract Type").fill(
                row["Contract Type"]
            )
            await page.wait_for_timeout(3000)

        # status
        if row["Status"] != "nan":
            await page.get_by_role("textbox", name="Status").fill(row["Status"])
            await page.wait_for_timeout(3000)

        # contract end date
        if row["Contract End date"] != "nan":
            contract_locator = page.get_by_role(
                "group", name="Contract End Date current"
            )
            input_element = contract_locator.get_by_placeholder("MM")
            await input_element.click()

            await page.wait_for_timeout(3000)
            contract_end_date = row["Contract End date"]
            contract_end_date = contract_end_date.replace("/", "")
            await page.keyboard.type(contract_end_date[:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(contract_end_date[2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(contract_end_date[4:])
            await page.wait_for_timeout(3000)

        # submit
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)

        popup_header_selector = page.get_by_role("dialog").first

        if await popup_header_selector.is_visible():
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_contract_{idx}.png"
            )
            print("Submission confirmation popup is visible and screenshot taken.")

            return True

        # if alert button appears
        await page.wait_for_timeout(10000)
        if await page.get_by_text("Success!").first.is_hidden():
            await page.wait_for_timeout(5000)
            await page.get_by_role("button", name="Submit").click()

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").first.is_visible()
        ):
            await page.wait_for_timeout(5000)
            await page.click(error_widget_selector)
            await page.wait_for_timeout(5000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_contract_{idx}.png"
            )
            print("Error widget appeared with errors after submission.")
            return False
        else:
            event_locator = page.locator("#bpSlimConclusionHeaderText")
            await event_locator.wait_for(state="visible", timeout=15000)

            if await event_locator.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_contract_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True
    except Exception as error:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_contract_{idx}.png"
        )
        print(f"Error: {error}")
        return False
