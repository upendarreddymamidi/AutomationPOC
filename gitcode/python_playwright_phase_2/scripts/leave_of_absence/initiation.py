from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Want to Rescind?"] == "Yes" or row["Want to Correct?"] == "Yes":
        return True
    await login(page, expect, env, user_id, idx)

    try:
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("combobox", name="Search Workday").click()
        await page.wait_for_timeout(2000)
        await page.get_by_role("combobox", name="Search Workday").fill(
            "place worker on leave"
        )
        await page.keyboard.press("Enter")
        await expect(
            page.get_by_role("link", name="Place Worker on Leave")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("link", name="Place Worker on Leave").click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_role("textbox", name="Worker")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("textbox", name="Worker").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["WWID"])
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_text("Place Worker on Leave")).to_be_visible(
            timeout=60000
        )
        if row["Last Day of Work current"] != "nan":
            await page.get_by_role(
                "group", name="Last Day of Work current"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Last Day of Work current"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Last Day of Work current"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Last Day of Work current"][4:])
            await page.wait_for_timeout(3000)

        if row["First Day of Leave current"] != "nan":
            await page.get_by_role(
                "group", name="First Day of Leave current"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["First Day of Leave current"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["First Day of Leave current"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["First Day of Leave current"][4:])
            await page.wait_for_timeout(3000)

        if row["Estimated Last Day of Leave"] != "nan":
            await page.get_by_role(
                "group", name="Estimated Last Day of Leave"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Estimated Last Day of Leave"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Estimated Last Day of Leave"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Estimated Last Day of Leave"][4:])
            await page.wait_for_timeout(3000)

        if row["Leave Type"] != "nan":
            await page.get_by_role("textbox", name="Leave Type").fill(row["Leave Type"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

        if await page.get_by_role("textbox", name="Leave Reason").is_visible():
            await page.get_by_role("textbox", name="Leave Reason").fill(
                row["Leave Reason"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

        if country == "Mexico":

            if await page.get_by_role(
                "textbox", name="Social Security Disability"
            ).is_visible():
                await page.get_by_role(
                    "textbox", name="Social Security Disability"
                ).fill(row["Social Security Disability"])
                await page.wait_for_timeout(3000)

            if await page.get_by_role("textbox", name="Case Number").is_visible():
                await page.get_by_role("textbox", name="Case Number").fill(
                    row["Case Number"]
                )
                await page.wait_for_timeout(3000)

        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)
        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/initiation_{idx}.png"
            )
            print("Widget error")
            return False
        await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
        await page.wait_for_timeout(3000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/initiation_{idx}.png"
        )
        print("Submission confirmation popup is visible and screenshot taken.")
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/initiation_{idx}.png",
            full_page=True,
        )
        print(error)
        return False
