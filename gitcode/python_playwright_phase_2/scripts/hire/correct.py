from ..login import login
import os
from helpers.encoding import safe_print


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Want to correct?"] != "Yes":
        return True
    await login(page, expect, env, user_id, idx)
    try:
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").fill(
            row["WWID to correct"]
        )
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # Click on "Employee" link
        await expect(
            page.get_by_role("link", name=f"({row["WWID to correct"]})")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("link", name=f"({row["WWID to correct"]})").click()
        await expect(page.get_by_text("Actions")).to_be_visible(timeout=60000)

        await page.wait_for_timeout(3000)
        name = (await page.text_content("h1")).strip()

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
        await page.get_by_role("textbox", name="Value").fill(row["Process Status - C"])
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Effective Date Sort and").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Correction Effective Date"][:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Correction Effective Date"][2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Correction Effective Date"][4:])
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)
        await page.get_by_text(f"Hire: {name}", exact=True).click()
        await page.wait_for_timeout(10000)
        await expect(
            page.get_by_role("button", name="Related Actions").first
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="Related Actions").first.click()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Business Process").hover()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Correct", exact=True).click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_text("Correct Business Process")).to_be_visible(
            timeout=60000
        )

        if row["Hire Date - C"] != "nan":
            await page.get_by_role("group").filter(
                has_text="Hire Date"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Hire Date - C"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Hire Date - C"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Hire Date - C"][4:])
            await page.wait_for_timeout(3000)

        if row["First Day of Work - C"] != "nan":
            await page.get_by_role("group").filter(
                has_text="First Day of Work"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["First Day of Work - C"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["First Day of Work - C"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["First Day of Work - C"][4:])
            await page.wait_for_timeout(3000)

        if row["Reason - C"] != "nan":
            await page.get_by_text("Reason").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Reason").fill(row["Reason - C"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            if await page.get_by_text("No matches found").nth(1).is_visible():
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/correct_{idx}.png",
                )
                return False

        if row["Employee Type - C"] != "nan":
            await page.get_by_text("Employee Type").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Employee Type").fill(
                row["Employee Type - C"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

        if (
            row["End Employment Date - C"] != "nan"
            and await page.get_by_text("End Employment Date").is_visible()
        ):
            await page.get_by_role("spinbutton", name="Month").nth(2).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["End Employment Date - C"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["End Employment Date - C"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["End Employment Date - C"][4:])
            await page.wait_for_timeout(3000)

        if row["Location - C"] != "nan":
            await page.get_by_text("Location", exact=True).click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Location").fill(row["Location - C"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            if await page.get_by_text("No matches found").nth(1).is_visible():
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/correct_{idx}.png",
                )
                return False

        if row["Job Profile - C"] != "nan":
            await page.get_by_text("Job Profile", exact=True).click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Job Profile").fill(
                row["Job Profile - C"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            if await page.get_by_text("No matches found").nth(1).is_visible():
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/correct_{idx}.png",
                )
                return False

        if row["Job Title - C"] != "nan":
            await page.get_by_role("textbox", name="Job Title").fill(
                row["Job Title - C"]
            )

        if row["Pay Rate Type - C"] != "nan":
            await page.get_by_text("Pay Rate Type").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Pay Rate Type").fill(
                row["Pay Rate Type - C"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

        if row["Time Type - C"] != "nan":
            await page.get_by_text("Time Type").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Time Type").fill(
                row["Time Type - C"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

        if row["Default Weekly Hours - C"] != "nan":
            await page.get_by_role("textbox", name="Default Weekly Hours").fill(
                row["Default Weekly Hours - C"]
            )

        if row["Scheduled Weekly Hours - C"] != "nan":
            await page.get_by_role("textbox", name="Scheduled Weekly Hours").fill(
                row["Scheduled Weekly Hours - C"]
            )

        if row["Work Shift - C"] != "nan":
            await page.get_by_text("Work Shift").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Work Shift").fill(
                row["Work Shift - C"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            if await page.get_by_text("No matches found").nth(1).is_visible():
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/correct_{idx}.png",
                )
                return False

        if row["Company Service Date - C"] != "nan":
            await page.locator("li").filter(
                has_text="Company Service Date"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Company Service Date - C"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Company Service Date - C"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Company Service Date - C"][4:])
            await page.wait_for_timeout(3000)

        if row["Comment on corrections"] != "nan":
            await page.get_by_role("textbox", name="enter your comment").fill(
                row["Comment on corrections"]
            )
            await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)
        if await page.get_by_role("button", name="Submit").is_visible():
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(10000)
        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/correct_{idx}.png"
            )
            safe_print("Error widget appeared with errors after submission.")
            return False
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/correct_{idx}.png"
        )
        safe_print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/correct_{idx}.png",
            full_page=True,
        )
        safe_print(error)  # Reraise the error after taking the screenshot
        return False
