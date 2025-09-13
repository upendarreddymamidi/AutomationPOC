from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Rescind"] != "Yes":
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
        await page.get_by_role("button", name="Initiated On Sort and filter").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter Condition").click()
        await page.wait_for_timeout(3000)
        await page.get_by_label("is on or after", exact=True).click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Initiated On"][:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Initiated On"][2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Initiated On"][4:])
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)
        await page.get_by_text(row["Rescind Process"]).first.click()
        await page.wait_for_timeout(10000)
        await page.get_by_role("button", name="Related Actions").nth(1).click()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Business Process").hover()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Rescind").click()
        await expect(
            page.get_by_text("Rescind Business Process", exact=True)
        ).to_be_visible(timeout=60000)
        await page.get_by_role("textbox", name="enter your comment").fill(
            row["Comment for Rescind"]
        )
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)

        popup_header_selector = page.get_by_role("dialog")
        if await popup_header_selector.is_visible():
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/change_personal_info_rescind_{idx}.png"
            )
            print("Submission confirmation popup is visible and screenshot taken.")
            return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_rescide_{idx}.png"
        )
        print(f"Error: {error}")
        return False
