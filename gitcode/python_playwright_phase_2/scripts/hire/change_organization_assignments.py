from ..login import login
import os
from helpers.encoding import safe_print


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Want to Rescind?"] == "Yes" or row["Want to correct?"] == "Yes":
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

        if country in ["Japan"]:
            name = f"{row["Given Name - Western Script"]} {row["Family Name - Western Script"]}"
            assign_button_name = f"Assign Organizations: Hire: {name}"
        else:
            name = f"{row["First Name"]} {row["Last Name"]}"
            if row["Second Last Name"] != "nan":
                name += f" {row["Second Last Name"]}"
            if row["Married Last Name"] != "nan":
                name += f" {row["Married Last Name"]}"
            assign_button_name = (
                f"Assign Organizations: Hire: {name} - {row["Job Posting Title"]}"
            )

        await page.get_by_role("button", name="My Tasks Items").click()

        await expect(
            page.get_by_role("button", name=assign_button_name).first
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name=assign_button_name).first.click()
        await page.wait_for_timeout(7000)

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
            ).to_be_visible(timeout=60000)
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
            await page.keyboard.press("Control+A")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Backspace")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_text(row["Union"]).last.click()
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
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # Controlling area (Sector)
        if row["Controlling Area (Sector)"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 4").click()
            await page.wait_for_timeout(3000)

            await page.get_by_label("Other", exact=True).get_by_placeholder(
                "Search"
            ).fill(row["Controlling Area (Sector)"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Other Row").click()
            await page.wait_for_timeout(3000)

        # Workday function
        if row["Workday Function"] != "nan":
            await page.get_by_role("button", name="Edit Other Row 5").click()
            await page.wait_for_timeout(3000)
            delete_button = page.locator('[data-automation-id="DELETE_charm"]')
            await delete_button.click()
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_text(row["Workday Function"]).click()
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

        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)
        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").first.is_visible()
        ):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/change_of_organizations_assignmets_error_{idx}.png"
            )
            safe_print("Widget error")
            return False
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/change_of_organizations_assignmets_confirmation_{idx}.png"
        )
        safe_print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/change_of_organizations_assignmets_error_{idx}.png",
            full_page=True,
        )
        safe_print(error)  # Reraise the error after taking the screenshot
        return False
