from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Rescind"] == "Yes":
        return True
    if row["Correction"] == "Yes":
        return True

    await login(page, expect, env, user_id, idx)
    try:
        if "promotion" not in row["Why making this changes?"].lower():
            return True

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
            timeout=60000
        )
        await page.get_by_role("link", name=f"({row["WWID"]})").click()

        await expect(page.get_by_text("Actions").first).to_be_visible(timeout=60000)
        await page.get_by_text("Actions").first.click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_text("View Worker History")).to_be_visible(
            timeout=60000
        )
        await page.get_by_text("View Worker History").click()
        await expect(page.get_by_text("View Worker History", exact=True)).to_be_visible(
            timeout=60000
        )
        await page.wait_for_timeout(3000)

        # Status filter

        await expect(
            page.get_by_role("button", name="Status Sort and filter column")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="Status Sort and filter column").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").fill("In Progress")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()

        # effective date filter
        await page.get_by_role("button", name="Effective Date Sort and").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        effective_date = row["Effective Date"]
        effective_date = effective_date.replace("/", "")
        await page.keyboard.type(effective_date[:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(effective_date[2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(effective_date[4:])
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)

        #  #Business process filter
        # await page.get_by_role("button", name="Business Process Sort and").click()

        # await page.wait_for_timeout(3000)
        # await page.get_by_role("textbox", name="Value").fill("Compensation change")
        # await page.wait_for_timeout(3000)
        # await page.keyboard.press("Enter")
        # await page.wait_for_timeout(3000)
        # await page.get_by_role("button", name="Filter", exact=True).click()
        # await page.wait_for_timeout(3000)
        # await page.get_by_role("button", name="Filter", exact=True).click()
        # await page.wait_for_timeout(3000)

        cname = f"Compensation Change: {row["Full Name"]}"
        if (
            await page.get_by_role("row", name=cname)
            .get_by_label("Related Actions ALEJANDRO")
            .first.is_visible()
        ):
            await page.get_by_role("row", name=cname).get_by_label(
                "Related Actions ALEJANDRO"
            ).click()
            await page.wait_for_timeout(3000)
            await page.get_by_text("Start Proxy").click()
            await page.wait_for_timeout(3000)

            await page.get_by_role("button", name="OK").click()
            await expect(
                page.get_by_role("heading", name="Awaiting Your Action")
            ).to_be_visible(timeout=15000)

            await page.get_by_role("button", name="My Tasks Items").click()

        work_authorisation_name = f"Compensation Change: {row['Full Name']}"

        await expect(
            page.locator(
                '[data-automation-id="titleText"]', has_text=work_authorisation_name
            ).first
        ).to_be_visible(timeout=15000)
        await page.locator(
            '[data-automation-id="titleText"]', has_text=work_authorisation_name
        ).first.click()

        # comp_button = page.get_by_role("button", name=work_authorisation_name)

        # # Wait for the first matching button to be visible
        # await expect(comp_button.nth(0)).to_be_visible(timeout=15000)

        # Click the first matching button
        # await comp_button.nth(0).click()

        # Wait for 3 seconds
        await page.wait_for_timeout(3000)

        # submit
        await page.get_by_role("button", name="Approve").click()
        await page.wait_for_timeout(10000)

        if page.get_by_text("Success!").is_visible():
            await page.wait_for_timeout(5000)
            popup_header_selector = page.get_by_role("dialog").nth(0)

            if await popup_header_selector.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_compensation_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True

        if (
            await page.get_by_role("button", name="Approve").is_visible()
            and await page.locator(
                '[data-automation-id="titleText"]', has_text=work_authorisation_name
            ).first.is_visible()
        ):
            await page.wait_for_timeout(5000)
            await page.get_by_role("button", name="Approve").click()

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").first.is_visible()
        ):
            await page.wait_for_timeout(5000)
            await page.click(error_widget_selector)
            await page.wait_for_timeout(3000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_compensation_{idx}.png"
            )
            print("Error widget appeared with errors after submission.")
            return False
        else:
            popup_header_selector = page.get_by_role("dialog").nth(0)
            await page.wait_for_timeout(3000)

            if await popup_header_selector.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_compensation_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True

    except Exception as error:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_compensation_{idx}.png"
        )
        print(f"Error: {error}")
        return False
