from ..login import login
import os


async def Contract_correction(page, expect, row, env, user_id, country, idx):
    # Get all links matching refurbish
    links = await page.get_by_text("Contract").all()
    print(links)

    if (
        "add" in row["What changes you made?-C"].lower()
        or "fixed" in row["What changes you made?-C"].lower()
    ):
        different_contract = page.locator(
            '[data-automation-id="promptOption"][data-automation-label="Open"]'
        )
    elif "close" in row["What changes you made?-C"].lower():
        different_contract = page.locator(
            '[data-automation-id="promptOption"][data-automation-label="Closed"]'
        )

    Contract_Type = row["Contract Type-C"]
    contract_type = (
        page.locator('[data-automation-id="promptOption"]')
        .get_by_text(Contract_Type)
        .first
    )

    for page_link in links:
        await page.wait_for_timeout(3000)
        await page_link.click()
        await page.wait_for_timeout(3000)

        if (
            await page.get_by_text("Contract").first.is_visible()
            and await different_contract.is_visible()
            and await contract_type.is_visible()
        ):
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Related Actions").nth(2).click()
            await page.wait_for_timeout(3000)
            await page.get_by_text("Business Process").hover()
            await page.wait_for_timeout(3000)
            await page.get_by_text("Correct").first.click()
            await expect(
                page.get_by_text("Correct Business Process", exact=True)
            ).to_be_visible(timeout=60000)

            # correction Contract scripts of job change

            # contract start date
            if row["Contract Start Date-C"] != "nan":
                start_date_locator = page.get_by_role(
                    "group", name="Contract Start Date Current"
                )
                await start_date_locator.get_by_placeholder("MM").click()
                await page.wait_for_timeout(3000)
                contract_start_date = row["Contract Start Date-C"]
                contract_start_date = contract_start_date.replace("/", "")
                await page.keyboard.type(contract_start_date[:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(contract_start_date[2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(contract_start_date[4:])
                await page.wait_for_timeout(3000)

            # Contract type
            if row["Contract Type-C"] != "nan":
                await page.wait_for_timeout(3000)
                label_locator = page.locator('[data-automation-id="formLabel"]')
                await label_locator.get_by_text("Contract Type").first.click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Contract Type").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Contract Type").fill(
                    row["Contract Type-C"]
                )
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Contract Type").press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

                await page.get_by_text("Correct Business Process").first.click()

            # Status
            if row["Status-C"] != "nan":
                await page.wait_for_timeout(3000)
                status_locator = page.locator('[data-automation-id="formLabel"]')
                await status_locator.get_by_text("Status").first.click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Status").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Status").fill(row["Status-C"])
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Status").press("Enter")
                await page.wait_for_timeout(3000)

            # Employee Contract End Date
            if row["Contract End date-C"] != "nan":
                await page.wait_for_timeout(3000)
                Contract_end_date = row["Contract End date-C"]
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

            # comment for correction
            if row["Comment for Correction"] != "nan":
                await page.get_by_role("textbox", name="enter your comment").fill(
                    row["Comment for Correction"]
                )

            if await page.get_by_role("button", name="Error").is_visible():
                return await error(page, expect, row, env, user_id, country, idx)

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

            event_locator = page.locator("#bpSlimConclusionHeaderText")
            await event_locator.wait_for(state="visible", timeout=15000)

            if await event_locator.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_correction_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True
        await page.go_back()
        await page.wait_for_timeout(5000)
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

        # Format effective date for correction
        Effective_Date = row["Effective Date of Process"]
        Effective_Date = Effective_Date.replace("/", "")
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(Effective_Date[:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(Effective_Date[2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(Effective_Date[4:])
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)

    await page.wait_for_timeout(5000)
    await page.screenshot(
        path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_correction_{idx}.png"
    )
    return False


async def error(page, expect, row, env, user_id, country, idx):
    if await page.get_by_role("button", name="Error").is_visible():
        await page.wait_for_timeout(5000)
        await page.get_by_role("button", name="Error").click()
    await page.wait_for_timeout(5000)
    await page.screenshot(
        path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_correction_{idx}.png"
    )
    print("Error widget appeared with errors.")
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
    await page.wait_for_timeout(3000)


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Rescind"] == "Yes":
        return True
    if row["Correction"] != "Yes":
        return True

    await login(page, expect, env, user_id, idx)
    try:
        # if lateral move proxy Aimbyl
        if "lateral" in row["Why making this changes?"].lower():
            await Aimbyl(page, expect, row, env, user_id, country, idx)

        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").fill(row["WWID"])
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # Click on "Employee" link
        await expect(page.get_by_role("link", name=f"({row['WWID']})")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("link", name=f"({row['WWID']})").click()

        await expect(page.get_by_text("Actions").first).to_be_visible(timeout=60000)
        await page.get_by_text("Actions").first.click()
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

        # Format effective date for correction
        Effective_Date = row["Effective Date of Process"]
        Effective_Date = Effective_Date.replace("/", "")
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(Effective_Date[:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(Effective_Date[2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(Effective_Date[4:])
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)

        # if Contract Script jump to specific function
        if "contract" in row["What changes you made?-C"].lower():
            await page.wait_for_timeout(5000)
            if not await Contract_correction(
                page, expect, row, env, user_id, country, idx
            ):
                return False
            else:
                return True

        # Get all links matching refurbish
        links = await page.get_by_text(row["Correction Process Name"]).all()
        print(links)

        for page_link in links:
            print(page_link)
            await page.wait_for_timeout(3000)
            await page_link.click()
            await page.wait_for_timeout(3000)

            if await page.get_by_text(
                row["What changes you made?-C"]
            ).first.is_visible():
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Related Actions").nth(1).click()
                await page.wait_for_timeout(3000)
                await page.get_by_text("Business Process").hover()
                await page.wait_for_timeout(3000)
                await page.get_by_text("Correct").first.click()
                await expect(
                    page.get_by_text("Correct Business Process", exact=True)
                ).to_be_visible(timeout=60000)

                # correction of job change

                # if not lateral move
                # effective date
                if row["Effective Date-C"] != "nan":
                    # Check if the specific group with placeholder "MM" is visible

                    await page.get_by_role(
                        "group", name="Effective Date current value"
                    ).get_by_placeholder("MM").click()

                    effective_date = row["Effective Date-C"]
                    effective_date = effective_date.replace("/", "")

                    # Type each part with delays
                    await page.keyboard.type(effective_date[:2])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(effective_date[2:4])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(effective_date[4:])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")

                # Reason

                if row["Why making this changes?-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text("Reason").first.click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Reason").first.click()

                    await page.get_by_role("textbox", name="Reason").first.fill(
                        row["Why making this changes?-C"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    if await page.get_by_text("No matches found").first.is_visible():
                        return await error(
                            page, expect, row, env, user_id, country, idx
                        )

                # Job details

                # Position name
                if row["Position name-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text("Position").first.click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_label("Position", exact=True).get_by_placeholder(
                        "Search"
                    ).fill(row["Position name-C"])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    if await page.get_by_text("No matches found").first.is_visible():
                        return await error(
                            page, expect, row, env, user_id, country, idx
                        )

                # Job Profile

                if row["Job Profile-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text("Job Profile").first.click()
                    await page.wait_for_timeout(3000)
                    job_profile_field = page.get_by_role(
                        "textbox", name="Job Profile"
                    ).first

                    await job_profile_field.fill(row["Job Profile-C"])
                    await page.wait_for_timeout(3000)
                    await job_profile_field.press("Enter")
                    await page.wait_for_timeout(3000)
                    if await page.get_by_text("No matches found").first.is_visible():
                        return await error(
                            page, expect, row, env, user_id, country, idx
                        )

                if row["Job Title-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text("Job Title").first.click()
                    await page.wait_for_timeout(3000)
                    job_title_field = page.get_by_role(
                        "textbox", name="Job Title"
                    ).first

                    await job_title_field.fill(row["Job Title-C"])
                    await page.wait_for_timeout(3000)
                    if await page.get_by_text("No matches found").first.is_visible():
                        return await error(
                            page, expect, row, env, user_id, country, idx
                        )

                # Business Title
                if row["Business Title-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text("Business Title").first.click()
                    await page.wait_for_timeout(3000)
                    business_title_field = page.get_by_role(
                        "textbox", name="Business Title"
                    ).first

                    await business_title_field.fill(row["Business Title-C"])
                    await page.wait_for_timeout(3000)
                    if await page.get_by_text("No matches found").first.is_visible():
                        return await error(
                            page, expect, row, env, user_id, country, idx
                        )

                # LOCATION

                # Fill Location
                if row["Where this person be located after this change?-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text("Location").first.click()
                    await page.wait_for_timeout(3000)
                    location_field = page.get_by_role("textbox", name="Location").first

                    await location_field.fill(
                        row["Where this person be located after this change?-C"]
                    )
                    await page.wait_for_timeout(3000)
                    await location_field.press("Enter")
                    await page.wait_for_timeout(3000)
                    if await page.get_by_text("No matches found").first.is_visible():
                        return await error(
                            page, expect, row, env, user_id, country, idx
                        )

                # Fill Scheduled Weekly Hours
                if row["Scheduled Weekly Hours-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text(
                        "Scheduled Weekly Hours"
                    ).first.click()
                    await page.wait_for_timeout(3000)
                    weekly_hours_field = page.get_by_role(
                        "textbox", name="Scheduled Weekly Hours"
                    ).first
                    if await weekly_hours_field.is_visible():
                        await weekly_hours_field.fill(row["Scheduled Weekly Hours-C"])
                        await page.wait_for_timeout(3000)
                        if await page.get_by_text(
                            "No matches found"
                        ).first.is_visible():
                            return await error(
                                page, expect, row, env, user_id, country, idx
                            )

                # Fill Work Shift
                if row["Work Shift-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text("Work Shift").first.click()
                    await page.wait_for_timeout(3000)
                    work_shift_field = page.get_by_role(
                        "textbox", name="Work Shift"
                    ).first
                    if await work_shift_field.is_visible():
                        await work_shift_field.fill(row["Work Shift-C"])
                        await page.wait_for_timeout(3000)
                        await work_shift_field.press("Enter")
                        await page.wait_for_timeout(3000)

                        if await page.get_by_text(
                            "No matches found"
                        ).first.is_visible():
                            return await error(
                                page, expect, row, env, user_id, country, idx
                            )

                # DETAILS tab

                # Fill Additional Job Classifications
                if row["Additional Job Classifications"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text(
                        "Additional Job Classifications"
                    ).first.click()
                    await page.wait_for_timeout(3000)
                    job_classifications_field = page.get_by_role(
                        "textbox", name="Additional Job Classifications"
                    ).first
                    if await job_classifications_field.is_visible():
                        await job_classifications_field.fill(
                            row["Additional Job Classifications-C"]
                        )
                        await page.wait_for_timeout(3000)
                        await job_classifications_field.press("Enter")
                        await page.wait_for_timeout(3000)
                        if await page.get_by_text(
                            "No matches found"
                        ).first.is_visible():
                            return await error(
                                page, expect, row, env, user_id, country, idx
                            )

                # Additional Details
                # Administrative

                # Fill Employee Type
                if row["Employee Type-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text("Employee Type").first.click()
                    await page.wait_for_timeout(3000)
                    employee_type_field = page.get_by_role(
                        "textbox", name="Employee Type"
                    ).first
                    if await employee_type_field.is_visible():
                        await employee_type_field.fill(row["Employee Type-C"])
                        await page.wait_for_timeout(3000)
                        await employee_type_field.press("Enter")
                        await page.wait_for_timeout(3000)
                        await employee_type_field.press("Enter")
                        await page.wait_for_timeout(3000)
                        if await page.get_by_text(
                            "No matches found"
                        ).first.is_visible():
                            return await error(
                                page, expect, row, env, user_id, country, idx
                            )

                # Fill Time Type
                if row["Time Type-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text("Time Type").first.click()
                    await page.wait_for_timeout(3000)
                    time_type_field = page.get_by_role(
                        "textbox", name="Time Type"
                    ).first
                    if await time_type_field.is_visible():
                        await time_type_field.fill(row["Time Type-C"])
                        await page.wait_for_timeout(3000)
                        await time_type_field.press("Enter")
                        await page.wait_for_timeout(3000)
                        if await page.get_by_text(
                            "No matches found"
                        ).first.is_visible():
                            return await error(
                                page, expect, row, env, user_id, country, idx
                            )

                # Fill Pay Rate Type
                if row["Pay Rate Type-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text("Pay Rate Type").first.click()
                    await page.wait_for_timeout(3000)
                    pay_rate_type_field = page.get_by_role(
                        "textbox", name="Pay Rate Type"
                    ).first
                    if await pay_rate_type_field.is_visible():
                        await pay_rate_type_field.fill(row["Pay Rate Type-C"])
                        await page.wait_for_timeout(3000)
                        await pay_rate_type_field.press("Enter")
                        await page.wait_for_timeout(3000)
                        await pay_rate_type_field.press("Enter")
                        await page.wait_for_timeout(3000)
                        if await page.get_by_text(
                            "No matches found"
                        ).first.is_visible():
                            return await error(
                                page, expect, row, env, user_id, country, idx
                            )

                if row["Default Weekly Hours-C"] != "nan":
                    label_locator = page.locator('[data-automation-id="formLabel"]')
                    await label_locator.get_by_text(
                        "Default Weekly Hours"
                    ).first.click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("textbox", name="Default Weekly Hours").fill(
                        row["Default Weekly Hours-C"]
                    )
                    await page.wait_for_timeout(3000)

                # End Employment Date
                if row["End Employment Date-C"] != "nan":
                    end_date_str = row["End Employment Date-C"]
                    end_date_str = end_date_str.replace("/", "")
                    end_month_input = page.get_by_role("spinbutton", name="Month").nth(
                        0
                    )
                    if await end_month_input.is_visible():
                        await end_month_input.click()
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(end_date_str[:2])  # Month
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(end_date_str[2:4])  # Day
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(end_date_str[4:])  # Year
                        await page.wait_for_timeout(3000)

                # First Day of Work
                if row["First Day of Work-C"] != "nan":
                    first_day_str = row["First Day of Work-C"]
                    first_day_str = first_day_str.replace("/", "")
                    # date_locator=page.locator('[data-automation-id="dateSectionMonth-input"]')
                    if row["End Employment Date-C"] == "nan":
                        first_day_spinbutton = page.get_by_role(
                            "group", name="First Day of Work current"
                        ).get_by_placeholder("MM")
                    else:
                        first_day_spinbutton = page.get_by_role(
                            "spinbutton", name="Month"
                        ).nth(1)
                    if await first_day_spinbutton.is_visible():
                        await first_day_spinbutton.click()
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(first_day_str[:2])  # Month
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(first_day_str[2:4])  # Day
                        await page.wait_for_timeout(3000)
                        await page.keyboard.type(first_day_str[4:])  # Year
                        await page.wait_for_timeout(3000)

                # comment for correction
                if row["Comment for Correction"] != "nan":
                    await page.get_by_role("textbox", name="enter your comment").fill(
                        row["Comment for Correction"]
                    )

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

                event_locator = page.locator("#bpSlimConclusionHeaderText")
                await event_locator.wait_for(state="visible", timeout=15000)

                if await event_locator.is_visible():
                    await page.wait_for_timeout(5000)
                    await page.screenshot(
                        path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_correction_{idx}.png"
                    )
                    print(
                        "Submission confirmation popup is visible and screenshot taken."
                    )
                    return True
            await page.go_back()
            await page.wait_for_timeout(5000)
            await expect(
                page.get_by_role("button", name="Status Sort and filter column")
            ).to_be_visible(timeout=60000)
            await page.get_by_role(
                "button", name="Status Sort and filter column"
            ).click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Value").fill(
                "Successfully Complete"
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Filter", exact=True).click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Effective Date Sort and").click()
            await page.wait_for_timeout(3000)

            # Format effective date for correction
            Effective_Date = row["Effective Date of Process"]
            Effective_Date = Effective_Date.replace("/", "")
            await page.get_by_role("spinbutton", name="Month").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(Effective_Date[:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(Effective_Date[2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(Effective_Date[4:])
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Filter", exact=True).click()
            await page.wait_for_timeout(3000)
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_correction_{idx}.png"
        )
        return False
    except Exception as error:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_correction_{idx}.png"
        )
        print(f"Error: {error}")
        return False
