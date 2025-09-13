from ..login import login
import os


async def Aimbyl_approval(page, expect, env, user_id, idx, row):
    try:

        await page.get_by_role("button", name="Related Actions Aimbyl").click()
        await page.wait_for_timeout(3000)

        await page.get_by_text("Start Proxy").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=15000)

        await page.get_by_role("button", name="My Tasks Items").click()

        if "promotion" in row["Why making this changes?"].lower():
            # Do something if it contains "promotion"
            work_authorisation_name = f"Promotion: {row["Full Name"]}"
        elif "demotion" in row["Why making this changes?"].lower():
            # Do something if it contains "promotion"
            work_authorisation_name = f"Demotion: {row["Full Name"]}"

        elif "Lateral Move" in row["Why making this changes?"]:
            work_authorisation_name = f"Lateral Move: {row["Full Name"]}"
        else:
            work_authorisation_name = f"Data Change: {row["Full Name"]}"

        await expect(
            page.get_by_role("button", name=work_authorisation_name).first
        ).to_be_visible(timeout=15000)
        await page.get_by_role("button", name=work_authorisation_name).first.click()
        await page.wait_for_timeout(5000)
        await page.get_by_role("button", name="Approve").click()
        await page.wait_for_timeout(10000)
        if page.get_by_text("Success!").first.is_visible():
            popup_header_selector = page.get_by_role("dialog").nth(0)

            if await popup_header_selector.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_approval_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True

        if (
            await page.get_by_role("button", name="Approve").is_visible()
            and await page.get_by_role(
                "button", name=work_authorisation_name
            ).first.is_visible()
        ):
            await page.wait_for_timeout(5000)
            await page.get_by_role("button", name="Approve").click()
            await page.wait_for_timeout(10000)

    except Exception as error:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_approval_{idx}.png"
        )
        print(f"Error: {error}")
        return False


