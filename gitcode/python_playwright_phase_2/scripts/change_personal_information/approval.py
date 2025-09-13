from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["What Change you want to make?"] != "Name":
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

        # Click on Employee link
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
        await page.get_by_role("textbox", name="Value").fill("In Progress")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Effective Date Sort and").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(9000)
        await page.keyboard.type(row["Effective Date for Name"][:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date for Name"][2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date for Name"][4:])
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Business Process Filter column").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").fill(
            f"Legal Name Change: {name}"
        )
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)

        i = 2
        while not await page.get_by_role("menuitem", name="Start Proxy").is_visible():
            await page.get_by_role("button", name="Related Actions").nth(i).click()
            await page.wait_for_timeout(3000)
            if await page.get_by_role("menuitem", name="Start Proxy").is_visible():
                await page.get_by_role("menuitem", name="Start Proxy").click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="OK").click()
                await page.wait_for_timeout(3000)
                break
            await page.get_by_role("button", name="Close", exact=True).click()
            await page.wait_for_timeout(3000)
            i += 1

        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=60000)

        await page.get_by_role("button", name="My Tasks Items").click()
        button_name = f"Legal Name Change:"
        await expect(
            page.get_by_role("button", name=f"({row["WWID"]})")
            .filter(has_text=button_name)
            .first
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name=f"({row["WWID"]})").filter(
            has_text=button_name
        ).first.click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Approve").click()

        await page.wait_for_timeout(10000)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector) and not (
            await page.get_by_role("dialog").first.is_visible()
        ):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/approval_{idx}.png"
            )
            print("Widget error")
            return False
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/approval_{idx}.png"
        )
        print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/approval_{idx}.png",
            full_page=True,
        )
        print(error)
        return False
