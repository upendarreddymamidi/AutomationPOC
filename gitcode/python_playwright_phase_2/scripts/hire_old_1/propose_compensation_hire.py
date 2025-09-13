from ..login import login
import os
from helpers.encoding import safe_print


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

        if country in ["Japan"]:
            name = f"{row["Given Name - Western Script"]} {row["Family Name - Western Script"]}"
            compensation_button_name = f"Propose Compensation Hire: {name}"
        else:
            name = f"{row["First Name"]} {row["Last Name"]}"
            if row["Second Last Name"] != "nan":
                name += f" {row["Second Last Name"]}"
            if row["Married Last Name"] != "nan":
                name += f" {row["Married Last Name"]}"
            compensation_button_name = (
                f"Propose Compensation Hire: {name} - {row["Job Posting Title"]}"
            )

        await page.get_by_role("button", name="My Tasks Items").click()
        await expect(
            page.get_by_role("button", name=compensation_button_name).first
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name=compensation_button_name).first.click()
        await page.wait_for_timeout(3000)

        if (
            row["Compensation Package"] != "nan"
            or row["Compensation Grade"] != "nan"
            or row["Compensation Grade Profile"] != "nan"
        ):
            await expect(
                page.get_by_role("button", name="Edit Guidelines")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name="Edit Guidelines").click()
            await page.wait_for_timeout(3000)
            if row["Compensation Package"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Compensation Package"
                ).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Compensation Package"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            if row["Compensation Grade"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Compensation Grade", exact=True
                ).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Compensation Grade"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            if row["Compensation Grade Profile"] != "nan":
                await page.wait_for_timeout(3000)
                if await page.get_by_role(
                    "listbox", name="items selected for Compensation Grade Profile"
                ).is_visible():
                    await page.get_by_role(
                        "listbox", name="items selected for Compensation Grade Profile"
                    ).click()
                else:
                    await page.get_by_role(
                        "textbox", name="Compensation Grade Profile"
                    ).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Compensation Grade Profile"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Guidelines").click()

        await expect(page.get_by_role("button", name="Edit Salary")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Edit Salary").click()
        await page.get_by_role("textbox", name="Amount").click()
        await page.get_by_role("textbox", name="Amount").fill(row["Salary Amount"])
        await page.get_by_role("option", name="press delete to clear").last.click()
        await page.get_by_role("textbox", name="Frequency").fill(
            row["Salary Frequency"]
        )
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Frequency").press("Enter")
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Save Salary").click()
        await page.wait_for_timeout(3000)

        # Add hour
        if (
            row["Hourly Amount"] != "nan"
            or row["Hourly Currency"] != "nan"
            or row["Hourly Frequency"] != "nan"
            or row["Hourly Compensation Plan"] != "nan"
        ):
            if await page.get_by_role("button", name="Edit Hourly").is_visible():
                await page.get_by_role("button", name="Edit Hourly").click()
            elif await page.get_by_role("button", name="Add Hourly").is_visible():
                await page.get_by_role("button", name="Add Hourly").click()
                await page.wait_for_timeout(3000)
                if row["Hourly Compensation Plan"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Hourly Compensation Plan"]
                    )
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")

            await page.wait_for_timeout(3000)

            if row["Hourly Amount"] != "nan":
                await page.get_by_role("textbox", name="Amount").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Amount").fill(
                    row["Hourly Amount"]
                )
                await page.wait_for_timeout(3000)

            if row["Hourly Currency"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Currency"
                ).locator("li").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Hourly Currency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Hourly Frequency"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Frequency"
                ).locator("li").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency").fill(
                    row["Hourly Frequency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

        if (
            row["Allowance Amount"] != "nan"
            or row["Allowance Currency"] != "nan"
            or row["Allowance Frequency"] != "nan"
            or row["Allowance Compensation Plan"] != "nan"
        ):
            if await page.get_by_role("button", name="Edit Allowance").is_visible():
                await page.get_by_role("button", name="Edit Allowance").click()
            elif await page.get_by_role("button", name="Add Allowance").is_visible():
                await page.get_by_role("button", name="Add Allowance").click()
                await page.wait_for_timeout(3000)
                if row["Allowance Compensation Plan"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Allowance Compensation Plan"]
                    )
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")

            await page.wait_for_timeout(3000)

            if row["Allowance Amount"] != "nan":
                await page.get_by_role("textbox", name="Amount").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Amount").fill(
                    row["Allowance Amount"]
                )
                await page.wait_for_timeout(3000)

            if row["Allowance Currency"] != "nan":
                await page.get_by_role("option", name="press delete to").first.click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Allowance Currency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Allowance Frequency"] != "nan":
                await page.get_by_role("option", name="press delete to").last.click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Allowance Frequency"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)
        if (
            await page.get_by_role("button", name=compensation_button_name).is_visible()
            and await page.get_by_role("button", name="Submit").is_visible()
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
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/propose_compensation_hire_error_{idx}.png"
            )
            safe_print("Error widget appeared with errors after submission.")
            return False
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/propose_compensation_hire_confirmation_{idx}.png"
        )
        safe_print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/propose_compensation_hire_error_{idx}.png",
            full_page=True,
        )
        safe_print(error)
        return False
