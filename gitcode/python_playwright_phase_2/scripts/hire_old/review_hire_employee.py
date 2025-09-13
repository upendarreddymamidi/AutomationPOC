from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    await login(page, expect, env, user_id, idx)
    try:
        await page.wait_for_timeout(5000)
        await expect(page.locator('input[type="search"]')).to_be_visible(timeout=60000)
        await page.fill('input[type="search"]', "review hire employee")
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_text("Hire Employee", exact=True).click()
        await expect(
            page.get_by_role("textbox", name="Supervisory Organization", exact=True)
        ).to_be_visible(timeout=120000)
        await page.get_by_role(
            "textbox", name="Supervisory Organization", exact=True
        ).click()
        await page.keyboard.type(row["Supervisory Organization"])
        await page.wait_for_timeout(1000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(1000)
        await page.get_by_role(
            "radio", name="Create a New Pre-Hire", exact=True
        ).click()
        await page.wait_for_timeout(1000)
        await page.get_by_role("button", name="OK").click()

        if country == "Mexico":
            ## Given Name(s)
            await expect(
                page.get_by_role("textbox", name="Given Name(s)")
            ).to_be_visible(timeout=120000)
            await page.get_by_role("textbox", name="Given Name(s)").fill(
                row["First Name"]
            )
        elif country == "United States of America":
            ## First Name
            await expect(page.get_by_role("textbox", name="First Name")).to_be_visible(
                timeout=120000
            )
            await page.get_by_role("textbox", name="First Name").fill(row["First Name"])

        if country == "Mexico":
            ## Father's Family Name
            await expect(
                page.get_by_role("textbox", name="Father's Family Name")
            ).to_be_visible(timeout=30000)
            await page.get_by_role("textbox", name="Father's Family Name").fill(
                row["Last Name"]
            )
        elif country == "United States of America":
            ## Last Name
            await expect(page.get_by_role("textbox", name="Last Name")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("textbox", name="Last Name").fill(row["Last Name"])

        await page.get_by_role("tab", name="Contact Information").click()
        await page.get_by_role("button", name="Add Phone").click()
        await page.wait_for_timeout(2000)

        await page.get_by_role("textbox", name="country Phone Code").fill(
            row["Country Phone Code"]
        )
        await page.keyboard.press("Enter")
        await page.get_by_role("textbox", name="Phone Number").fill(row["Phone Number"])

        await page.get_by_role("button", name="Phone Device select one").click()
        await page.wait_for_timeout(2000)
        await page.get_by_role("option", name=row["Phone Device"]).click()
        await page.wait_for_timeout(1000)

        await page.get_by_role("textbox", name="Type").click()
        await page.keyboard.type(row["Type"])
        await page.keyboard.press("Enter")

        await page.get_by_role("button", name="Add Address").click()
        await page.wait_for_timeout(2000)

        await page.get_by_role("spinbutton", name="Month").click()
        await page.keyboard.type(row["Date"])

        await page.get_by_role("textbox", name="Address Line 1").fill(
            f"{row["Address Line 1"]} {row["Address Line 2"]}"
        )

        if country == "Mexico":
            # Neighborhood
            await page.get_by_role("textbox", name="Neighborhood").fill(
                row["Neighborhood"]
            )
        elif country == "United States of America":
            ## State
            await expect(page.get_by_role("textbox", name="State")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("textbox", name="State").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["State"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")

        await page.get_by_role("textbox", name="Postal Code").fill(row["Postal Code"])
        await page.get_by_role("textbox", name="City").fill(row["City"])

        await page.get_by_role("group", name="Address").get_by_label("Type").click()
        await page.keyboard.type(row["Address Type"])
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(1000)

        await page.get_by_role("option", name="Mailing, press delete to").locator(
            "svg"
        ).click()
        await page.get_by_role("option", name="Street Address, press delete").locator(
            "svg"
        ).click()
        await page.wait_for_timeout(1000)

        await page.keyboard.type("Permanent")
        await page.keyboard.press("Enter")

        await page.get_by_role("button", name="Add Email").click()
        await page.wait_for_timeout(2000)

        await expect(page.get_by_role("textbox", name="Email Address")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("textbox", name="Email Address").fill(
            row["Email Address"]
        )
        await page.get_by_role("group", name="Email").get_by_placeholder(
            "Search"
        ).click()
        await page.keyboard.type(row["Email Usage Type"])
        await page.keyboard.press("Enter")

        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(4000)

        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/hire.png"
            )
            print("Error widget appeared with errors after submission.")
            return False
        else:
            await page.get_by_role("spinbutton", name="Hire Date").click()
            await page.keyboard.type(row["Hire Date"])
            await page.get_by_role("textbox", name="Reason").click()
            await page.keyboard.type(row["Reason"])
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

            await page.get_by_role("textbox", name="Position", exact=True).click()
            await page.wait_for_timeout(3000)
            await page.get_by_text("Positions without Job Requisitions").first.click()
            await page.wait_for_timeout(3000)
            await page.get_by_text(row["Job Posting Title"]).first.click()
            await page.wait_for_timeout(3000)

            await page.get_by_role("textbox", name="Employee Type").click()
            await page.wait_for_timeout(2000)
            await page.keyboard.type(row["Employee Type"])
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(2000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

            if await page.get_by_role(
                "spinbutton", name="End Employment Date"
            ).is_visible():
                await page.get_by_role("spinbutton", name="End Employment Date").click()
                await page.keyboard.type(row["End Employment date"])

            await page.get_by_role("textbox", name="Job Title").click()
            await page.keyboard.press("Control+A")
            await page.keyboard.type(row["Job Title"])
            await page.wait_for_timeout(2000)

            if await page.get_by_role("listbox", name="Pay Rate Type").is_visible():
                await page.get_by_role("listbox", name="Pay Rate Type").click()

            elif await page.get_by_role("textbox", name="Pay Rate Type").is_visible():
                await page.get_by_role("textbox", name="Pay Rate Type").click()
            elif await page.get_by_role(
                "textbox", name="items selected for Pay Rate"
            ).is_visible():
                await page.get_by_role(
                    "textbox", name="items selected for Pay Rate"
                ).click()
            else:
                await page.get_by_role(
                    "listbox", name="items selected for Pay Rate"
                ).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Pay Rate Type"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

            if country == "Mexico":
                await page.get_by_role("textbox", name="Work Shift").click()
                await page.keyboard.type(row["Work Shift"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")

            await page.get_by_role("spinbutton", name="Company Service Date").click()
            await page.keyboard.type(row["Company Service Date"])
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(3000)

            if await page.is_visible(error_widget_selector):
                await page.click(error_widget_selector)
                await page.wait_for_timeout(2000)
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/hire_{idx}.png"
                )
                print("Error widget appeared with errors after submission.")
                return False
            else:
                await page.wait_for_timeout(10000)
                popup_header_selector = page.get_by_role(
                    "heading", name="You have submitted"
                )

                if await popup_header_selector.is_visible():
                    await page.screenshot(
                        path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/hire_{idx}.png"
                    )
                    print(
                        "Submission confirmation popup is visible and screenshot taken."
                    )
                    return True

    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/hire_{idx}.png"
        )
        print(error)  # Reraise the error after taking the screenshot
        return False
