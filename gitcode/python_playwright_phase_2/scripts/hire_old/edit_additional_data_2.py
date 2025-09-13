from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
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

        await page.get_by_role("button", name="My Tasks Items").click()
        edit_button_name = (
            f"Hire: {row["First Name"]} {row["Last Name"]} - {row["Job Posting Title"]}"
        )
        await expect(
            page.get_by_role("button", name=edit_button_name, exact=True).first
        ).to_be_visible(timeout=60000)
        await page.get_by_role(
            "button", name=edit_button_name, exact=True
        ).first.click()
        await page.wait_for_timeout(3000)
        if not (
            await page.get_by_role("heading", name="COMPANY CAR")
            .get_by_label("COMPANY CAR")
            .is_visible()
        ):
            await expect(
                page.get_by_role("button", name=edit_button_name, exact=True).nth(1)
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name=edit_button_name, exact=True).nth(
                1
            ).click()
            await page.wait_for_timeout(3000)
        await expect(
            page.get_by_role("heading", name="COMPANY CAR").get_by_label("COMPANY CAR")
        ).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(3000)
        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").first.is_visible()
        ):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/edit_additional_data_2_error_{idx}.png"
            )
            print("Widget error")
            return False
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/edit_additional_data_2_confirmation_{idx}.png"
        )
        print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/edit_additional_data_2_error_{idx}.png",
            full_page=True,
        )
        print(error)  # Reraise the error after taking the screenshot
        return False
