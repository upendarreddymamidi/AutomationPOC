from ..login import login
import os, re


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Want to correct?"] != "Yes":
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
            timeout=60000
        )
        await page.get_by_role("link", name=f"({row["WWID"]})").click()

        await expect(page.get_by_text("Actions")).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.get_by_text("Actions").click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_text("View Worker History")).to_be_visible(
            timeout=60000
        )
        await page.get_by_text("View Worker History").click()
        await expect(page.get_by_text("View Worker History", exact=True)).to_be_visible(
            timeout=60000
        )
        await page.wait_for_timeout(3000)
        await expect(
            page.get_by_role("button", name="Status Sort and filter column")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="Status Sort and filter column").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").fill("Successfully Complete")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Effective Date Sort and").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(
            row["Effective date of the process you want to correct?"][:2]
        )
        await page.wait_for_timeout(3000)
        await page.keyboard.type(
            row["Effective date of the process you want to correct?"][2:4]
        )
        await page.wait_for_timeout(3000)
        await page.keyboard.type(
            row["Effective date of the process you want to correct?"][4:]
        )
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("link", name=f"({row["WWID"]})").filter(
            has_text=re.compile("^Compensation Change:")
        ).first.click()
        await page.wait_for_timeout(10000)
        await page.get_by_role("button", name="Related Actions").first.click()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Business Process").hover()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Correct").click()
        await expect(
            page.get_by_text("Correct Business Process", exact=True)
        ).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(3000)
        await expect(
            page.get_by_text("Correct Compensation Change", exact=True)
        ).to_be_visible(timeout=60000)

        if row["Reason - C"] != "nan" or row["Effective Date - C"] != "nan":
            await page.get_by_role(
                "button", name="Edit Effective Date & Reason"
            ).click()
            await page.wait_for_timeout(3000)
            if row["Reason - C"] != "nan":
                await page.get_by_role("textbox", name="Reason").fill(row["Reason - C"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            if row["Effective Date - C"] != "nan":
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Effective Date - C"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Effective Date - C"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Effective Date - C"][4:])
                await page.wait_for_timeout(3000)

            await page.get_by_role(
                "button", name="Save Effective Date & Reason"
            ).click()

        if (
            row["Compensation Package - C"] != "nan"
            or row["Compensation Grade - C"] != "nan"
            or row["Compensation Grade Profile - C"] != "nan"
        ):
            await expect(
                page.get_by_role("button", name="Edit Guidelines")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name="Edit Guidelines").click()
            await page.wait_for_timeout(3000)
            if row["Compensation Package - C"] != "nan":
                await page.locator("label").filter(
                    has_text="Compensation Package"
                ).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Compensation Package - C"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            if row["Compensation Grade - C"] != "nan":
                await page.locator("label").filter(
                    has_text=re.compile(r"^Compensation Grade$")
                ).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Compensation Grade - C"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            if row["Compensation Grade Profile - C"] != "nan":
                await page.wait_for_timeout(3000)
                await page.get_by_role(
                    "textbox", name="Compensation Grade Profile"
                ).fill(row["Compensation Grade Profile - C"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Guidelines").click()

        if row["Want to Add Salary or Edit Salary? - C"] != "nan":
            if row["Want to Add Salary or Edit Salary? - C"] == "Add":
                await page.get_by_role("button", name="Add Salary").first.click()
                await page.wait_for_timeout(3000)
                if row["Salary Compensation Plan - C"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Salary Compensation Plan - C"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            elif row["Want to Add Salary or Edit Salary? - C"] == "Edit":
                await expect(
                    page.get_by_role("button", name="Edit Salary").first
                ).to_be_visible(timeout=60000)
                await page.get_by_role("button", name="Edit Salary").first.click()
                await page.wait_for_timeout(3000)

            if row["Salary Amount - C"] != "nan":
                await page.get_by_role("textbox", name="Amount", exact=True).fill(
                    row["Salary Amount - C"]
                )
                await page.wait_for_timeout(3000)

            if row["Salary Currency - C"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Currency"
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Salary Currency - C"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Salary Frequency - C"] != "nan":
                await page.locator("label").filter(has_text="Frequency").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency").fill(
                    row["Salary Frequency - C"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Salary").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Add Hourly or Edit Hourly? - C"] != "nan":
            if row["Want to Add Hourly or Edit Hourly? - C"] != "Add":
                await page.get_by_role("button", name="Add Hourly").click()
                await page.wait_for_timeout(3000)
                if row["Hourly Compensation Plan - C"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Hourly Compensation Plan - C"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)

            elif row["Want to Add Hourly or Edit Hourly? - C"] != "Edit":
                await page.get_by_role("button", name="Edit Hourly").first.click()
                await page.wait_for_timeout(3000)

            if row["Hourly Amount - C"] != "nan":
                await page.get_by_role("textbox", name="Amount").fill(
                    row["Hourly Amount - C"]
                )
                await page.wait_for_timeout(3000)

            if row["Hourly Currency - C"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Currency"
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Hourly Currency - C"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Hourly Frequency - C"] != "nan":
                await page.locator("label").filter(has_text="Frequency").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency").fill(
                    row["Hourly Frequency - C"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Hourly").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Edit Period Salary or Add Period Salary? - C"] != "nan":
            if row["Want to Edit Period Salary or Add Period Salary? - C"] == "Add":
                await page.get_by_role("button", name="Add Period Salary").click()
                await page.wait_for_timeout(3000)
                if row["Add Period Salary Compensation Plan - C"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Add Period Salary Compensation Plan - C"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            elif row["Want to Edit Period Salary or Add Period Salary? - C"] == "Edit":
                await page.get_by_text(
                    row["if Edit, which plan you want to change? - C"]
                ).click()
                await page.wait_for_timeout(3000)

            if row["Period Salary Actual End Date - C"] != "nan":
                await page.get_by_role("button", name="Additional Details").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Period Salary Actual End Date - C"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Period Salary Actual End Date - C"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Period Salary Actual End Date - C"][4:])

            await page.get_by_role("button", name="Save Period Salary").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Add Allowance or Edit Allowance? - C"] != "nan":
            if row["Want to Add Allowance or Edit Allowance? - C"] == "Add":
                await page.get_by_role("button", name="Add Allowance").click()
                await page.wait_for_timeout(3000)
                if row["Allowance Compensation Plan - C"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Allowance Compensation Plan - C"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            elif row["Want to Add Allowance or Edit Allowance? - C"] == "Edit":
                await page.get_by_text(
                    row["If Edit, which allowance plan you want to edit? - C"]
                ).click()
                await page.wait_for_timeout(3000)
            if row["Allowance Amount - C"] != "nan":
                await page.get_by_role("textbox", name="Amount").fill(
                    row["Allowance Amount - C"]
                )
                await page.wait_for_timeout(3000)
            if row["Allowance Currency - C"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Currency"
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Allowance Currency - C"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            if row["Allowance Frequency - C"] != "nan":
                await page.locator("label").filter(has_text="Frequency").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency").fill(
                    row["Allowance Frequency - C"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Allowance").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Edit Merit or Add Merit? - C"] != "nan":
            if row["Want to Edit Merit or Add Merit? - C"] == "Add":
                await page.get_by_role("button", name="Add Merit").first.click()
                if row["Merit Compensation Plan - C"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Merit Compensation Plan - C"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            if row["Want to Edit Merit or Add Merit? - C"] == "Edit":
                await page.get_by_role("button", name="Edit Merit").first.click()
                await page.wait_for_timeout(3000)

            if row["Merit Individual Target % - C"] != "nan":
                await page.get_by_role("textbox", name="Individual Target %").fill(
                    row["Merit Individual Target % - C"]
                )
                await page.wait_for_timeout(3000)

            if row["Merit Actual End Date - C"] != "nan":
                await page.get_by_role("button", name="Additional Details").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Merit Actual End Date - C"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Merit Actual End Date - C"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Merit Actual End Date - C"][4:])
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Merit").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Edit Bonus or Add Bonus? - C"] != "nan":
            if row["Want to Edit Bonus or Add Bonus? - C"] == "Add":
                await page.get_by_role("button", name="Add Bonus").first.click()
                if row["Bonus Compensation Plan - C"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Bonus Compensation Plan - C"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            if row["Want to Edit Bonus or Add Bonus? - C"] == "Edit":
                await page.get_by_role("button", name="Edit Bonus").first.click()
                await page.wait_for_timeout(3000)

            if row["Bonus Individual Target % - C"] != "nan":
                await page.get_by_role("textbox", name="Individual Target %").fill(
                    row["Bonus Individual Target % - C"]
                )
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Additional Details").click()
            await page.wait_for_timeout(3000)

            if row["Bonus % Assigned - C"] != "nan":
                await page.get_by_role("textbox", name="% Assigned").fill(
                    row["Bonus % Assigned - C"]
                )
                await page.wait_for_timeout(3000)

            if row["Bonus Actual End Date - C"] != "nan":
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Bonus Actual End Date - C"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Bonus Actual End Date - C"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Bonus Actual End Date - C"][4:])
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Bonus").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Edit LTI or Add LTI? - C"] != "nan":
            if row["Want to Edit LTI or Add LTI? - C"] == "Add":
                await page.get_by_role("button", name="Add LTI").first.click()
                if row["LTI Compensation Plan - C"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["LTI Compensation Plan - C"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            if row["Want to Edit LTI or Add LTI? - C"] == "Edit":
                await page.get_by_role("button", name="Edit LTI").first.click()
                await page.wait_for_timeout(3000)

            if row["LTI Individual Target % - C"] != "nan":
                await page.get_by_role("textbox", name="Individual Target %").fill(
                    row["LTI Individual Target % - C"]
                )
                await page.wait_for_timeout(3000)

            if row["LTI Actual End Date - C"] != "nan":
                await page.get_by_role("button", name="Additional Details").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["LTI Actual End Date - C"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["LTI Actual End Date - C"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["LTI Actual End Date - C"][4:])
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save LTI").first.click()
            await page.wait_for_timeout(3000)

        if row["Want to Add Commission or Edit Commision? - C"] != "nan":
            if row["Want to Add Commission or Edit Commision? - C"] == "Add":
                await page.get_by_role("button", name="Add Commission").first.click()
                await page.wait_for_timeout(3000)
                if row["Commission Compensation Plan - C"] != "nan":
                    await page.get_by_role("textbox", name="Compensation Plan").fill(
                        row["Commission Compensation Plan - C"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
            elif row["Want to Add Commission or Edit Commision? - C"] == "Edit":
                await page.get_by_role("button", name="Edit Commission").first.click()
                await page.wait_for_timeout(3000)

            if row["Target Amount - C"] != "nan":
                await page.get_by_role("textbox", name="Target Amount").fill(
                    row["Target Amount - C"]
                )
                await page.wait_for_timeout(3000)

            if row["Commission Currency - C"] != "nan":
                await page.locator("label").filter(has_text="Currency").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Commission Currency - C"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Commission Frequency - C"] != "nan":
                await page.locator("label").filter(
                    has_text=re.compile(r"^Frequency$")
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency", exact=True).fill(
                    row["Commission Frequency - C"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Draw Amount - C"] != "nan":
                await page.get_by_role("textbox", name="Draw Amount").fill(
                    row["Draw Amount - C"]
                )
                await page.wait_for_timeout(3000)

            if row["Draw Frequency - C"] != "nan":
                await page.locator("label").filter(
                    has_text=re.compile(r"^Draw Frequency$")
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Draw Frequency").fill(
                    row["Draw Frequency - C"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Draw Duration - C"] != "nan":
                await page.get_by_role("textbox", name="Draw Duration").fill(
                    row["Draw Duration - C"]
                )
                await page.wait_for_timeout(3000)

            if row["Change Recoverable? - C"] == "Yes":
                await page.locator("label").filter(has_text="Recoverable").click()
                await page.wait_for_timeout(3000)

            if row["Commission Actual End Date - C"] != "nan":
                await page.get_by_role("button", name="Additional Details").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Commission Actual End Date - C"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Commission Actual End Date - C"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Commission Actual End Date - C"][4:])
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Commission").click()
            await page.wait_for_timeout(3000)

        await page.get_by_role("textbox", name="enter your comment").fill(
            row["Comment for correction"]
        )

        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)
        if await page.get_by_role("button", name="Submit").is_visible():
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(10000)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(3000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/correction_{idx}.png"
            )
            print("Error widget appeared with errors after submission.")
            return False

        popup_header_selector = page.get_by_role("dialog").first
        if await popup_header_selector.is_visible():
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/correction_{idx}.png"
            )
            print("Submission confirmation popup is visible and screenshot taken.")
            return True

    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/correction_{idx}.png"
        )
        print(f"Error: {error}")
        return False
