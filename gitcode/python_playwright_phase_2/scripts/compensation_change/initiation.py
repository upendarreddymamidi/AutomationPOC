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
        await page.get_by_role("combobox", name="Search Workday").fill(
            "request compensation change"
        )
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await expect(
            page.get_by_role("link", name="Request Compensation Change")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("link", name="Request Compensation Change").click()
        await expect(page.get_by_role("spinbutton", name="Month")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date"][:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date"][2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date"][4:])
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Employee").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["WWID"])
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(3000)
        await expect(
            page.get_by_role("button", name="Edit Effective Date & Reason")
        ).to_be_visible(timeout=60000)

        await page.get_by_role("button", name="Edit Effective Date & Reason").click()
        await page.wait_for_timeout(3000)

        await page.get_by_role("textbox", name="Reason").fill(row["Reason"])
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date"][:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date"][2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date"][4:])
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
                await page.locator("label").filter(
                    has_text="Compensation Package"
                ).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Compensation Package"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            if row["Compensation Grade"] != "nan":
                await page.locator("label").filter(
                    has_text=re.compile(r"^Compensation Grade$")
                ).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Compensation Grade"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            if row["Compensation Grade Profile"] != "nan":
                await page.wait_for_timeout(3000)
                await page.get_by_role(
                    "textbox", name="Compensation Grade Profile"
                ).fill(row["Compensation Grade Profile"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Guidelines").click()

        if row["Want to Add Salary or Edit Salary?"] != "nan":
            if row["Want to Add Salary or Edit Salary?"] == "Add":
                await page.get_by_role("button", name="Add Salary").first.click()
                await page.wait_for_timeout(3000)
                if row["Salary Compensation Plan"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Salary Compensation Plan"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            elif row["Want to Add Salary or Edit Salary?"] == "Edit":
                await expect(
                    page.get_by_role("button", name="Edit Salary").first
                ).to_be_visible(timeout=60000)
                await page.get_by_role("button", name="Edit Salary").first.click()
                await page.wait_for_timeout(3000)

            if row["Salary Amount"] != "nan":
                await page.get_by_role("textbox", name="Amount", exact=True).fill(
                    row["Salary Amount"]
                )
                await page.wait_for_timeout(3000)

            if row["Salary Currency"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Currency"
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Salary Currency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Salary Frequency"] != "nan":
                await page.locator("label").filter(has_text="Frequency").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency").fill(
                    row["Salary Frequency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Salary").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Add Hourly or Edit Hourly?"] != "nan":
            if row["Want to Add Hourly or Edit Hourly?"] != "Add":
                await page.get_by_role("button", name="Add Hourly").click()
                await page.wait_for_timeout(3000)
                if row["Hourly Compensation Plan"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Hourly Compensation Plan"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)

            elif row["Want to Add Hourly or Edit Hourly?"] != "Edit":
                await page.get_by_role("button", name="Edit Hourly").first.click()
                await page.wait_for_timeout(3000)

            if row["Hourly Amount"] != "nan":
                await page.get_by_role("textbox", name="Amount").fill(
                    row["Hourly Amount"]
                )
                await page.wait_for_timeout(3000)

            if row["Hourly Currency"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Currency"
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Hourly Currency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Hourly Frequency"] != "nan":
                await page.locator("label").filter(has_text="Frequency").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency").fill(
                    row["Hourly Frequency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Hourly").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Edit Period Salary or Add Period Salary?"] != "nan":
            if row["Want to Edit Period Salary or Add Period Salary?"] == "Add":
                await page.get_by_role("button", name="Add Period Salary").click()
                await page.wait_for_timeout(3000)
                if row["Add Period Salary Compensation Plan"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Add Period Salary Compensation Plan"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            elif row["Want to Edit Period Salary or Add Period Salary?"] == "Edit":
                await page.get_by_text(
                    row["if Edit, which plan you want to change?"]
                ).click()
                await page.wait_for_timeout(3000)

            if row["Period Salary Actual End Date"] != "nan":
                await page.get_by_role("button", name="Additional Details").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Period Salary Actual End Date"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Period Salary Actual End Date"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Period Salary Actual End Date"][4:])

            await page.get_by_role("button", name="Save Period Salary").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Add Allowance or Edit Allowance?"] != "nan":
            if row["Want to Add Allowance or Edit Allowance?"] == "Add":
                await page.get_by_role("button", name="Add Allowance").click()
                await page.wait_for_timeout(3000)
                if row["Allowance Compensation Plan"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Allowance Compensation Plan"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            elif row["Want to Add Allowance or Edit Allowance?"] == "Edit":
                await page.get_by_text(
                    row["If Edit, which allowance plan you want to Edit?"]
                ).first.click()
                await page.wait_for_timeout(3000)
            if row["Allowance Amount"] != "nan":
                await page.get_by_role("textbox", name="Amount").fill(
                    row["Allowance Amount"]
                )
                await page.wait_for_timeout(3000)
            if row["Allowance Currency"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Currency"
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Allowance Currency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            if row["Allowance Frequency"] != "nan":
                await page.locator("label").filter(has_text="Frequency").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency").fill(
                    row["Allowance Frequency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Allowance").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Edit Merit or Add Merit?"] != "nan":
            if row["Want to Edit Merit or Add Merit?"] == "Add":
                await page.get_by_role("button", name="Add Merit").first.click()
                if row["Merit Compensation Plan"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Merit Compensation Plan"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            if row["Want to Edit Merit or Add Merit?"] == "Edit":
                await page.get_by_role("button", name="Edit Merit").first.click()
                await page.wait_for_timeout(3000)

            if row["Merit Individual Target %"] != "nan":
                await page.get_by_role("textbox", name="Individual Target %").fill(
                    row["Merit Individual Target %"]
                )
                await page.wait_for_timeout(3000)

            if row["Merit Actual End Date"] != "nan":
                await page.get_by_role("button", name="Additional Details").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Merit Actual End Date"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Merit Actual End Date"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Merit Actual End Date"][4:])
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Merit").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Edit Bonus or Add Bonus?"] != "nan":
            if row["Want to Edit Bonus or Add Bonus?"] == "Add":
                await page.get_by_role("button", name="Add Bonus").first.click()
                if row["Bonus Compensation Plan"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Bonus Compensation Plan"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            if row["Want to Edit Bonus or Add Bonus?"] == "Edit":
                await page.get_by_role("button", name="Edit Bonus").first.click()
                await page.wait_for_timeout(3000)

            if row["Bonus Individual Target %"] != "nan":
                await page.get_by_role("textbox", name="Individual Target %").fill(
                    row["Bonus Individual Target %"]
                )
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Additional Details").click()
            await page.wait_for_timeout(3000)

            if row["Bonus % Assigned"] != "nan":
                await page.get_by_role("textbox", name="% Assigned").fill(
                    row["Bonus % Assigned"]
                )
                await page.wait_for_timeout(3000)

            if row["Bonus Actual End Date"] != "nan":
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Bonus Actual End Date"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Bonus Actual End Date"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Bonus Actual End Date"][4:])
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Bonus").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Edit LTI or Add LTI?"] != "nan":
            if row["Want to Edit LTI or Add LTI?"] == "Add":
                await page.get_by_role("button", name="Add LTI").first.click()
                if row["LTI Compensation Plan"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["LTI Compensation Plan"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            if row["Want to Edit LTI or Add LTI?"] == "Edit":
                await page.get_by_role("button", name="Edit LTI").first.click()
                await page.wait_for_timeout(3000)

            if row["LTI Individual Target %"] != "nan":
                await page.get_by_role("textbox", name="Individual Target %").fill(
                    row["LTI Individual Target %"]
                )
                await page.wait_for_timeout(3000)

            if row["LTI Actual End Date"] != "nan":
                await page.get_by_role("button", name="Additional Details").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["LTI Actual End Date"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["LTI Actual End Date"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["LTI Actual End Date"][4:])
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save LTI").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Add Commission or Edit Commision?"] != "nan":
            if row["Want to Add Commission or Edit Commision?"] == "Add":
                await page.get_by_role("button", name="Add Commission").first.click()
                await page.wait_for_timeout(3000)
                if row["Commission Compensation Plan"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Commission Compensation Plan"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            elif row["Want to Add Commission or Edit Commision?"] == "Edit":
                await page.get_by_role("button", name="Edit Commission").first.click()
                await page.wait_for_timeout(3000)

            if row["Target Amount"] != "nan":
                await page.get_by_role("textbox", name="Target Amount").fill(
                    row["Target Amount"]
                )
                await page.wait_for_timeout(3000)

            if row["Commission Currency"] != "nan":
                await page.locator("label").filter(has_text="Currency").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Commission Currency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Commission Frequency"] != "nan":
                await page.locator("label").filter(
                    has_text=re.compile(r"^Frequency$")
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency", exact=True).fill(
                    row["Commission Frequency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Draw Amount"] != "nan":
                await page.get_by_role("textbox", name="Draw Amount").fill(
                    row["Draw Amount"]
                )
                await page.wait_for_timeout(3000)

            if row["Draw Frequency"] != "nan":
                await page.locator("label").filter(
                    has_text=re.compile(r"^Draw Frequency$")
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Draw Frequency").fill(
                    row["Draw Frequency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Draw Duration"] != "nan":
                await page.get_by_role("textbox", name="Draw Duration").fill(
                    row["Draw Duration"]
                )
                await page.wait_for_timeout(3000)

            if row["Change Recoverable?"] == "Yes":
                await page.locator("label").filter(has_text="Recoverable").click()
                await page.wait_for_timeout(3000)

            if row["Commission Actual End Date"] != "nan":
                await page.get_by_role("button", name="Additional Details").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Commission Actual End Date"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Commission Actual End Date"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Commission Actual End Date"][4:])
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Commission").click()
            await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)
        if await page.get_by_role("button", name="Submit").is_visible():
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(10000)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if (
            await page.is_visible(error_widget_selector)
            and not await page.get_by_role("dialog").first.is_visible()
        ):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(3000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/initiation_{idx}.png"
            )
            print("Error widget appeared with errors after submission.")
            return False

        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/initiation_{idx}.png"
        )
        print("Submission confirmation popup is visible and screenshot taken.")
        return True

    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/initiation_{idx}.png"
        )
        print(f"Error: {error}")
        return False
