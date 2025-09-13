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
        name = (await page.text_content("h1")).strip()
        await page.get_by_text("Actions").click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_text("View Worker History")).to_be_visible(
            timeout=60000
        )
        await page.get_by_text("View Worker History").click()
        await page.wait_for_timeout(3000)

        await expect(
            page.get_by_role("button", name="Status Sort and filter column")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="Status Sort and filter column").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").fill("Success")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Effective Date Sort and").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(9000)
        await page.keyboard.type(
            row["Effective Date of the process you want to correct?"][:2]
        )
        await page.wait_for_timeout(3000)
        await page.keyboard.type(
            row["Effective Date of the process you want to correct?"][2:4]
        )
        await page.wait_for_timeout(3000)
        await page.keyboard.type(
            row["Effective Date of the process you want to correct?"][4:]
        )
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)

        await page.get_by_role("link", name=f"One-Time Payment: {name}").first.click()
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

        if row["Effective Date - C"] != "nan":
            await page.get_by_role("group", name="Effective Date").get_by_placeholder(
                "MM"
            ).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Effective Date - C"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Effective Date - C"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Effective Date - C"][4:])
            await page.wait_for_timeout(3000)

        if row["Reason - C"] != "nan":
            await page.locator("label").filter(has_text="Reason").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Reason").fill(row["Reason - C"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

        await page.locator("td").filter(has_text="*Plan").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").fill(
            row["Which OTP plan you want to correct?"]
        )
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()

        await page.wait_for_timeout(3000)
        await page.get_by_role("cell").filter(has_text="Coverage Period").first.click()
        await page.wait_for_timeout(3000)

        if row["One-Time Payment Plan - C"] != "nan":
            await page.get_by_role("option", name="press delete to clear").nth(
                1
            ).click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Plan").fill(
                row["One-Time Payment Plan - C"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

        if row["Schedule Payment Date - C"] != "nan":
            await page.get_by_role("group", name="current value").get_by_placeholder(
                "MM"
            ).nth(1).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Schedule Payment Date - C"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Schedule Payment Date - C"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Schedule Payment Date - C"][4:])
            await page.wait_for_timeout(3000)

        if row["Currency - C"] != "nan":
            await page.get_by_role("option", name="press delete to clear").nth(
                2
            ).click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Currency").fill(row["Currency - C"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

        if row["Amount - C"] != "nan":
            await page.locator('[id="56$11291-input"]').fill(row["Amount - C"])
            await page.wait_for_timeout(3000)

        await page.get_by_role("textbox", name="enter your comment").fill(
            row["Comment for correction"]
        )
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/correction_{idx}.png"
            )
            print("Widget error")
            return False
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/correction_{idx}.png"
        )
        print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/correction_{idx}.png",
            full_page=True,
        )
        print(error)
        return False
