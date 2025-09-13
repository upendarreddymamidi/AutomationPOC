from ..login import login
import os, re


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Want to rescind?"] != "Yes" or row["Want to correct?"] == "Yes":
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

        await page.get_by_role("button", name="Effective Date Sort and").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(
            row["Effective date of the process you want to rescind?"][:2]
        )
        await page.wait_for_timeout(3000)
        await page.keyboard.type(
            row["Effective date of the process you want to rescind?"][2:4]
        )
        await page.wait_for_timeout(3000)
        await page.keyboard.type(
            row["Effective date of the process you want to rescind?"][4:]
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

        await page.get_by_text("Rescind").click()
        await expect(
            page.get_by_text("Rescind Business Process", exact=True)
        ).to_be_visible(timeout=60000)
        await page.get_by_role("textbox", name="enter your comment").fill(
            row["Comment for rescind"]
        )
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/rescind_{idx}.png"
            )
            print("Widget error")
            return False
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=15000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/rescind_{idx}.png"
        )
        print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/rescind_{idx}.png",
            full_page=True,
        )
        print(error)
        return False
