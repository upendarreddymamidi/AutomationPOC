from ..login import login
import os
from helpers.encoding import safe_print

async def run_script(page, expect, row, env, user_id, country, idx):
    if country in ["Mexico", "Brazil", "Japan"] and env.split("-")[1] == "jj1":
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
        ).to_be_visible(timeout=35000)

        if country in ["Japan"]:
            name = f"{row["Given Name - Western Script"]} {row["Family Name - Western Script"]}"
            personal_change_button_name = f"Personal Information Change: {name}"
        else:
            name = f"{row["First Name"]} {row["Last Name"]}"
            if row["Second Last Name"] != "nan":
                name += f" {row["Second Last Name"]}"
            if row["Married Last Name"] != "nan":
                name += f" {row["Married Last Name"]}"
            personal_change_button_name = (
                f"Personal Information Change: {name} ({row["Country"]})"
            )

        await page.get_by_role("button", name="My Tasks Items").click()
        await expect(
            page.locator(
                '[data-automation-id="titleText"]', has_text=personal_change_button_name
            ).first
        ).to_be_visible(timeout=35000)
        await page.locator(
            '[data-automation-id="titleText"]', has_text=personal_change_button_name
        ).first.click()
        await page.wait_for_timeout(3000)

        await expect(
            page.get_by_role("button", name="Edit Gender", exact=True)
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="Edit Gender", exact=True).click()
        await page.wait_for_timeout(2000)
        await page.get_by_role("button", name="Gender select one").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("option", name=row["Gender"], exact=True).click()
        await page.wait_for_timeout(2000)
        await page.get_by_role("button", name="Save Gender").click()

        # Edit Date of Birth
        await expect(
            page.get_by_role("button", name="Edit Date of Birth")
        ).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Edit Date of Birth").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Date of Birth"])
        await page.get_by_role("button", name="Save Date of Birth").click()
        await page.wait_for_timeout(3000)

        if country in ["United States of America", "Brazil"]:
            await expect(
                page.get_by_role("button", name="Edit Race/Ethnicity")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name="Edit Race/Ethnicity").click()
            await expect(
                page.get_by_role("textbox", name="Race/Ethnicity")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("textbox", name="Race/Ethnicity").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Race/Ethnicity"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Race/Ethnicity").click()

        if country in ["Mexico", "Costa Rica", "Brazil"]:
            # Edit Place of Birth
            await expect(
                page.get_by_role("button", name="Edit Place of Birth")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name="Edit Place of Birth").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Place of Birth"])
            await page.keyboard.press("Enter")

            if country in ["Costa Rica", "Brazil"]:
                await page.wait_for_timeout(3000)
                await expect(
                    page.get_by_role("textbox", name="Region of Birth")
                ).to_be_visible(timeout=60000)
                await page.get_by_role("textbox", name="Region of Birth").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Region of Birth"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")

            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="City of Birth").click()
            await page.keyboard.type(row["City of Birth"])
            await page.get_by_role("button", name="Save Place of Birth").click()

        if country in ["Mexico", "Costa Rica", "Brazil", "Japan"]:
            # Edit Marital Status
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
            await expect(
                page.get_by_role("button", name="Edit Citizenship Status")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name="Edit Citizenship Status").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Citizenship"])
            await page.wait_for_timeout(5000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(5000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Citizenship Status").click()

        if country in ["Mexico", "Costa Rica", "Brazil", "Japan"]:
            # Edit Nationality
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

        if country in ["Japan"]:
            await expect(
                page.get_by_role("button", name="Edit Gender Identity")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name="Edit Gender Identity").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_text(row["Gender Identity"]).first.click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Gender Identity").click()

        # Submit
        await page.wait_for_timeout(5000)
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)
        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").first.is_visible()
        ):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/change_personal_information_error_{idx}.png"
            )
            safe_print("Widget error")
            return False
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/change_personal_information_confirmation_{idx}.png"
        )
        safe_print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/change_personal_information_error_{idx}.png",
            full_page=True,
        )
        safe_print(error)  # Reraise the error after taking the screenshot
        return False
