from ..login import login
import os


async def error(page, expect, row, env, user_id, country, idx):
    await page.wait_for_timeout(5000)
    if await page.get_by_role("button", name="Error").is_visible():
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
        path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_initiation_{idx}.png"
    )
    print("Error detected. Screenshot taken.")
    await page.wait_for_timeout(10000)
    return False


async def Aimbyl(page, expect, row, env, user_id, country, idx):
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


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Rescind"] == "Yes":
        return True
    if row["Correction"] == "Yes":
        return True
    print(row["Why making this changes?"].lower())

    if (
        "add" in row["Why making this changes?"].lower()
        or "close" in row["Why making this changes?"].lower()
    ):
        return True

    await login(page, expect, env, user_id, idx)
    try:
        # if lateral move proxy Aimbyl
        if "lateral" in row["Why making this changes?"].lower():
            await Aimbyl(page, expect, row, env, user_id, country, idx)

        # if not lateral move
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
        await page.get_by_text("Job Change").click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_text("Change Job", exact=True)).to_be_visible(
            timeout=15000
        )
        await page.get_by_text("Change Job", exact=True).click()
        await page.wait_for_timeout(3000)
        await expect(
            page.get_by_role("button", name="Edit Start Details")
        ).to_be_visible(timeout=30000)
        await page.get_by_role("button", name="Edit Start Details").click()
        await page.wait_for_timeout(3000)

        # effective date
        if row["Effective Date"] != "nan":
            await page.get_by_role("spinbutton", name="Month").click()
            await page.wait_for_timeout(3000)
            effective_date = row["Effective Date"]
            effective_date = effective_date.replace("/", "")
            await page.keyboard.type(effective_date[:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(effective_date[2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(effective_date[4:])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")

        # reason mandatory field
        await page.get_by_role(
            "textbox", name="Why are you making this change?"
        ).click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Why are you making this change?").fill(
            row["Why making this changes?"]
        )
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # after manager
        if row["Manager after this change?"] != "nan":
            await page.wait_for_timeout(3000)
            await page.get_by_role(
                "textbox", name="Who will be the manager after"
            ).fill(row["Manager after this change?"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

            if await page.get_by_text("No matches found").is_visible():
                await error(page, expect, row, env, user_id, country, idx)

        # team
        if row["Which team will this person be on after this change?"] != "nan":

            await page.get_by_role("textbox", name="Which team will this person").fill(
                row["Which team will this person be on after this change?"]
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Which team will this person").press(
                "Enter"
            )
            await page.wait_for_timeout(3000)
            if await page.get_by_text("No matches found").is_visible():
                await error(page, expect, row, env, user_id, country, idx)

        # where
        if row["Where this person be located after this change?"] != "nan":
            await page.get_by_role("textbox", name="Where will this person be").fill(
                row["Where this person be located after this change?"]
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Where will this person be").press(
                "Enter"
            )
            await page.wait_for_timeout(3000)
            if await page.get_by_text("No matches found").is_visible():
                await error(page, expect, row, env, user_id, country, idx)

        # save details
        await page.get_by_role("button", name="Save Start Details").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Start", exact=True).click()
        await page.wait_for_timeout(3000)
        if await page.get_by_role("button", name="Error").is_visible():
            await error(page, expect, row, env, user_id, country, idx)

        await expect(page.get_by_text("Change Job", exact=True)).to_be_visible(
            timeout=15000
        )
        await page.get_by_text("Change Job", exact=True).click()
        await page.wait_for_timeout(3000)

        # Move Tab (only if manager is changed)
        if await page.get_by_role("heading", name="Opening").is_visible():
            if row["What do you want to do with position left on your team?"] != "nan":
                await expect(page.get_by_role("heading", name="Opening")).to_be_visible(
                    timeout=30000
                )
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Edit Opening").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role(
                    "button", name="What do you want to do with"
                ).click()
                await page.wait_for_timeout(3000)
                option = row["What do you want to do with position left on your team?"]
                await page.get_by_label(option, exact=True).last.click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Save Opening").click()
                await page.wait_for_timeout(3000)

            if await page.get_by_role("button", name="Edit Move Team").is_visible():
                if row["Move Team"] != "nan":
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("button", name="Edit Move Team").click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("radio", name=row["Move Team"]).check()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("button", name="Save Move Team").click()
                    await page.wait_for_timeout(3000)

            await page.wait_for_timeout(2000)
            await page.get_by_role("button", name="Next", exact=True).click()
            await page.wait_for_timeout(2000)
            if await page.get_by_role("button", name="Error").is_visible():
                await error(page, expect, row, env, user_id, country, idx)

        # Job details
        await expect(page.get_by_text("Change Job", exact=True)).to_be_visible()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Change Job", exact=True).click()
        await page.wait_for_timeout(3000)

        if (
            row["What do you want to do with position left on your team?"]
            != "Move this headcount to the new manager"
        ):
            # Position name
            if (
                row["Position name"] != "nan"
                or row["Do you want to create a new position?"] != "nan"
                or row["Close the current position?"] != "nan"
            ):
                await page.get_by_role("button", name="Edit Position").click()
                await page.wait_for_timeout(3000)

                if row["Do you want to create a new position?"] == "Yes":
                    await page.get_by_text("Position").nth(1).click()
                    await page.wait_for_timeout(3000)
                    await page.locator(".WH3E").first.click()
                    await page.wait_for_timeout(3000)

                if row["Close the current position?"] == "Yes":
                    await page.locator(".WH3E").last.click()
                    await page.wait_for_timeout(3000)

                else:
                    # position name
                    if row["Position name"] != "nan":
                        await page.get_by_label(
                            "Position", exact=True
                        ).get_by_placeholder("Search").fill(row["Position name"])
                        await page.wait_for_timeout(3000)
                        await page.keyboard.press("Enter")
                        await page.wait_for_timeout(3000)
                        await page.keyboard.press("Enter")
                        await page.wait_for_timeout(3000)

                await page.get_by_role("button", name="Save Position").click()
                await page.wait_for_timeout(3000)

        # Job Profile
        if row["Job Profile"] != "nan" or row["Job Title"] != "nan":
            await page.get_by_role("button", name="Edit Job Profile").click()
            await page.wait_for_timeout(3000)

            if row["Job Profile"] != "nan":
                await page.get_by_role("textbox", name="Job Profile").fill(
                    row["Job Profile"]
                )
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Job Profile").press("Enter")
                await page.wait_for_timeout(3000)

            if row["Job Title"] != "nan":
                await page.get_by_role("textbox", name="Job Title").fill(
                    row["Job Title"]
                )
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Job Profile").click()
            await page.wait_for_timeout(3000)

            # Business Title
            if row["Business Title"] != "nan":
                await page.get_by_role("button", name="Edit Business Title").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Business Title").fill(
                    row["Business Title"]
                )
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Save Business Title").click()
                await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Next", exact=True).click()
        await page.wait_for_timeout(3000)
        if await page.get_by_role("button", name="Error").is_visible():
            await error(page, expect, row, env, user_id, country, idx)

        # LOCATION
        if (
            row["Location"] != "nan"
            or row["Scheduled Weekly Hours"] != "nan"
            or row["Work Shift"] != "nan"
        ):
            await expect(
                page.get_by_role("button", name="Edit Location Details")
            ).to_be_visible(timeout=15000)
            await page.get_by_role("button", name="Edit Location Details").click()
            await page.wait_for_timeout(3000)

            # fill location
            if row["Location"] != "nan":
                await page.get_by_role("textbox", name="Location").fill(row["Location"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            # Scheduled Weekly Hours
            if row["Scheduled Weekly Hours"] != "nan":
                await page.get_by_role("textbox", name="Scheduled Weekly Hours").fill(
                    row["Scheduled Weekly Hours"]
                )
                await page.wait_for_timeout(3000)

            # work shift
            if row["Work Shift"] != "nan":
                await page.get_by_role("textbox", name="Work Shift").fill(
                    row["Work Shift"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Location Details").click()
            await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Next", exact=True).click()
        await page.wait_for_timeout(5000)
        if await page.get_by_role("button", name="Error").is_visible():
            await error(page, expect, row, env, user_id, country, idx)

        # DETAILS tab
        await expect(
            page.get_by_role("heading", name="Job Classifications")
        ).to_be_visible(timeout=15000)
        await page.wait_for_timeout(3000)

        # job classification
        if row["Additional Job Classifications"] != "nan":
            await page.get_by_role("button", name="Edit Job Classifications").click()
            await page.wait_for_timeout(3000)

            await page.get_by_role(
                "textbox", name="Additional Job Classifications"
            ).fill(row["Additional Job Classifications"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Job Classifications").click()
            await page.wait_for_timeout(3000)

        # Administrative
        if (
            row["Employee Type"] != "nan"
            or row["Time Type"] != "nan"
            or row["Pay Rate Type"] != "nan"
            or row["Default Weekly Hours"] != "nan"
            or row["End Employment Date"] != "nan"
            or row["First Day of Work"] != "nan"
        ):

            await page.get_by_role("button", name="Edit Administrative").click()
            await page.wait_for_timeout(3000)

            if row["Employee Type"] != "nan":
                await page.get_by_role("textbox", name="Employee Type").fill(
                    row["Employee Type"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Time Type"] != "nan":
                await page.get_by_role("textbox", name="Time Type").fill(
                    row["Time Type"]
                )
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Time Type").press("Enter")
                await page.wait_for_timeout(3000)

            if row["Pay Rate Type"] != "nan":
                await page.get_by_role("textbox", name="Pay Rate Type").fill("Salary")
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Pay Rate Type").press("Enter")
                await page.wait_for_timeout(3000)

            if row["Default Weekly Hours"] != "nan":
                await page.get_by_role("textbox", name="Default Weekly Hours").fill(
                    row["Default Weekly Hours"]
                )
                await page.wait_for_timeout(3000)

            # End Employment Date
            if (
                "fixed term" in row["Employee Type"].lower()
                and row["End Employment Date"] != "nan"
            ):
                end_date = row["End Employment Date"]
                end_date = end_date.replace("/", "")
                await page.get_by_role("spinbutton", name="Month").nth(0).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(end_date[:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(end_date[2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(end_date[4:])
                await page.wait_for_timeout(3000)

            # First day of work
            if row["First Day of Work"] != "nan":
                first_day = row["First Day of Work"]
                first_day = first_day.replace("/", "")
                await page.get_by_role("spinbutton", name="Month").nth(1).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(first_day[:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(first_day[2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(first_day[4:])
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Administrative").click()
            await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Next", exact=True).click()
        await page.wait_for_timeout(5000)
        if await page.get_by_role("button", name="Error").is_visible():
            await error(page, expect, row, env, user_id, country, idx)

        # Compensation

        # Guidelines
        if (
            row["Compensation Package"] != "nan"
            or row["Compensation Grade"] != "nan"
            or row["Compensation Grade Profile"] != "nan"
        ):
            await page.get_by_role("button", name="Edit Guidelines").click()
            await page.wait_for_timeout(3000)

            # Compensation Packag
            if row["Compensation Package"] != "nan":
                await page.get_by_role("textbox", name="Compensation Package").fill(
                    row["Compensation Package"]
                )
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Compensation Package").press(
                    "Enter"
                )
                await page.wait_for_timeout(3000)

            # Compensation Grade
            if row["Compensation Grade"] != "nan":
                await page.get_by_role(
                    "textbox", name="Compensation Grade", exact=True
                ).fill(row["Compensation Grade"])
                await page.wait_for_timeout(3000)
                await page.get_by_role(
                    "textbox", name="Compensation Grade", exact=True
                ).press("Enter")
                await page.wait_for_timeout(3000)

            # Compensation Grade Profile
            if row["Compensation Grade Profile"] != "nan":
                await page.get_by_role(
                    "textbox", name="Compensation Grade Profile"
                ).fill(row["Compensation Grade Profile"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")

                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Guidelines").click()
            await page.wait_for_timeout(3000)

        # salary
        if (
            row["Salary Amount"] != "nan"
            or row["Salary Currency"] != "nan"
            or row["Salary Frequency"] != "nan"
        ):
            await page.get_by_role("button", name="Edit Salary").click()
            await page.wait_for_timeout(3000)

            if row["Salary Amount"] != "nan":
                await page.get_by_role("textbox", name="Amount", exact=True).fill(
                    row["Salary Amount"]
                )
                await page.wait_for_timeout(3000)

            if row["Salary Currency"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Currency"
                ).locator("li").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Salary Currency"]
                )
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").press("Enter")
                await page.wait_for_timeout(3000)

            if row["Salary Frequency"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Frequency"
                ).locator("li").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency").fill(
                    row["Salary Frequency"]
                )
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency").press("Enter")
                await page.wait_for_timeout(3000)
                await page.get_by_role("listbox", name="Search Results, Options").press(
                    "Enter"
                )
                await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Salary").click()
            await page.wait_for_timeout(3000)

        # Allowance
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

            await page.wait_for_timeout(3000)

            if row["Allowance Amount"] != "nan":
                await page.get_by_role("textbox", name="Amount").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Amount").fill(
                    row["Allowance Amount"]
                )
                await page.wait_for_timeout(3000)

            if row["Allowance Currency"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Currency"
                ).locator("li").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Allowance Currency"]
                )
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Currency").press("Enter")
                await page.wait_for_timeout(3000)

            if row["Allowance Frequency"] != "nan":
                await page.get_by_role(
                    "listbox", name="items selected for Frequency"
                ).locator("li").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency").fill(
                    row["Allowance Frequency"]
                )
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Frequency").press("Enter")
                await page.wait_for_timeout(3000)
                await page.get_by_label("Monthly radio button selected").get_by_text(
                    row["Allowance Frequency"]
                ).click()
                await page.wait_for_timeout(3000)

            # additional details

            # await page.get_by_role("button", name="Additional Details").click()
            # await page.wait_for_timeout(3000)

            # await page.get_by_role("group", name="Expected End Date current").get_by_placeholder("MM").click()

            # await page.wait_for_timeout(3000)
            # await page.keyboard.type("08")
            # await page.wait_for_timeout(3000)
            # await page.keyboard.type("01")
            # await page.wait_for_timeout(3000)
            # await page.keyboard.type("2025")
            # await page.wait_for_timeout(3000)

            # await page.get_by_role("group", name="Actual End Date current value").get_by_placeholder("MM").click()
            # await page.wait_for_timeout(3000)
            # await page.keyboard.type("08")
            # await page.wait_for_timeout(3000)
            # await page.keyboard.type("01")
            # await page.wait_for_timeout(3000)
            # await page.keyboard.type("2025")
            # await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Allowance").click()

            await page.wait_for_timeout(3000)

        # Merit
        if (
            row["Merit Individual Target %"] != "nan"
            and row["Merit Compensation Plan"] != "nan"
        ):

            await expect(page.get_by_role("button", name="Add Merit")).to_be_visible(
                timeout=15000
            )
            await page.get_by_role("button", name="Add Merit").click()

            await page.get_by_role("textbox", name="Compensation Plan").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Compensation Plan").fill(
                row["Merit Compensation Plan"]
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Merit").click()
            await page.wait_for_timeout(3000)

        elif row["Merit Individual Target %"] != "nan":
            await page.get_by_role("button", name="Edit Merit").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Individual Target %").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Individual Target %").fill(
                row["Merit Individual Target %"]
            )
            await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Merit").click()
            await page.wait_for_timeout(3000)

        # Bonus
        if (
            row["Bonus Compensation Plan"] != "nan"
            and row["Bonus Individual Target %"] != "nan"
        ):
            await page.get_by_role("button", name="Add Bonus").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Search").fill(
                row["Bonus Compensation Plan"]
            )
            await page.wait_for_timeout(5000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Individual Target %").fill(
                row["Bonus Individual Target %"]
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Bonus").click()
            await page.wait_for_timeout(3000)

        elif row["Bonus Individual Target %"] != "nan":
            await page.get_by_role("button", name="Edit Bonus").click()
            await page.wait_for_timeout(3000)

            await page.get_by_role("textbox", name="Individual Target %").fill(
                row["Bonus Individual Target %"]
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Bonus").click()
            await page.wait_for_timeout(3000)

        # Add LTI
        if (
            row["LTI Compensation change"] != "nan"
            and row["LTI Individual Target %"] != "nan"
        ):
            await page.get_by_role("button", name="Add LTI").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Compensation Plan").fill(
                row["LTI Compensation change"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Individual Target %").fill(
                row["LTI Individual Target %"]
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save LTI").click()
            await page.wait_for_timeout(3000)

        elif row["LTI Individual Target %"] != "nan":
            await page.get_by_role("button", name="Edit LTI").click()
            await page.wait_for_timeout(3000)

            await page.get_by_role("textbox", name="Individual Target %").fill(
                row["LTI Individual Target %"]
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save LTI").click()
            await page.wait_for_timeout(3000)

        # commission
        if row["Compensation Plan"] != "nan":
            await page.get_by_role("button", name="Add Commission").click()
            await page.wait_for_timeout(3000)

            await page.get_by_role("textbox", name="Compensation Plan").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Compensation Plan").fill(
                row["Commission Compensation Plan"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

            if row["Target Amount"] != "nan":
                await page.get_by_role("textbox", name="Target Amount").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Target Amount").fill(
                    row["Target Amount"]
                )
                await page.wait_for_timeout(3000)

            if row["Commission Currency"] != "nan":
                await page.get_by_role("textbox", name="Currency").fill(
                    row["Commission Currency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Commission Frequency"] != "nan":
                await page.get_by_role("textbox", name="Frequency", exact=True).fill(
                    row["Commission Frequency"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Draw Amount"] != "nan":
                await page.get_by_role("textbox", name="Draw Amount").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Draw Amount").fill(
                    row["Draw Amount"]
                )
                await page.wait_for_timeout(3000)

            if row["Draw Frequency"] != "nan":
                await page.get_by_role("textbox", name="Draw Frequency").click()
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
                await page.get_by_role("textbox", name="Draw Duration").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Draw Duration").fill(
                    row["Draw Duration"]
                )
                await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Commission").click()
            await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Next", exact=True).click()
        await page.wait_for_timeout(5000)
        if await page.get_by_role("button", name="Error").is_visible():
            await error(page, expect, row, env, user_id, country, idx)

        # ORGANIZATIONS

        # edit company
        if row["Company"] != "nan":
            await page.get_by_role("button", name="Edit Company").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Company").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Company").fill(row["Company"])
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Company").press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Company").click()
            await page.wait_for_timeout(3000)

        # edit cost center
        if row["Cost Center"] != "nan":
            await page.get_by_role("button", name="Edit Cost Center").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Cost Center").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Cost Center").fill(
                row["Cost Center"]
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Cost Center").press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Cost Center").click()
            await page.wait_for_timeout(3000)

        # edit region
        if row["Region"] != "nan":
            await page.get_by_role("button", name="Edit Region").click()
            await page.wait_for_timeout(3000)

            await page.get_by_role("textbox", name="Region").fill(row["Region"])
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Region").press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Region").click()
            await page.wait_for_timeout(3000)

        # other

        # MRC
        if row["MRC"] != "nan":
            await expect(
                page.get_by_role("button", name="Edit Other Row 1", exact=True)
            ).to_be_visible(timeout=15000)
            await page.get_by_role(
                "button", name="Edit Other Row 1", exact=True
            ).click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["MRC"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # union
        if row["Union"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 2").click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["Union"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # employee function
        if row["Employee Function"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 3").click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["Employee Function"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # Controlling area (Sector)
        if row["Controlling Area"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 4").click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["Controlling Area"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # Workday function
        if row["Workday Function"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 5").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("listbox", name="items selected for").locator(
                "li"
            ).click()
            await page.wait_for_timeout(3000)
            locator = page.locator('div[id="56$213513"]')
            await locator.click()
            await page.wait_for_timeout(3000)
            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).click()
            await page.wait_for_timeout(3000)
            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["Workday Function"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # Contact center agents
        if row["Contact Center Agents"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 6").click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["Contact Center Agents"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # Ionized radiation exposure
        if row["Ionized Radiation Exposure"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 7").click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["Ionized Radiation Exposure"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # Year end compensation wage
        if row["Year End Compensation Wage"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 8").click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["Year End Compensation Wage"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # Franchise
        if row["Franchise"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 9").click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["Franchise"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # MRC for headcount
        if row["MRC for Headcount"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 10").click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["MRC for Headcount"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # cost center headcount
        if row["Cost Center for Headcount"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 11").click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["Cost Center for Headcount"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # Remote work
        if row["Remote Work"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 12").click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["Remote Work"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Next", exact=True).click()
        await page.wait_for_timeout(5000)
        if await page.get_by_role("button", name="Error").is_visible():
            await error(page, expect, row, env, user_id, country, idx)

        # Skipping collective agreement
        if row["Collective Agreement"] != "nan":
            await expect(page.get_by_role("button", name="Add")).to_be_visible(
                timeout=15000
            )
            await page.get_by_role("button", name="Add").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Collective Agreement").fill(
                row["Collective Agreement"]
            )
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(000)

        await page.get_by_role("button", name="Next", exact=True).click()
        await page.wait_for_timeout(5000)
        if await page.get_by_role("button", name="Error").is_visible():
            await error(page, expect, row, env, user_id, country, idx)
            await page.wait_for_timeout(5000)

        # Final submit step
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(20000)

        # Wait for dialog popup (use wait_for_selector + timeout)
        try:
            await page.wait_for_timeout(10000)
            popup_header_selector = page.get_by_role("dialog").first

            if (
                await popup_header_selector.is_visible()
                and await page.get_by_label("Review Change Job").is_visible()
            ):
                await page.wait_for_timeout(10000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_initiation_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
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
            await page.wait_for_timeout(10000)
            popup_header_selector = page.get_by_role("dialog").first

            if await popup_header_selector.is_visible():
                await page.wait_for_timeout(10000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_initiation_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
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
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_initiation_{idx}.png"
            )
            print("Error detected. Screenshot taken.")
            await page.wait_for_timeout(10000)
            return False

    except Exception as e:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_initiation_{idx}.png"
        )
        print(f"Unexpected Error: {e}")
        await page.wait_for_timeout(10000)
        return False
