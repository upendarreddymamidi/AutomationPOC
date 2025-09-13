from ..login import login
import os


async def error(page, expect, row, env, user_id, country, idx):
    if await page.get_by_role("button", name="Error").is_visible():
        await page.get_by_role("button", name="Error").click()
    await page.wait_for_timeout(2000)
    await page.screenshot(
        path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/Close_contract_{idx}.png"
    )
    print("Error widget appeared with errors.")
    return False


async def run_script(page, expect, row, env, user_id, country, idx):

    if "close" not in row["Why making this changes?"].lower():
        return True
    if row["Rescind"] == "Yes":
        return True
    if row["Correction"] == "Yes":
        return True

    await login(page, expect, env, user_id, idx)
    try:

        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").fill(row["WWID"])
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # Click on "Employee" link
        await expect(page.get_by_role("link", name=f"({row["WWID"]})")).to_be_visible(
            timeout=15000
        )
        await page.get_by_role("link", name=f"({row["WWID"]})").click()

        await expect(page.get_by_text("Actions").first).to_be_visible(timeout=15000)
        await page.get_by_text("Actions").first.click()
        await page.wait_for_timeout(3000)

        # Add reason
        await page.get_by_text("Job Change").hover()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Employee Contracts").first.click()
        await page.wait_for_timeout(3000)

        # Contract Details
        await expect(
            page.get_by_text("Employee Contracts", exact=True).first
        ).to_be_visible(timeout=15000)
        await page.wait_for_timeout(3000)

        # Filter Contract Type
        await page.wait_for_timeout(3000)
        start_date_locator = (
            page.get_by_role("button").filter(has_text="Contract Type").first
        )

        await start_date_locator.click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").fill(row["Contract Type"])
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(5000)

        # Filter Contract Start Date
        if row["Contract Start Date"] != "nan":
            await page.wait_for_timeout(3000)
            start_date = (
                page.get_by_role("button").filter(has_text="Contract Start Date").first
            )
            await start_date.click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("spinbutton", name="Month").click()
            await page.wait_for_timeout(3000)
            contract_start_date = row["Contract Start Date"]
            contract_start_date = contract_start_date.replace("/", "")
            await page.keyboard.type(contract_start_date[:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(contract_start_date[2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(contract_start_date[4:])
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Filter", exact=True).click()
            await page.wait_for_timeout(5000)

        # Contract End Date Filter
        if row["Contract End date"] != "nan":
            await page.wait_for_timeout(3000)
            end_date = (
                page.get_by_role("button").filter(has_text="Contract End Date").first
            )
            await end_date.click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("spinbutton", name="Month").click()
            await page.wait_for_timeout(3000)
            Contract_end_date = row["Contract End date"]
            Contract_end_date = Contract_end_date.replace("/", "")
            await page.wait_for_timeout(3000)
            await page.keyboard.type(Contract_end_date[:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(Contract_end_date[2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(Contract_end_date[4:])
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Filter", exact=True).click()
            await page.wait_for_timeout(5000)

        # Status Filter
        await page.wait_for_timeout(3000)
        status_filter = (
            page.get_by_role("button").filter(has_text="Contract Status").first
        )
        await status_filter.click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").fill("Open")
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(5000)
        await page.get_by_text("Employee Contracts", exact=True).first.click()

        # Click on Edit
        edit_button = page.get_by_role("button", name="Edit").filter(has_text="Edit")
        await edit_button.nth(1).click()

        await page.wait_for_timeout(3000)

        # Expect Edit Contract
        await expect(
            page.get_by_role("heading", name="Edit Contract").first
        ).to_be_visible(timeout=15000)
        await page.wait_for_timeout(3000)

        # effective date
        if row["Effective Date of Contract"] != "nan":
            await page.wait_for_timeout(3000)
            await page.get_by_role(
                "group", name="Effective Date current value"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            Effective_Date = row["Effective Date of Contract"]
            Effective_Date = Effective_Date.replace("/", "")
            await page.keyboard.type(Effective_Date[:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(Effective_Date[2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(Effective_Date[4:])
            await page.wait_for_timeout(3000)

        # Status

        await page.wait_for_timeout(3000)
        label_locator = page.locator('[data-automation-id="formLabel"]')
        await label_locator.get_by_text("Status").first.click()

        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Status").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Status").fill(row["Status"])
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Status").press("Enter")
        await page.wait_for_timeout(3000)

        # Employee Contract End Date
        if row["Contract End date"] != "nan":
            await page.wait_for_timeout(3000)
            Contract_end_date = row["Contract End date"]
            Contract_end_date = Contract_end_date.replace("/", "")
            await page.wait_for_timeout(3000)
            Contract_end_date_locator = page.get_by_role(
                "group", name="Contract End Date current"
            )
            await page.wait_for_timeout(3000)
            await Contract_end_date_locator.get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(Contract_end_date[:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(Contract_end_date[2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(Contract_end_date[4:])
            await page.wait_for_timeout(3000)

        # Final submit step
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(20000)

        # Wait for dialog popup (use wait_for_selector + timeout)
        try:

            # Confirm dialog visibility
            event_locator = page.locator("#bpSlimConclusionHeaderText")
            await event_locator.wait_for(state="visible", timeout=15000)
            if await event_locator.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/Close_contract_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                await page.wait_for_timeout(10000)
                return True
        except:
            # No popup, proceed to check error / alert
            pass

        # Check for alert message presence
        alert_element = await page.query_selector(
            '[data-automation-id="errorWidgetBarMessageCountCanvas"]'
        )
        alert_text = await alert_element.inner_text() if alert_element else ""
        if "Alert" in alert_text or "Alerts" in alert_text:
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(20000)

        # Wait for dialog popup (use wait_for_selector + timeout)
        try:

            event_locator = page.locator("#bpSlimConclusionHeaderText")
            await event_locator.wait_for(state="visible", timeout=15000)
            if await event_locator.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/Close_contract_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                await page.wait_for_timeout(10000)
                return True
        except:
            # No popup, proceed to check error / alert
            pass

        # Check for error message
        error_element = await page.query_selector(
            '[data-automation-id="errorWidgetBarMessageCountCanvas"]'
        )
        error_text = await error_element.inner_text() if error_element else ""

        if "Error" in error_text or "Erros" in error_text:
            await page.wait_for_timeout(5000)
            if error_element:
                await error_element.click()
                await page.wait_for_timeout(5000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/Close_contract_{idx}.png"
            )
            print("Error detected. Screenshot taken.")
            await page.wait_for_timeout(10000)
            return False

    except Exception as e:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/Close_contract_{idx}.png"
        )
        print(f"Unexpected Error: {e}")
        await page.wait_for_timeout(10000)
        return False
