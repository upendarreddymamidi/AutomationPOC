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
        else:
            name = f"{row["First Name"]} {row["Last Name"]}"
            if row["Second Last Name"] != "nan":
                name += f" {row["Second Last Name"]}"
            if row["Married Last Name"] != "nan":
                name += f" {row["Married Last Name"]}"

        await page.get_by_role("button", name="My Tasks Items").click()
        payment_button_name = f"One-Time Payment: {name}"
        await expect(
            page.get_by_role("button", name=payment_button_name).first
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name=payment_button_name).first.click()
        await page.wait_for_timeout(3000)

        if row["OTP Reason"] != "nan":
            await expect(page.get_by_role("button", name="Edit Summary")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("button", name="Edit Summary").click()
            await page.wait_for_timeout(3000)
            if await page.get_by_role("textbox", name="Reason").is_visible():
                await page.get_by_role("textbox", name="Reason").click()

            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["OTP Reason"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Save Summary").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Add", exact=True).click()
            await page.wait_for_timeout(3000)
            await expect(page.get_by_text("Organizational Assignments")).to_be_visible(
                timeout=60000
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="One-Time Payment Plan").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["One-Time Payment Plan"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            ## Schedule payment date
            if row["Schedule Payment Date"] != "nan":
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Schedule Payment Date"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Schedule Payment Date"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Schedule Payment Date"][4:])
                await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Amount").fill(row["OTP Amount"])
            await page.wait_for_timeout(3000)
            if await page.get_by_role(
                "listbox", name="item selected for Currency"
            ).is_visible():
                await page.get_by_role(
                    "listbox", name="item selected for Currency"
                ).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["OTP Currency"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            await page.get_by_role(
                "button", name="Save Organizational Assignments"
            ).click()
            await page.wait_for_timeout(3000)
        await page.get_by_text("Submit").click()
        await page.wait_for_timeout(10000)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").is_visible()
        ):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/request_one_time_payment_error_{idx}.png"
            )
            safe_print("Error widget appeared with errors after submission.")
            return False
        await expect(page.get_by_role("dialog")).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/request_one_time_payment_confirmation_{idx}.png"
        )
        safe_print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/request_one_time_payment_error_{idx}.png",
            full_page=True,
        )
        safe_print(error)  # Reraise the error after taking the screenshot
        return False
