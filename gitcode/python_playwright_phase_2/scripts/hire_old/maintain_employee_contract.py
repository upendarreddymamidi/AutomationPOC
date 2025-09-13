from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    if country != "United States of America":
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
            contract_button_name = f"Contract: {row["First Name"]} {row["Last Name"]}"
            await expect(
                page.get_by_role("button", name=contract_button_name).first
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name=contract_button_name).first.click()
            await page.wait_for_timeout(3000)
            await expect(
                page.get_by_role("textbox", name="Contract Type")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("textbox", name="Contract Type").click()
            await page.get_by_role("textbox", name="Contract Type").fill(
                row["Contract Type"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            if row["Contract Type"] == "Fixed Term Contract":
                await page.locator('[data-automation-id="dateSectionMonth-input"]').nth(
                    3
                ).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Contract End date"])
            await page.get_by_role("textbox", name="Status").click()
            await page.get_by_role("textbox", name="Status").fill(row["Status"])
            await page.get_by_role("textbox", name="Status").press("Enter")
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(5000)
            error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
            if await page.is_visible(error_widget_selector) and not (
                await page.get_by_role("dialog").first.is_visible()
            ):
                await page.click(error_widget_selector)
                await page.wait_for_timeout(2000)
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/maintain_employee_contract_error_{idx}.png"
                )
                print("Error widget appeared with errors after submission.")
                return False
            await expect(page.get_by_role("dialog").first).to_be_visible(timeout=60000)
            await page.wait_for_timeout(3000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/maintain_employee_contract_confirmation_{idx}.png"
            )
            print("Submission confirmation popup is visible and screenshot taken.")
            return True
        except Exception as error:
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/maintain_employee_contract_error_{idx}.png",
                full_page=True,
            )
            print(error)  # Reraise the error after taking the screenshot
            return False
    else:
        return True
