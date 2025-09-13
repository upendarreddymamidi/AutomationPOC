from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    if country == "Mexico" and env.split("-")[1] == "jj1":
        return True
    await login(page, expect, env, user_id, idx)
    try:
        await page.get_by_role("combobox", name="Search Workday").fill(
            "Start Proxy"
        )
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

        await page.get_by_role("button", name="My Tasks Items").click()
        id_button_name = f"ID Change: {row["First Name"]} {row["Last Name"]}"
        await expect(
            page.get_by_role("button", name=id_button_name).first
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name=id_button_name).first.click()
        await page.wait_for_timeout(3000)

        add_row_locator = (
            page.locator("tbody")
            .filter(has_text="*Country*National ID")
            .get_by_label("Add Row")
        )

        await expect(add_row_locator).to_be_visible(timeout=60000)
        await add_row_locator.click()
        await page.get_by_role("textbox", name="Country").click()
        await page.keyboard.type(row["Identification Country 1"])
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")

        await page.get_by_role("textbox", name="National ID Type").click()
        await page.keyboard.type(row["National ID Type1"])
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")

        await page.locator('input[data-automation-id="textInputBox"]').click()
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Control+A")
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["ID value1"])

        if row["Issued Date"] != "nan":
            await page.wait_for_timeout(3000)
            await expect(
                page.get_by_role("cell")
                .filter(has_text="current value is MM/DD/YYYY//")
                .first.get_by_role("spinbutton", name="Month")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("cell").filter(
                has_text="current value is MM/DD/YYYY//"
            ).first.get_by_role("spinbutton", name="Month").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Issued Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Issued Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Issued Date"][4:])
            await page.wait_for_timeout(3000)

        if row["Expiration Date"] != "nan":
            await page.wait_for_timeout(3000)
            await expect(
                page.get_by_role("cell")
                .filter(has_text="current value is MM/DD/YYYY//")
                .nth(1)
                .get_by_role("spinbutton", name="Month")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("cell").filter(
                has_text="current value is MM/DD/YYYY//"
            ).nth(1).get_by_role("spinbutton", name="Month").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Expiration Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Expiration Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Expiration Date"][4:])
            await page.wait_for_timeout(3000)

        if row["Comment"] != "nan":
            await expect(
                page.get_by_role("textbox", name="enter your comment")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("textbox", name="enter your comment").fill(
                row["Comment"]
            )

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
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/edit_ids_error_{idx}.png"
            )
            print("Widget error")
            return False
        else:
            await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
            await page.wait_for_timeout(3000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/edit_ids_confirmation_{idx}.png"
            )
            print("Submission confirmation popup is visible and screenshot taken.")
            return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/edit_ids_error_{idx}.png",
            full_page=True,
        )
        print(error)  # Reraise the error after taking the screenshot
        return False