async def stage_approval(page, expect, env, user_id, idx, row):
    try:

        if await page.get_by_text("Start Proxy").is_visible():
            await page.get_by_text("Start Proxy").click()
        else:
            await page.get_by_role("button", name="Close", exact=True).click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Related Actions").nth(4).click()
            await page.get_by_text("Start Proxy").click()
            await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=15000)

        await page.get_by_role("button", name="My Tasks Items").click()

        if row["Why making this changes?"].split(":")[0].strip().lower() in (
            "promotion",
            "demotion",
        ):
            work_authorisation_name = (
                str(row["Why making this changes?"]).split(":")[0].strip()
            )
        elif "Lateral Move" in row["Why making this changes?"]:
            work_authorisation_name = f"Lateral Move: {row["Full Name"]}"
        else:
            work_authorisation_name = f"Data Change: {row["Full Name"]}"

        await expect(
            page.get_by_role("button", name=work_authorisation_name).first
        ).to_be_visible(timeout=15000)
        await page.get_by_role("button", name=work_authorisation_name).first.click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Approve").click()
        await page.wait_for_timeout(10000)

        if page.get_by_text("Success!").is_visible():
            await page.wait_for_timeout(10000)
            popup_header_selector = page.get_by_role("dialog").nth(0)

            if await popup_header_selector.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_approval_{idx}.png"
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

    except Exception as error:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_approval_{idx}.png"
        )
        print(f"Error: {error}")
        return False


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

        # if Aimbyl found
        if await page.get_by_role("button", name="Related Actions Aimbyl").is_visible():
            await Aimbyl_approval(page, expect, env, user_id, idx, row)

        else:
            await expect(
                page.get_by_role("button", name="Related Actions").nth(2)
            ).to_be_visible(timeout=15000)
            await page.get_by_role("button", name="Related Actions").nth(2).click()
            await page.wait_for_timeout(3000)

            # if start proxy visible
            if await page.get_by_text("Start Proxy").is_visible():
                await page.get_by_text("Start Proxy").click()
                await page.wait_for_timeout(3000)
            else:
                await page.get_by_role("button", name="Close", exact=True).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Related Actions").nth(3).click()
                await page.wait_for_timeout(3000)
                await page.get_by_text("Start Proxy").click()
                await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="OK").click()
            await expect(
                page.get_by_role("heading", name="Awaiting Your Action")
            ).to_be_visible(timeout=15000)

            await page.get_by_role("button", name="My Tasks Items").click()

            if row["Why making this changes?"].split(":")[0].strip().lower() in (
                "promotion",
                "demotion",
            ):
                work_authorisation_name = (
                    str(row["Why making this changes?"]).split(":")[0].strip()
                )
            elif "Lateral Move" in row["Why making this changes?"]:
                work_authorisation_name = f"Lateral Move: {row["Full Name"]}"
            else:
                work_authorisation_name = f"Data Change: {row["Full Name"]}"

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

        # jump to maintain employee contract
        if (
            await page.get_by_label(
                "Aimbyl Ava Guillermo | Maintain Employee Contract"
            ).is_visible()
            or await page.get_by_text("Maintain Employee Contract").first.is_visible()
        ):
            await page.wait_for_timeout(5000)
            popup_header_selector = page.get_by_role("dialog").first

            if await popup_header_selector.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_approval_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True

        # jump to To Do:Edit ID
        if await page.get_by_label("Global Mobility Partner | To").is_visible():
            await page.wait_for_timeout(5000)
            popup_header_selector = page.get_by_role("dialog").first

            if await popup_header_selector.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_approval_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True

        # second approval
        if await page.get_by_label("Up Next:").is_visible():
            await page.wait_for_timeout(3000)
            await page.get_by_role("combobox", name="Search Workday").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("combobox", name="Search Workday").fill(row["WWID"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

            # Click on "Employee" link
            await expect(
                page.get_by_role("link", name=f"({row["WWID"]})")
            ).to_be_visible(timeout=15000)
            await page.get_by_role("link", name=f"({row["WWID"]})").click()

            await expect(page.get_by_text("Actions").first).to_be_visible(timeout=15000)
            await page.get_by_text("Actions").first.click()
            await page.wait_for_timeout(3000)

            # Add reason
            await page.get_by_text("Job Change").click()
            await page.wait_for_timeout(3000)
            await expect(page.get_by_text("Change Job", exact=True)).to_be_visible(
                timeout=15000
            )
            await page.get_by_text("Change Job", exact=True).click()
            await page.wait_for_timeout(3000)
            if await page.get_by_role(
                "button", name="Related Actions Aimbyl"
            ).is_visible():
                await Aimbyl_approval(page, expect, env, user_id, idx, row)
            else:
                await page.wait_for_timeout(5000)
                await page.get_by_role("button", name="Related Actions").nth(3).click()
                await page.wait_for_timeout(3000)
                await stage_approval(page, expect, env, user_id, idx, row)

        # third approval
        if await page.get_by_label("Up Next:").is_visible():
            await page.wait_for_timeout(3000)
            await page.get_by_role("combobox", name="Search Workday").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("combobox", name="Search Workday").fill(row["WWID"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

            # Click on "Employee" link
            await expect(
                page.get_by_role("link", name=f"({row["WWID"]})")
            ).to_be_visible(timeout=15000)
            await page.get_by_role("link", name=f"({row["WWID"]})").click()

            await expect(page.get_by_text("Actions").first).to_be_visible(timeout=15000)
            await page.get_by_text("Actions").first.click()
            await page.wait_for_timeout(3000)

            # Add reason
            await page.get_by_text("Job Change").click()
            await page.wait_for_timeout(3000)
            await expect(page.get_by_text("Change Job", exact=True)).to_be_visible(
                timeout=15000
            )
            await page.get_by_text("Change Job", exact=True).click()
            await page.wait_for_timeout(3000)
            if await page.get_by_role(
                "button", name="Related Actions Aimbyl"
            ).is_visible():
                await Aimbyl_approval(page, expect, env, user_id, idx, row)
            else:
                await page.get_by_role("button", name="Related Actions").nth(3).click()
                await page.wait_for_timeout(3000)
                await stage_approval(page, expect, env, user_id, idx, row)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").first.is_visible()
        ):
            await page.wait_for_timeout(5000)
            await page.click(error_widget_selector)
            await page.wait_for_timeout(10000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_approval_{idx}.png"
            )
            print("Error widget appeared with errors after submission.")
            return False
        else:
            await page.wait_for_timeout(10000)
            popup_header_selector = page.get_by_role("dialog").first

            if await popup_header_selector.is_visible():
                await page.wait_for_timeout(10000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_approval_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True
    except Exception as error:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_approval_{idx}.png"
        )
        print(f"Error: {error}")
        return False
