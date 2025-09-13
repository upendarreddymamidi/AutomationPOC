from ..login import login
import os
from helpers.encoding import safe_print

async def run_script(page, expect, row, env, user_id, country, idx):
    await login(page, expect, env, user_id, idx)
    try:
        await page.wait_for_timeout(5000)
        await expect(page.locator('input[type="search"]')).to_be_visible(timeout=60000)
        await page.fill('input[type="search"]', "View Supervisory Organization")
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # Click on "View Supervisory Organization"
        await page.get_by_role(
            "link", name="View Supervisory Organization", exact=True
        ).click()
        await page.wait_for_timeout(5000)

        # Click on Supervisory Organization and search for a specific one
        await page.get_by_role(
            "textbox", name="Supervisory Organization", exact=True
        ).click()
        await page.locator('input[placeholder="Search"]').nth(1).fill(
            row["Supervisory Organization"]
        )
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(3000)

        # Click on "Related Actions"
        related_icon_by_aria_label = page.get_by_role(
            "button", name="Related Actions"
        ).nth(0)
        await expect(related_icon_by_aria_label).to_be_visible(timeout=60000)
        await related_icon_by_aria_label.click()
        await page.wait_for_timeout(3000)

        # Click on "Staffing"
        await page.get_by_role("menuitem", name="Staffing", exact=True).click()
        await page.wait_for_timeout(3000)

        # Click on "Position Request Reason"
        await page.get_by_role(
            "textbox", name="Position Request Reason", exact=True
        ).click()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Create Position > Position Request", exact=True).click()
        await page.wait_for_timeout(3000)

        # Click on Position Request Reason
        await page.get_by_text(row["Position Request Reason"], exact=True).click()
        await page.wait_for_timeout(3000)

        # Fill in "Job Posting Title"
        await page.get_by_role("textbox", name="Job Posting Title", exact=True).fill(
            row["Job Posting Title"]
        )
        await page.wait_for_timeout(3000)

        # Fill in "Number of Positions"
        number_of_positions = page.get_by_role(
            "textbox", name="Number of Positions", exact=True
        )
        await number_of_positions.click()
        await page.keyboard.press("Control+A")  # Select all text
        await page.keyboard.type(row["Number of Positions"])
        await page.wait_for_timeout(3000)

        # Fill in "Availability Date"
        await page.get_by_role("spinbutton", name="Month", exact=True).nth(0).click()
        await page.keyboard.type(row["Availability Date"])
        await page.wait_for_timeout(3000)

        # Fill in "Earliest Hire Date"
        await page.get_by_role("spinbutton", name="Month", exact=True).nth(1).click()
        await page.keyboard.type(row["Earliest Hire Date"])
        await page.wait_for_timeout(3000)

        # Fill in "Job Profile"
        await page.get_by_role("textbox", name="Job Profile", exact=True).fill(
            row["Job profile"]
        )
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # Fill in "Location"
        await page.get_by_role("textbox", name="Location", exact=True).fill(
            row["Location"]
        )
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # Fill in "Time Type"
        await page.get_by_role("textbox", name="Time Type", exact=True).fill(
            row["Time Type"]
        )
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # Fill in "Worker Type"
        await page.get_by_role("textbox", name="Worker Type", exact=True).fill(
            row["Worker Type"]
        )
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(1000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # Submit the form
        await page.get_by_role("button", name="Submit", exact=True).click()
        await page.wait_for_timeout(3000)

        # Check if the error widget is visible after submission
        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector):
            await page.click(error_widget_selector)  # Click on the error widget
            await page.wait_for_timeout(2000)  # Wait for 2 seconds
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/create_position_error_{idx}.png",
                full_page=True,
            )  # Save the screenshot
            raise Exception("Error widget appeared with errors after submission.")
        else:
            await page.wait_for_timeout(6000)
            popup_header_selector = "h2#bpSlimConclusionHeaderText"
            if await page.is_visible(popup_header_selector):
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/create_position_confirmation_{idx}.png"
                )
                safe_print("Submission confirmation popup is visible and screenshot taken.")
                return True

    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/create_position_error_{idx}.png",
            full_page=True,
        )
        safe_print(error)  # Reraise the error after taking the screenshot
        return False
