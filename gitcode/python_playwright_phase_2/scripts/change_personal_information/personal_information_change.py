from ..login import login
import os

dummmy_file_path = os.getenv("DUMMY_DOCUMENT")


async def run_change_preference(page, expect, row, user_id, country, idx):
    try:
        await page.get_by_text("Actions").click()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Start Proxy").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(3000)
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="Profile On behalf of").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("menuitem", name="My Account").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("menuitem", name="Change Preferences").click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_role("button", name="Preferred Locale")).to_be_visible(
            timeout=60000
        )
        if row["Preferred Locale"] != "nan":
            await page.get_by_role("button", name="Preferred Locale").click()
            await page.wait_for_timeout(3000)
            await page.get_by_label(row["Preferred Locale"]).last.click()
            await page.wait_for_timeout(3000)
        if row["Preferred Display Language"] != "nan":
            await page.get_by_role("button", name="Preferred Display Language").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role(
                "listbox", name="Preferred Display Language"
            ).get_by_label(row["Preferred Display Language"]).click()
            await page.wait_for_timeout(3000)
        if row["Change Show Month/Day Names in Preferred Language?"] == "Yes":
            if (
                await page.locator("label")
                .filter(has_text="Show Month/Day Names in")
                .is_visible()
            ):
                await page.locator("label").filter(
                    has_text="Show Month/Day Names in"
                ).click()
            if await page.get_by_text(
                "Show Month/Day Names in Preferred Language"
            ).last.is_visible():
                await page.get_by_text(
                    "Show Month/Day Names in Preferred Language"
                ).last.click()
            await page.wait_for_timeout(3000)
        if row["Preferred Hour Clock"] != "nan":
            await page.get_by_role("button", name="Preferred Hour Clock").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("option", name=row["Preferred Hour Clock"]).click()
            await page.wait_for_timeout(3000)
        if row["Preferred Currency"] != "nan":
            await page.get_by_text("Preferred Currency").first.click()
            await page.get_by_role("textbox", name="Preferred Currency").fill(
                row["Preferred Currency"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
        if row["Workday Search Provider"] != "nan":
            await page.locator("label").filter(
                has_text="Workday Search Provider"
            ).click()
            await page.wait_for_timeout(3000)
            await page.get_by_role(
                "option", name=row["Workday Search Provider"]
            ).get_by_role("radio").click()
            await page.wait_for_timeout(3000)
        if row["Preferred Home Page"] != "nan":
            await page.locator("label").filter(has_text="Preferred Home Page").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Preferred Home Page").fill(
                row["Preferred Home Page"]
            )
            await page.wait_for_timeout(3000)
        if row["Change Simplified View?"] == "Yes":
            await page.locator("label").filter(has_text="Simplified View").click()
            await page.wait_for_timeout(3000)
        if row["Change Show responsive layout for prompts?"] == "Yes":
            await page.locator("label").filter(
                has_text="Show responsive layout for"
            ).click()
            await page.wait_for_timeout(3000)
        if row["Change Suppress My Tasks Exceptions?"] == "Yes":
            await page.locator("label").filter(
                has_text="Suppress My Tasks Exceptions"
            ).click()
            await page.wait_for_timeout(3000)
        if (
            row["Change Opt Out of Absence Third-Party Calendar Integration Events?"]
            == "Yes"
        ):
            await page.get_by_text(
                "Opt Out of Absence Third-Party Calendar Integration Events"
            ).first.click()
            await page.wait_for_timeout(3000)
        if row["Change Display a message when a background report completes?"] == "Yes":
            await page.locator("label").filter(
                has_text="Display a message when a background report completes"
            ).click()
            await page.wait_for_timeout(3000)
        if (
            row["Change Display a message when a shared background report completes?"]
            == "Yes"
        ):
            await page.locator("label").filter(
                has_text="Display a message when a shared background report completes"
            ).click()
            await page.wait_for_timeout(3000)
        if row["Approvals Frequency"] != "nan":
            await page.get_by_text("Frequency").nth(0).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Approvals Frequency"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
        if row["Custom Business Process Notifications Frequency"] != "nan":
            await page.get_by_text("Frequency").nth(2).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(
                row["Custom Business Process Notifications Frequency"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
        if row["Tasks Frequency"] != "nan":
            await page.get_by_text("Frequency").nth(4).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Tasks Frequency"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
        if row["To-Dos Frequency"] != "nan":
            await page.get_by_text("Frequency").nth(6).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["To-Dos Frequency"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
        if row["Give Feedback Frequency"] != "nan":
            await page.get_by_text("Frequency").nth(8).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Give Feedback Frequency"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
        if row["Surveys Frequency"] != "nan":
            await page.get_by_text("Frequency").nth(10).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Surveys Frequency"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
        if row["HCM Give Feedback Frequency"] != "nan":
            await page.get_by_label("navigation pane").get_by_text(
                "Mobile Push Notification"
            ).click()
            await page.wait_for_timeout(3000)
            await page.get_by_text("Frequency").first.click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["HCM Give Feedback Frequency"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK", exact=True).click()
        await page.wait_for_timeout(10000)
        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/personal_info_change_{idx}.png"
            )
            print("Widget error")
            return False
        await expect(page.get_by_role("button", name="Done")).to_be_visible(
            timeout=60000
        )
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/personal_info_change_{idx}.png"
        )
        print("Submission confirmation popup is visible and screenshot taken.")
        await page.get_by_role("button", name="Done").click()
        await page.wait_for_timeout(10000)
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/personal_info_change_{idx}.png",
            full_page=True,
        )
        print(error)  # Reraise the error after taking the screenshot
        return False


async def run_script(page, expect, row, env, user_id, country, idx):
    await login(page, expect, env, user_id, idx)
    try:

        if row["What Change you want to make?"] == "Name":
            await expect(
                page.get_by_role("heading", name="Awaiting Your Action")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("combobox", name="Search Workday").fill(
                "Start Proxy"
            )
            await page.keyboard.press("Enter")
            await expect(page.get_by_role("link", name="Start Proxy")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("link", name="Start Proxy").click()
            await page.get_by_role("textbox", name="User to Proxy As").click()
            await page.get_by_role("textbox", name="User to Proxy As").fill(row["WWID"])
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="OK").click()
            await expect(
                page.get_by_role("heading", name="Awaiting Your Action")
            ).to_be_visible(timeout=60000)

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
        await page.wait_for_timeout(3000)

        if row["What Change you want to make?"] == "Change Preferences":
            return await run_change_preference(page, expect, row, user_id, country, idx)

        if await page.get_by_text("More").first.is_visible():
            await page.get_by_text("More").first.click()
            await page.wait_for_timeout(3000)

        if row["What Change you want to make?"] == "Bank Details":
            await page.get_by_role("link", name="Pay").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("tab", name="Payment Elections").click()
            await page.wait_for_timeout(3000)
            if row["Add Bank Account?"] == "Yes":
                await page.wait_for_timeout(3000)
                if await page.get_by_role("button", name="Add").first.is_visible():
                    await page.get_by_role("button", name="Add").first.click()
                await page.wait_for_timeout(3000)
                await expect(
                    page.get_by_role("textbox", name="Account Number")
                ).to_be_visible(timeout=60000)
                if row["Account Type"] != "nan":
                    await page.get_by_role("radio", name=row["Account Type"]).click()
                    await page.wait_for_timeout(3000)

                if country in ["Mexico"]:
                    if row["Routing Transit Number"] != "nan":
                        await page.get_by_role(
                            "textbox", name="Routing Transit Number"
                        ).fill(row["Routing Transit Number"].strip('"'))

                if country in ["Costa Rica"]:
                    if row["Bank Code"] != "nan":
                        await page.locator("label").filter(has_text="Bank Code").click()
                        await page.wait_for_timeout(3000)
                        await page.get_by_role("textbox", name="Bank Code").fill(
                            row["Bank Code"].strip('"')
                        )
                        await page.wait_for_timeout(3000)
                        await page.keyboard.press("Enter")
                        await page.wait_for_timeout(3000)

                if row["Account Number"] != "nan":
                    await page.get_by_role("textbox", name="Account Number").fill(
                        row["Account Number"].strip('"')
                    )
                if row["Bank Name"] != "nan":
                    await page.locator("label").filter(has_text="Bank Name").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Bank Name").fill(
                        row["Bank Name"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)

                if row["Branch ID"] != "nan":
                    if country in ["Mexico"]:
                        await page.get_by_role("textbox", name="Branch ID").fill(
                            row["Branch ID"].strip('"')
                        )
                    if country in ["Costa Rica"]:
                        await page.get_by_role("textbox", name="Branch Code").fill(
                            row["Branch ID"].strip('"')
                        )
                if row["Branch Name"] != "nan":
                    await page.get_by_role("textbox", name="Branch Name").fill(
                        row["Branch Name"]
                    )

                if row["Bank Identification Code"] != "nan":
                    if country in ["Costa Rica"]:
                        await page.get_by_role(
                            "listbox",
                            name="items selected for Bank Identification Code",
                        ).click()
                        await page.wait_for_timeout(3000)
                        await page.get_by_role(
                            "textbox", name="Bank Identification Code"
                        ).fill(row["Bank Identification Code"].strip('"'))
                        await page.wait_for_timeout(3000)
                        await page.keyboard.press("Enter")
                        await page.wait_for_timeout(3000)
                    if country in ["Mexico"]:
                        await page.get_by_role(
                            "textbox", name="Bank Identification Code"
                        ).fill(row["Bank Identification Code"].strip('"'))

                if country in ["Mexico"]:
                    if row["Check Digit"] != "nan":
                        await page.get_by_role("textbox", name="Check Digit").fill(
                            row["Check Digit"].strip('"')
                        )
                if country in ["Mexico"]:
                    if row["Roll Number"] != "nan":
                        await page.get_by_role("textbox", name="Roll Number").fill(
                            row["Roll Number"].strip('"')
                        )
                if row["IBAN"] != "nan":
                    await page.get_by_role("textbox", name="IBAN").fill(
                        row["IBAN"].strip('"')
                    )
                if row["Name On Account"] != "nan":
                    await page.get_by_role("textbox", name="Name On Account").fill(
                        row["Name On Account"]
                    )
                if row["Account Nickname (optional)"] != "nan":
                    await page.get_by_role(
                        "textbox", name="Account Nickname (optional)"
                    ).fill(row["Account Nickname (optional)"])
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="OK", exact=True).click()

            if row["Edit Bank Account?"] == "Yes":
                await page.get_by_role(
                    "button", name=f"Edit {row["Account Nickname"]}"
                ).click()
                await page.wait_for_timeout(3000)
                await expect(
                    page.get_by_role("textbox", name="Account Number")
                ).to_be_visible(timeout=60000)
                if row["New Account Type"] != "nan":
                    await page.get_by_role(
                        "radio", name=row["New Account Type"]
                    ).click()
                    await page.wait_for_timeout(3000)

                if country in ["Mexico"]:
                    if row["New Routing Transit Number"] != "nan":
                        await page.get_by_role(
                            "textbox", name="Routing Transit Number"
                        ).fill(row["New Routing Transit Number"].strip('"'))

                if country in ["Costa Rica"]:
                    if row["New Bank Code"] != "nan":
                        await page.get_by_role("textbox", name="Bank Code").fill(
                            row["New Bank Code"].strip('"')
                        )
                        await page.wait_for_timeout(3000)
                        await page.keyboard.press("Enter")
                        await page.wait_for_timeout(3000)

                if row["New Account Number"] != "nan":
                    await page.get_by_role("textbox", name="Account Number").fill(
                        row["New Account Number"].strip('"')
                    )
                if row["New Bank Name"] != "nan":
                    await page.locator("label").filter(has_text="Bank Name").click()

                    await page.get_by_role("textbox", name="Bank Name").fill(
                        row["New Bank Name"]
                    )

                if row["New Branch ID"] != "nan":
                    if country in ["Mexico"]:
                        await page.get_by_role("textbox", name="Branch ID").fill(
                            row["New Branch ID"].strip('"')
                        )
                    if country in ["Costa Rica"]:
                        await page.get_by_role("textbox", name="Branch Code").fill(
                            row["New Branch ID"].strip('"')
                        )
                if row["New Branch Name"] != "nan":
                    await page.get_by_role("textbox", name="Branch Name").fill(
                        row["New Branch Name"]
                    )

                if row["New Bank Identification Code"] != "nan":
                    if country in ["Costa Rica"]:
                        await page.get_by_role(
                            "listbox",
                            name="items selected for Bank Identification Code",
                        ).click()
                        await page.wait_for_timeout(3000)
                        await page.get_by_role(
                            "textbox", name="Bank Identification Code"
                        ).fill(row["New Bank Identification Code"].strip('"'))
                        await page.wait_for_timeout(3000)
                        await page.keyboard.press("Enter")
                        await page.wait_for_timeout(3000)
                    if country in ["Mexico"]:
                        await page.get_by_role(
                            "textbox", name="Bank Identification Code"
                        ).fill(row["New Bank Identification Code"].strip('"'))

                if country in ["Mexico"]:
                    if row["New Check Digit"] != "nan":
                        await page.get_by_role("textbox", name="Check Digit").fill(
                            row["New Check Digit"].strip('"')
                        )
                if country in ["Mexico"]:
                    if row["New Roll Number"] != "nan":
                        await page.get_by_role("textbox", name="Roll Number").fill(
                            row["New Roll Number"].strip('"')
                        )
                if row["New IBAN"] != "nan":
                    await page.get_by_role("textbox", name="IBAN").fill(
                        row["New IBAN"].strip('"')
                    )
                if row["New Name On Account"] != "nan":
                    await page.get_by_role("textbox", name="Name On Account").fill(
                        row["New Name On Account"]
                    )
                if row["New Account Nickname (optional)"] != "nan":
                    await page.get_by_role(
                        "textbox", name="Account Nickname (optional)"
                    ).fill(row["New Account Nickname (optional)"])
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="OK", exact=True).click()
            await page.wait_for_timeout(10000)
            error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
            if await page.is_visible(error_widget_selector):
                await page.click(error_widget_selector)
                await page.wait_for_timeout(2000)
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/personal_info_change_{idx}.png"
                )
                print("Widget error")
                return False
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/personal_info_change_{idx}.png"
            )
            print("Submission confirmation popup is visible and screenshot taken.")
            return True

        if row["What Change you want to make?"] == "Name":
            await expect(page.get_by_role("link", name="Personal")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("link", name="Personal").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("tab", name="Names").click()
            await page.wait_for_timeout(3000)
            await page.get_by_text("Edit").nth(1).click()
            await page.wait_for_timeout(3000)
            await expect(page.get_by_text("Edit Legal Name", exact=True)).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("spinbutton", name="Month").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Effective Date for Name"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Effective Date for Name"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Effective Date for Name"][4:])
            await page.wait_for_timeout(3000)

            if country in ["Mexico"]:
                if row["New First Name"] != "nan":
                    await page.get_by_role("textbox", name="Given Name(s)").fill(
                        row["New First Name"]
                    )
            if country in ["Mexico"]:
                if row["New Last Name"] != "nan":
                    await page.get_by_role("textbox", name="Father's Family Name").fill(
                        row["New Last Name"]
                    )
            if country in ["Costa Rica"]:
                if row["New First Name"] != "nan":
                    await page.get_by_role("textbox", name="First Name").fill(
                        row["New First Name"]
                    )
            if country in ["Costa Rica"]:
                if row["New Last Name"] != "nan":
                    await page.get_by_role("textbox", name="First Last Name").fill(
                        row["New Last Name"]
                    )
            if country in ["Costa Rica"]:
                if row["New Second Last Name"] != "nan":
                    await page.get_by_role("textbox", name="Second Last Name").fill(
                        row["New Second Last Name"]
                    )
            if country in ["Costa Rica"]:
                if row["New Married Last Name"] != "nan":
                    await page.get_by_role("textbox", name="Married Last Name").fill(
                        row["New Married Last Name"]
                    )

            await page.wait_for_timeout(10000)
            await page.set_input_files('input[type="file"]', dummmy_file_path)
            await page.wait_for_timeout(3000)

            if row["Description"] != "nan":
                await page.get_by_role("textbox", name="Description").fill(
                    row["Description"]
                )
            if row["Category"] != "nan":
                await expect(
                    page.get_by_role("textbox", name="Category")
                ).to_be_visible(timeout=60000)
                await page.get_by_role("textbox", name="Category").fill(row["Category"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            await page.get_by_text("Submit").last.click()

        if row["What Change you want to make?"] == "Personal Data":
            await expect(page.get_by_role("link", name="Personal")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("link", name="Personal").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Edit").click()
            await page.wait_for_timeout(3000)
            await expect(
                page.get_by_text("Edit Personal Information", exact=True)
            ).to_be_visible(timeout=60000)

            if row["Gender"] != "nan":
                await expect(
                    page.get_by_role("button", name="Edit Gender", exact=True)
                ).to_be_visible(timeout=60000)
                await page.get_by_role("button", name="Edit Gender", exact=True).click()
                await page.wait_for_timeout(2000)
                await page.get_by_role("button", name="Gender").first.click()
                await page.wait_for_timeout(3000)
                await page.get_by_text(row["Gender"]).last.click()
                await page.wait_for_timeout(2000)
                await page.get_by_role("button", name="Save Gender").click()

            # Edit Date of Birth
            if row["Date of Birth"] != "nan":
                await expect(
                    page.get_by_role("button", name="Edit Date of Birth")
                ).to_be_visible(timeout=60000)
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Edit Date of Birth").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("spinbutton", name="Month").first.click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Date of Birth"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Date of Birth"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Date of Birth"][4:])
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Save Date of Birth").click()
                await page.wait_for_timeout(3000)

            # if country in ["United States of America", "Brazil"]:
            #     await expect(
            #         page.get_by_role("button", name="Edit Race/Ethnicity")
            #     ).to_be_visible(timeout=60000)
            #     await page.get_by_role("button", name="Edit Race/Ethnicity").click()
            #     await expect(
            #         page.get_by_role("textbox", name="Race/Ethnicity")
            #     ).to_be_visible(timeout=60000)
            #     await page.get_by_role("textbox", name="Race/Ethnicity").click()
            #     await page.wait_for_timeout(3000)
            #     await page.keyboard.type(row["Race/Ethnicity"])
            #     await page.wait_for_timeout(3000)
            #     await page.keyboard.press("Enter")
            #     await page.wait_for_timeout(3000)
            #     await page.get_by_role("button", name="Save Race/Ethnicity").click()

            if country in ["Mexico", "Costa Rica", "Brazil"]:
                # Edit Place of Birth
                await expect(
                    page.get_by_role("button", name="Edit Place of Birth")
                ).to_be_visible(timeout=60000)
                await page.get_by_role("button", name="Edit Place of Birth").click()
                if row["Place of Birth"] != "nan":
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Place of Birth"])
                    await page.keyboard.press("Enter")

                if row["Region of Birth"] != "nan":
                    await page.wait_for_timeout(3000)
                    if (
                        await page.get_by_role("option", name="press delete")
                        .nth(1)
                        .is_visible()
                    ):
                        await page.get_by_role("option", name="press delete").nth(
                            1
                        ).click()
                    else:
                        await page.get_by_role(
                            "textbox", name="Region of Birth"
                        ).click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Region of Birth"])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")

                await page.wait_for_timeout(3000)
                if row["City of Birth"] != "nan":
                    await page.get_by_role("textbox", name="City of Birth").fill(
                        row["City of Birth"]
                    )
                await page.get_by_role("button", name="Save Place of Birth").click()

            if country in ["Mexico", "Costa Rica", "Brazil", "Japan"]:
                # Edit Marital Status
                if row["Marital status"] != "nan":
                    await expect(
                        page.get_by_role("button", name="Edit Marital Status")
                    ).to_be_visible(timeout=60000)
                    await page.get_by_role("button", name="Edit Marital Status").click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Marital status"])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(2000)
                    await page.get_by_role("button", name="Save Marital Status").click()

            # Edit Citizenship Status
            if country not in ["Japan"]:
                if row["Citizenship"] != "nan":
                    await expect(
                        page.get_by_role("button", name="Edit Citizenship Status")
                    ).to_be_visible(timeout=60000)
                    await page.get_by_role(
                        "button", name="Edit Citizenship Status"
                    ).click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("option", name="press delete to").locator(
                        "span svg"
                    ).first.click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Citizenship"])
                    await page.wait_for_timeout(5000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(5000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.get_by_role(
                        "button", name="Save Citizenship Status"
                    ).click()

            if country in ["Mexico", "Costa Rica", "Brazil", "Japan"]:
                # Edit Nationality
                if row["Nationality"] != "nan":
                    await expect(
                        page.get_by_role("button", name="Edit Nationality")
                    ).to_be_visible(timeout=60000)
                    await page.get_by_role("button", name="Edit Nationality").click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Nationality"])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("button", name="Save Nationality").click()

            # if country in ["Japan"]:
            #     await expect(
            #         page.get_by_role("button", name="Edit Gender Identity")
            #     ).to_be_visible(timeout=60000)
            #     await page.get_by_role("button", name="Edit Gender Identity").click()
            #     await page.wait_for_timeout(3000)
            #     await page.keyboard.press("Enter")
            #     await page.wait_for_timeout(3000)
            #     await page.get_by_text(row["Gender Identity"]).first.click()
            #     await page.wait_for_timeout(3000)
            #     await page.get_by_role("button", name="Save Gender Identity").click()

            # Submit
            await page.wait_for_timeout(5000)
            await expect(page.get_by_role("button", name="Submit")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("button", name="Submit").click()

        if row["What Change you want to make?"] == "IDs":
            await expect(page.get_by_role("link", name="Personal")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("link", name="Personal").click()
            await page.wait_for_timeout(3000)
            await expect(page.get_by_role("tab", name="IDs")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("tab", name="IDs").click()
            await page.wait_for_timeout(3000)
            if await page.locator("button").filter(has_text="Edit").is_visible():
                await page.locator("button").filter(has_text="Edit").click()
            elif await page.locator("button").filter(has_text="Add").is_visible():
                await page.locator("button").filter(has_text="Add").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("option", name="Edit IDs").click()
            await page.wait_for_timeout(3000)
            await expect(page.get_by_text("Edit IDs")).to_be_visible(timeout=60000)

            if row["Want to edit ID?"] == "Yes":
                await page.wait_for_timeout(3000)
                await page.locator("td").filter(has_text="*National ID Type").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Value").click()
                await page.wait_for_timeout(3000)
                await page.get_by_label("Value, Options Expanded").get_by_text(
                    row["Which ID you want to edit?"]
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Filter", exact=True).click()
                await page.wait_for_timeout(3000)
                await page.get_by_text(row["Current ID Value"].strip('"')).click()
                await page.wait_for_timeout(3000)
                if row["New ID value"] != "nan":
                    await page.locator('input[type="text"]').click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Control+A")
                    await page.keyboard.type(row["New ID value"].strip('"'))
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)

                await page.get_by_role("cell").filter(
                    has_text="current value"
                ).first.get_by_role("spinbutton", name="Month").click()
                if row["New Issued Date"] != "nan":
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["New Issued Date"][:2])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["New Issued Date"][2:4])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["New Issued Date"][4:])
                    await page.wait_for_timeout(3000)

                await page.get_by_role("cell").filter(has_text="current value").nth(
                    1
                ).get_by_role("spinbutton", name="Month").click()
                if row["New Expiration Date"] != "nan":
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["New Expiration Date"][:2])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["New Expiration Date"][2:4])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["New Expiration Date"][4:])
                    await page.wait_for_timeout(3000)

            if row["Want to add ID?"] == "Yes":
                await page.locator('[id="wd-PageContent-6$16798"]').get_by_label(
                    "Add Row"
                ).click()

                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Country").fill(
                    row["Add Country"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="National ID Type").fill(
                    row["Which ID you want to add?"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.locator('input[type="text"]').click()
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Control+A")
                await page.keyboard.type(row["Add ID value"].strip('"'))
                await page.wait_for_timeout(3000)

                await page.get_by_role("cell").filter(
                    has_text="current value"
                ).first.get_by_role("spinbutton", name="Month").click()
                if row["Add Issued Date"] != "nan":
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Add Issued Date"][:2])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Add Issued Date"][2:4])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Add Issued Date"][4:])
                    await page.wait_for_timeout(3000)

                await page.get_by_role("cell").filter(has_text="current value").nth(
                    1
                ).get_by_role("spinbutton", name="Month").click()
                if row["Add Expiration Date"] != "nan":
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Add Expiration Date"][:2])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Add Expiration Date"][2:4])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Add Expiration Date"][4:])
                    await page.wait_for_timeout(3000)

            # if row["Add Government ID"] == "Yes" or row["Edit Government ID"] == "Yes":
            #     await page.get_by_role("tab", name="Additional Government IDs").click()
            #     await page.wait_for_timeout(3000)
            #     if row["Add Government ID"] == "Yes":
            #         await page.locator("tr").filter(
            #             has_text="*Country*Government ID"
            #         ).get_by_label("Add Row")
            #         await page.wait_for_timeout(3000)
            #         await page.get_by_role("textbox", name="Country").fill(
            #             row["Government ID Country"]
            #         )
            #         await page.wait_for_timeout(3000)
            #         await page.keyboard.press("Enter")
            #         await page.wait_for_timeout(3000)
            #         await page.get_by_role("textbox", name="Government ID Type").fill(
            #             row["Govenment ID Type"]
            #         )
            #         await page.wait_for_timeout(3000)
            #         await page.keyboard.press("Enter")
            #         await page.wait_for_timeout(3000)
            #         await page.get_by_role("row", name="Government").first.locator(
            #             'input[type="text"]'
            #         ).click()
            #         await page.wait_for_timeout(3000)
            #         await page.keyboard.type(row["Government ID value"])
            #         await page.wait_for_timeout(3000)
            #         if row["ID Issue Date"] != "nan":
            #             await page.get_by_role("spinbutton", name="Month").first.click()
            #             await page.wait_for_timeout(3000)
            #             await page.keyboard.type(row["ID Issue Date"][:2])
            #             await page.wait_for_timeout(3000)
            #             await page.keyboard.type(row["ID Issue Date"][2:4])
            #             await page.wait_for_timeout(3000)
            #             await page.keyboard.type(row["ID Issue Date"][4:])
            #             await page.wait_for_timeout(3000)
            #         if row["ID Expiration Date"] != "nan":
            #             await page.get_by_role("spinbutton", name="Month").first.click()
            #             await page.wait_for_timeout(3000)
            #             await page.keyboard.type(row["ID Issue Date"][:2])
            #             await page.wait_for_timeout(3000)
            #             await page.keyboard.type(row["ID Issue Date"][2:4])
            #             await page.wait_for_timeout(3000)
            #             await page.keyboard.type(row["ID Issue Date"][4:])
            #             await page.wait_for_timeout(3000)

            if (
                row["Want to add Passport?"] == "Yes"
                or row["Want to edit Passport?"] == "Yes"
            ):
                await page.get_by_role("tab", name="Passports").click()
                await page.wait_for_timeout(3000)
                if row["Want to add Passport?"] == "Yes":
                    await page.locator("tr").filter(
                        has_text="*Country*Passport ID"
                    ).get_by_label("Add Row").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Country").fill(
                        row["Passport Country"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Passport ID Type").fill(
                        row["Passport ID Type"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    ## Identification Number
                    await page.get_by_role("table", name="Passports").locator(
                        'input[type="text"]'
                    ).click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Control+A")
                    await page.keyboard.type(row["Identification Number"].strip('"'))
                    await page.wait_for_timeout(3000)

                    await page.get_by_role("spinbutton", name="Month").nth(0).click()
                    if row["Passport Issue Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Passport Issue Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Passport Issue Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Passport Issue Date"][4:])
                        await page.wait_for_timeout(3000)
                    await page.get_by_role("spinbutton", name="Month").nth(1).click()
                    if row["Passport Expiration Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Passport Expiration Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Passport Expiration Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Passport Expiration Date"][4:])
                        await page.wait_for_timeout(3000)

                if row["Want to edit Passport?"] == "Yes":
                    await page.locator("td").filter(has_text="*Country").nth(2).click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Value").fill(
                        row["Which Country passport you want to edit?"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("button", name="Filter", exact=True).click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_text(
                        row["Current Identification Number"].strip('"')
                    ).click()
                    await page.wait_for_timeout(3000)
                    if row["New Identification Number"] != "nan":
                        await page.locator('input[type="text"]').click()
                        await page.wait_for_timeout(3000)
                        await page.keyboard.press("Control+A")
                        await page.keyboard.type(
                            row["New Identification Number"].strip('"')
                        )
                        await page.wait_for_timeout(3000)
                    await page.get_by_role(
                        "group", name="current value"
                    ).first.get_by_placeholder("MM").click()
                    if row["New Passport Issue Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Passport Issue Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Passport Issue Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Passport Issue Date"][4:])
                        await page.wait_for_timeout(3000)
                    await page.get_by_role("group", name="current value").nth(
                        1
                    ).get_by_placeholder("MM").click()
                    if row["New Passport Expiration Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(
                            row["New Passport Expiration Date"][:2]
                        )
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(
                            row["New Passport Expiration Date"][2:4]
                        )
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(
                            row["New Passport Expiration Date"][4:]
                        )
                        await page.wait_for_timeout(3000)

            if row["Want to edit Visa?"] == "Yes" or row["Want to add Visa?"] == "Yes":
                await page.get_by_role("tab", name="Visas").click()
                await page.wait_for_timeout(3000)
                if row["Want to edit Visa?"] == "Yes":
                    await page.wait_for_timeout(3000)
                    await page.get_by_text(
                        row["Current Visa ID Value"].strip('"')
                    ).click()
                    await page.wait_for_timeout(3000)
                    if row["New Visa ID value"] != "nan":
                        await page.locator('input[type="text"]').last.click()
                        await page.wait_for_timeout(3000)
                        await page.keyboard.press("Control+A")
                        await page.keyboard.type(row["New Visa ID value"].strip('"'))
                        await page.wait_for_timeout(3000)
                    await page.get_by_role(
                        "group", name="current value"
                    ).first.get_by_placeholder("MM").click()
                    if row["New Visa Issue Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Visa Issue Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Visa Issue Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Visa Issue Date"][4:])
                        await page.wait_for_timeout(3000)
                    await page.get_by_role("group", name="current value").nth(
                        1
                    ).get_by_placeholder("MM").click()
                    if row["New Visa Expiration Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Visa Expiration Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Visa Expiration Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Visa Expiration Date"][4:])
                        await page.wait_for_timeout(3000)
                if row["Want to add Visa?"] == "Yes":
                    await page.locator("tr").filter(
                        has_text="*Country*Visa ID"
                    ).get_by_label("Add Row").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Country").fill(
                        row["Visa Country"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Visa ID Type").fill(
                        row["Visa ID Type"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.locator('input[type="text"]').last.click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Visa ID value"].strip('"'))
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("spinbutton", name="Month").first.click()
                    if row["Visa Issue Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Visa Issue Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Visa Issue Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Visa Issue Date"][4:])
                        await page.wait_for_timeout(3000)
                    await page.get_by_role("spinbutton", name="Month").nth(1).click()
                    if row["Visa Expiration Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Visa Expiration Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Visa Expiration Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Visa Expiration Date"][4:])
                        await page.wait_for_timeout(3000)

            if (
                row["Want to Add license?"] == "Yes"
                or row["Want to Edit license?"] == "Yes"
            ) and await page.get_by_role("tab", name="Licenses").is_visible():
                await page.get_by_role("tab", name="Licenses").click()
                await page.wait_for_timeout(3000)
                if row["Want to Add license?"] == "Yes":
                    await page.locator("tr").filter(
                        has_text="*License ID TypeClassIssued"
                    ).get_by_label("Add Row").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role(
                        "row", name="Remove Row License ID Type", exact=True
                    ).get_by_label("License ID Type").click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["License Id Type"])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.locator('input[type="text"]').first.click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["License Class"])
                    await page.wait_for_timeout(3000)
                    await page.locator('input[type="text"]').nth(1).click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["License Id value"].strip('"'))
                    await page.wait_for_timeout(3000)
                    if row["License Issued Date"] != "nan":
                        await page.get_by_role("spinbutton", name="Month").nth(
                            0
                        ).click()
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["License Issued Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["License Issued Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["License Issued Date"][4:])
                        await page.wait_for_timeout(3000)
                    if row["License Expiration Date"] != "nan":
                        await page.get_by_role("spinbutton", name="Month").nth(
                            1
                        ).click()
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["License Expiration Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["License Expiration Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["License Expiration Date"][4:])
                        await page.wait_for_timeout(3000)
                if row["Want to Edit license?"] == "Yes":
                    await page.locator("td").filter(has_text="*License ID Type").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Value").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Value").fill(
                        row["Which license Id you want to Edit?"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Value").press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.get_by_label("Search Results, Options").get_by_text(
                        row["Which license Id you want to Edit?"]
                    ).click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("button", name="Filter", exact=True).click()
                    if await page.get_by_role(
                        "button", name="Filter", exact=True
                    ).is_visible():
                        await page.get_by_role(
                            "button", name="Filter", exact=True
                        ).click()
                        await page.wait_for_timeout(3000)
                    await page.get_by_text(
                        row["Current License Id value"].strip('"')
                    ).click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role(
                        "cell", name=row["Current License Id value"].strip('"')
                    ).get_by_role("textbox").click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Control+A")
                    await page.keyboard.type(row["New License Id value"].strip('"'))
                    await page.wait_for_timeout(3000)
                    if row["New License Class"] != "nan":
                        await page.get_by_role("textbox").nth(1).fill(
                            row["New License Class"]
                        )
                        await page.wait_for_timeout(3000)
                    if row["New License Issued Date"] != "nan":
                        await page.get_by_role("group", name="current value").nth(
                            0
                        ).get_by_placeholder("MM").click()
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New License Issued Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New License Issued Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New License Issued Date"][4:])
                        await page.wait_for_timeout(3000)
                    if row["New License Expiration Date"] != "nan":
                        await page.get_by_role("group", name="current value").nth(
                            1
                        ).get_by_placeholder("MM").click()
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New License Expiration Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(
                            row["New License Expiration Date"][2:4]
                        )
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New License Expiration Date"][4:])
                        await page.wait_for_timeout(3000)
            if (
                row["Want to edit Other IDs?"] == "Yes"
                or row["Want to add Other IDs?"] == "Yes"
            ):
                await page.get_by_role("tab", name="Other IDs").click()
                await page.wait_for_timeout(3000)
                if row["Want to edit Other IDs?"] == "Yes":
                    await page.locator("td").filter(has_text="*Other ID Type").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Value").fill(
                        row["Which ID Type you want to edit?"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("button", name="Filter", exact=True).click()
                    await page.wait_for_timeout(3000)
                    if await page.get_by_role(
                        "button", name="Filter", exact=True
                    ).is_visible():
                        await page.get_by_role(
                            "button", name="Filter", exact=True
                        ).click()
                        await page.wait_for_timeout(3000)
                    if row["New Other ID value"] != "nan":
                        await page.get_by_text(
                            row["Current Other ID Value"].strip('"')
                        ).click()
                        await page.wait_for_timeout(3000)
                        await page.keyboard.press("Control+A")
                        await page.keyboard.type(row["New Other ID value"].strip('"'))
                        await page.wait_for_timeout(3000)
                    await page.get_by_role(
                        "group", name="current value"
                    ).first.get_by_placeholder("MM").click()
                    if row["New Other ID Issue Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Other ID Issue Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Other ID Issue Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["New Other ID Issue Date"][4:])
                        await page.wait_for_timeout(3000)
                    await page.get_by_role("group", name="current value").nth(
                        1
                    ).get_by_placeholder("MM").click()
                    if row["New Other ID Expiration Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(
                            row["New Other ID Expiration Date"][:2]
                        )
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(
                            row["New Other ID Expiration Date"][2:4]
                        )
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(
                            row["New Other ID Expiration Date"][4:]
                        )
                        await page.wait_for_timeout(3000)
                if row["Want to add Other IDs?"] == "Yes":
                    await page.locator("tr").filter(has_text="*Other ID").get_by_label(
                        "Add Row"
                    ).click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("button", name="select one").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("option", name=row["Other ID Type"]).click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox").nth(2).click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Other ID Value"].strip('"'))
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("spinbutton", name="Month").first.click()
                    if row["Other ID Issue Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Other ID Issue Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Other ID Issue Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Other ID Issue Date"][4:])
                        await page.wait_for_timeout(3000)
                    await page.get_by_role("spinbutton", name="Month").nth(1).click()
                    if row["Other ID Expiration Date"] != "nan":
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Other ID Expiration Date"][:2])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Other ID Expiration Date"][2:4])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(row["Other ID Expiration Date"][4:])
                        await page.wait_for_timeout(3000)
            await page.get_by_text("Submit").last.click()

        if row["What Change you want to make?"] == "Address or Contact":
            await page.get_by_role("link", name="Contact").click()
            await page.wait_for_timeout(3000)
            await page.locator("button").filter(has_text="Edit").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("option", name="Change Home Contact").click()
            await page.wait_for_timeout(3000)
            if row["Primary Address"] == "No":
                await page.get_by_label("Address", exact=True).get_by_text(
                    "PrimaryNo"
                ).click()
                await page.wait_for_timeout(3000)
            else:
                await page.get_by_label("Address", exact=True).get_by_text(
                    "PrimaryYes"
                ).click()
                await page.wait_for_timeout(3000)
            if row["Effective Date"] != "nan":
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Effective Date"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Effective Date"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Effective Date"][4:])
                await page.wait_for_timeout(3000)
            if row["Country"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Country"
                ).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Country"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            if row["Address Line 1"] != "nan":
                await page.get_by_role("textbox", name="Address Line 1").fill(
                    row["Address Line 1"]
                )
            if row["Address Line 2"] != "nan":
                await page.get_by_role("textbox", name="Address Line 2").fill(
                    row["Address Line 2"]
                )
            if row["Neighborhood"] != "nan":
                await page.get_by_role("textbox", name="Neighborhood").fill(
                    row["Neighborhood"]
                )
            if row["Postal Code"] != "nan":
                await page.get_by_role("textbox", name="Postal Code").fill(
                    row["Postal Code"].strip('"')
                )
            if row["City"] != "nan":
                await page.get_by_role("textbox", name="City").fill(row["City"])

            if country in ["Costa Rica"]:
                if row["Province"] != "nan":
                    await page.locator("label").filter(has_text="Province").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Province").fill(
                        row["Province"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)

            if country in ["Mexico"]:
                if row["State"] != "nan":
                    await page.get_by_role("option", name="press delete to").nth(
                        1
                    ).click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["State"])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)

            if row["Usage"] != "nan":
                await page.locator("li").filter(has_text="Usage").locator(
                    "label"
                ).first.click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Usage"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Address").click()
            await page.wait_for_timeout(5000)

            if await page.get_by_role("button", name="Edit Phone").first.is_visible():
                await page.get_by_role("button", name="Edit Phone").first.click()
                await page.wait_for_timeout(3000)
                if row["Phone Type"] != "nan":
                    await page.get_by_role("button", name="Phone Type").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("option", name=row["Phone Type"]).click()
                    await page.wait_for_timeout(3000)
                if row["Country Phone Code"] != "nan":
                    await page.get_by_role(
                        "listbox", name="items selected for Country"
                    ).click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Country Phone Code"])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    if await page.get_by_text("No matches found").nth(1).is_visible():
                        await page.screenshot(
                            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/personal_info_change_{idx}.png",
                            full_page=True,
                        )
                        return False

                if row["Phone Number"] != "nan":
                    await page.get_by_role("textbox", name="Phone Number").fill(
                        row["Phone Number"].strip('"')
                    )
                if row["Phone Extension"] != "nan":
                    await page.get_by_role("textbox", name="Phone Extension").fill(
                        row["Phone Extension"]
                    )
                if row["Phone Visibilty"] != "nan":
                    await page.get_by_role("button", name="Visibility").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("listbox", name="Visibility").get_by_label(
                        row["Phone Visibilty"]
                    ).click()
                await page.get_by_role("button", name="Save Phone").click()
                await page.wait_for_timeout(5000)

            if await page.get_by_role("button", name="Edit Email").first.is_visible():
                await page.get_by_role("button", name="Edit Email").first.click()
                await page.wait_for_timeout(3000)
                if row["Email Address"] != "nan":
                    await page.get_by_role("textbox", name="Email Address").fill(
                        row["Email Address"]
                    )
                if row["Email Visibility"] != "nan":
                    await page.get_by_role("button", name="Visibility").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("listbox", name="Visibility").get_by_label(
                        row["Email Visibility"]
                    ).click()

                await page.get_by_role("button", name="Save Email").click()
                await page.wait_for_timeout(5000)

            await page.get_by_text("Submit").last.click()

        await page.wait_for_timeout(10000)
        if await page.get_by_text("Submit").last.is_visible():
            await page.get_by_text("Submit").last.click()
            await page.wait_for_timeout(10000)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/personal_info_change_{idx}.png"
            )
            print("Widget error")
            return False
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/personal_info_change_{idx}.png"
        )
        print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/personal_info_change_{idx}.png",
            full_page=True,
        )
        print(error)  # Reraise the error after taking the screenshot
        return False
