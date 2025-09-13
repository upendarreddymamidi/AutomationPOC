from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Rescind"] == "Yes":
        return True

    if row["Correction"] == "Yes":
        return True

    if (
        "add" in row["Why making this changes?"].lower()
        or "close" in row["Why making this changes?"].lower()
    ):
        return True
    if row["Different Country Lateral Move"] != "Yes":
        return True

    await login(page, expect, env, user_id, idx)
    try:

        # Approval by manager
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").fill(row["WWID"])
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # Click on "Employee" link
        await expect(page.get_by_role("link", name=f"({row["WWID"]})")).to_be_visible(
            timeout=15000
        )
        await page.get_by_role("link", name=f"({row["WWID"]})").click()

        await expect(page.get_by_text("Actions").first).to_be_visible(timeout=15000)
        await page.get_by_text("Actions").first.click()
        await page.wait_for_timeout(3000)

        # Start proxy
        await page.get_by_text("Job Change").click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_text("Change Job", exact=True)).to_be_visible(
            timeout=15000
        )
        await page.get_by_text("Change Job", exact=True).click()
        await page.wait_for_timeout(3000)

        await expect(
            page.get_by_role("button", name="Related Actions").nth(4)
        ).to_be_visible(timeout=15000)
        await page.get_by_role("button", name="Related Actions").nth(4).click()
        await page.wait_for_timeout(3000)

        # if start proxy visible
        if await page.get_by_text("Start Proxy").is_visible():
            await page.get_by_text("Start Proxy").click()
            await page.wait_for_timeout(3000)
        else:
            await page.get_by_role("button", name="Close", exact=True).click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Related Actions").nth(5).click()
            await page.wait_for_timeout(3000)
            await page.get_by_text("Start Proxy").click()
            await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=15000)

        await page.get_by_role("button", name="My Tasks Items").click()

        work_authorisation_name = f"Lateral Move: {row["Full Name"]}"

        await expect(
            page.get_by_role("button", name=work_authorisation_name).first
        ).to_be_visible(timeout=15000)
        await page.get_by_role("button", name=work_authorisation_name).first.click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Approve").click()
        await page.wait_for_timeout(10000)
        if await page.get_by_text("Approved").first.is_hidden():
            await page.get_by_role("button", name="Approve").click()
            await page.wait_for_timeout(10000)

        if await page.get_by_text("Success!").is_visible():
            await page.wait_for_timeout(10000)
            popup_header_selector = page.get_by_role("dialog").nth(0)

            if await popup_header_selector.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_Alternate_approval_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True

        if (
            await page.get_by_role("button", name="Approve").is_visible()
            and await page.get_by_role(
                "button", name=work_authorisation_name
            ).first.is_visible()
        ):
            await page.wait_for_timeout(10000)
            await page.get_by_role("button", name="Approve").click()
            await page.wait_for_timeout(10000)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").first.is_visible()
        ):
            await page.wait_for_timeout(5000)
            await page.click(error_widget_selector)
            await page.wait_for_timeout(10000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_Alternate_approval_{idx}.png"
            )
            print("Error widget appeared with errors after submission.")
            return False
        else:
            await page.wait_for_timeout(10000)
            popup_header_selector = page.get_by_role("dialog").first

            if await popup_header_selector.is_visible():
                await page.wait_for_timeout(10000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_Alternate_approval_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True
    except Exception as error:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_Alternate_approval_{idx}.png"
        )
        print(f"Error: {error}")
        return False
