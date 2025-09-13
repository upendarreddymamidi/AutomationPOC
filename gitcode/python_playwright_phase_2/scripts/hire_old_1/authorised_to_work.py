from ..login import login
import os
from helpers.encoding import safe_print

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

        if country in ["Japan"]:
            name = f"{row["Given Name - Western Script"]} {row["Family Name - Western Script"]}"
            work_authorisation_name = f"Authorized to Work: Hire: {name}"
        else:
            name = f"{row["First Name"]} {row["Last Name"]}"
            if row["Second Last Name"] != "nan":
                name += f" {row["Second Last Name"]}"
            if row["Married Last Name"] != "nan":
                name += f" {row["Married Last Name"]}"
            work_authorisation_name = (
                f"Authorized to Work: Hire: {name} - {row["Job Posting Title"]}"
            )

        await page.get_by_role("button", name="My Tasks Items").click()

        await expect(
            page.get_by_role("button", name=work_authorisation_name).first
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name=work_authorisation_name).first.click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/authorisation_to_work_confirmation_{idx}.png"
        )
        safe_print("Submission confirmation popup is visible and screenshot taken.")
        return True

    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/authorisation_to_work_error_{idx}.png",
            full_page=True,
        )
        safe_print(error)  # Reraise the error after taking the screenshot
        return False
