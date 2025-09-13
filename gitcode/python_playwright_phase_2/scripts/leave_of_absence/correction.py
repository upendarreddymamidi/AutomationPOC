from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Want to Correct?"] != "Yes":
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
        await page.keyboard.type(row["Effective Date for Correct"][:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date for Correct"][2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date for Correct"][4:])
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)

        await page.get_by_text(f"Leave Request: {name}").first.click()
        await page.wait_for_timeout(10000)
        await page.get_by_role("button", name="Related Actions").nth(2).click()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Business Process").hover()
        await page.wait_for_timeout(3000)

        await page.get_by_text("Correct").click()
        await expect(
            page.get_by_text("Correct Business Process", exact=True)
        ).to_be_visible(timeout=60000)

        if row["Last Day of Work current - C"] != "nan":
            await page.get_by_role("group", name="Last Day of Work").get_by_placeholder(
                "MM"
            ).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Last Day of Work current - C"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Last Day of Work current - C"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Last Day of Work current - C"][4:])
            await page.wait_for_timeout(3000)

        if row["First Day of Leave current - C"]:
            await page.get_by_role(
                "group", name="First Day of Leave"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["First Day of Leave current - C"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["First Day of Leave current - C"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["First Day of Leave current - C"][4:])
            await page.wait_for_timeout(3000)

        if row["Estimated Last Day of Leave - C"] != "nan":
            await page.get_by_role(
                "group", name="Estimated Last Day of Leave"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Estimated Last Day of Leave - C"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Estimated Last Day of Leave - C"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Estimated Last Day of Leave - C"][4:])
            await page.wait_for_timeout(3000)

        if row["Leave Type - C"] != "nan":
            await page.get_by_role(
                "listbox", name="items selected for Leave Type"
            ).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Leave Type - C"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            if await page.get_by_text("No matches found").nth(1).is_visible():
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/correction_{idx}.png",
                )
                return False

        if (
            await page.locator("label").filter(has_text="Leave Reason").is_visible()
            and row["Leave Reason - C"] != "nan"
        ):
            await page.locator("label").filter(has_text="Leave Reason").click()
            await page.keyboard.type(row["Leave Reason - C"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            if await page.get_by_text("No matches found").nth(1).is_visible():
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/correction_{idx}.png",
                )
                return False

        if country in ["Mexico"]:

            if (
                await page.get_by_role(
                    "textbox", name="Social Security Disability"
                ).is_visible()
                and row["Social Security Disability - C"]
            ):
                await page.get_by_role(
                    "textbox", name="Social Security Disability"
                ).fill(row["Social Security Disability - C"])
                await page.wait_for_timeout(3000)

            if (
                await page.get_by_role("textbox", name="Case Number").is_visible()
                and row["Case Number - C"]
            ):
                await page.get_by_role("textbox", name="Case Number").fill(
                    row["Case Number - C"]
                )
                await page.wait_for_timeout(3000)

        if row["Comment for Correct"] != "nan":
            await page.get_by_role("textbox", name="enter your comment").fill(
                row["Comment for Correct"]
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
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=15000)
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
