from ..login import login
import os
from helpers.encoding import safe_print


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Want to Rescind?"] == "Yes" or row["Want to correct?"] == "Yes":
        return True
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

        ## Allow Duplicate Name
        if row["Allow Duplicate Name"] == "Yes":
            await expect(page.get_by_text("Allow Duplicate Name").first).to_be_visible(
                timeout=120000
            )
            await page.get_by_text("Allow Duplicate Name").first.click()
            await page.wait_for_timeout(3000)

            ## Enter Western Script for JAPAN

        if row["Enter Western Script for Name"] == "Yes" and country in ["Japan"]:
            await expect(page.get_by_text("Enter Western Script").first).to_be_visible(
                timeout=120000
            )
            await page.get_by_text("Enter Western Script").first.click()
            await page.wait_for_timeout(3000)

        if country in ["Mexico", "Brazil"]:
            ## Given Name(s)
            await expect(
                page.get_by_role("textbox", name="Given Name(s)")
            ).to_be_visible(timeout=120000)
            await page.get_by_role("textbox", name="Given Name(s)").fill(
                row["First Name"]
            )
        elif country in ["United States of America", "Costa Rica"]:
            ## First Name
            await expect(
                page.get_by_role("textbox", name="First Name", exact=True)
            ).to_be_visible(timeout=120000)
            await page.get_by_role("textbox", name="First Name").fill(row["First Name"])

        if row["Middle Name"] != "nan":
            if page.get_by_role("textbox", name="Middle Name").is_visible():
                await page.get_by_role("textbox", name="Middle Name").fill(
                    row["Middle Name"]
                )

        if country in ["Mexico"]:
            ## Father's Family Name
            await expect(
                page.get_by_role("textbox", name="Father's Family Name")
            ).to_be_visible(timeout=30000)
            await page.get_by_role("textbox", name="Father's Family Name").fill(
                row["Last Name"]
            )
        elif country in ["United States of America"]:
            ## Last Name
            await expect(
                page.get_by_role("textbox", name="Last Name", exact=True)
            ).to_be_visible(timeout=60000)
            await page.get_by_role("textbox", name="Last Name", exact=True).fill(
                row["Last Name"]
            )
        elif country in ["Costa Rica"]:
            ## Last Name
            await expect(
                page.get_by_role("textbox", name="First Last Name", exact=True)
            ).to_be_visible(timeout=60000)
            await page.get_by_role("textbox", name="First Last Name", exact=True).fill(
                row["Last Name"]
            )
        elif country in ["Brazil"]:
            ## Family Name
            await expect(
                page.get_by_role("textbox", name="Family Name", exact=True)
            ).to_be_visible(timeout=60000)
            await page.get_by_role("textbox", name="Family Name", exact=True).fill(
                row["Last Name"]
            )

        if country in ["Costa Rica"]:
            if row["Second Last Name"] != "nan":
                await expect(
                    page.get_by_role("textbox", name="Second Last Name")
                ).to_be_visible(timeout=60000)
                await page.get_by_role("textbox", name="Second Last Name").fill(
                    row["Second Last Name"]
                )
            if row["Married Last Name"] != "nan":
                await expect(
                    page.get_by_role("textbox", name="Married Last Name")
                ).to_be_visible(timeout=60000)
                await page.get_by_role("textbox", name="Married Last Name").fill(
                    row["Married Last Name"]
                )

        ## Only for Japan
        if country in ["Japan"]:
            if row["Title"] != "nan":
                await page.get_by_role("textbox", name="Title").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Title"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

            if row["Family Name - Kanji"] != "nan":
                await page.get_by_role("textbox", name="Family Name - Kanji").fill(
                    row["Family Name - Kanji"]
                )
            if row["Given Name - Kanji"] != "nan":
                await page.get_by_role("textbox", name="Given Name - Kanji").fill(
                    row["Given Name - Kanji"]
                )

            await page.wait_for_timeout(5000)

            if row["Family Name - Furigana"] != "nan":
                await page.get_by_role("textbox", name="Family Name - Furigana").fill(
                    row["Family Name - Furigana"]
                )
                await page.wait_for_timeout(2000)
                await page.get_by_text("Given Name - Furigana").first.click()
                await page.wait_for_timeout(5000)

            if row["Given Name - Furigana"] != "nan":
                await page.get_by_role("textbox", name="Given Name - Furigana").fill(
                    row["Given Name - Furigana"]
                )
                await page.wait_for_timeout(2000)
                await page.get_by_text("Family Name - Western Script").first.click()
                await page.wait_for_timeout(5000)

            ## Filled only if Enter Western Script is selected "Yes"
            if row["Enter Western Script for Name"] == "Yes":
                await page.wait_for_timeout(5000)
                if row["Family Name - Western Script"] != "nan":
                    await page.get_by_role(
                        "textbox", name="Family Name - Western Script"
                    ).fill(row["Family Name - Western Script"])
                if row["Given Name - Western Script"] != "nan":
                    await page.get_by_role(
                        "textbox", name="Given Name - Western Script"
                    ).fill(row["Given Name - Western Script"])

        await page.wait_for_timeout(5000)
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

        if row["Enter Western Script for Address"] == "Yes" and country in ["Japan"]:
            await expect(page.get_by_text("Enter Western Script").nth(2)).to_be_visible(
                timeout=120000
            )
            await page.get_by_text("Enter Western Script").nth(2).click()
            await page.wait_for_timeout(3000)

        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Date"][:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Date"][2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Date"][4:])
        await page.wait_for_timeout(3000)

        await page.get_by_role(
            "listbox", name="items selected for Country", exact=True
        ).click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Home Country"])
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        if row["Home Country"] in ["Japan"]:
            if row["Prefecture"] != "nan":
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Prefecture").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["Prefecture"])
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
            if row["City or Ward - Kanji"] != "nan":
                await page.get_by_role("textbox", name="City or Ward - Kanji").fill(
                    row["City or Ward - Kanji"]
                )
            if row["Address Line 1 - Kanji"] != "nan":
                await page.get_by_role("textbox", name="Address Line 1 - Kanji").fill(
                    row["Address Line 1 - Kanji"]
                )
            if row["City or Ward - Furigana"] != "nan":
                await page.get_by_role("textbox", name="City or Ward - Furigana").fill(
                    row["City or Ward - Furigana"]
                )
            if row["Address Line 1 - Furigana"] != "nan":
                await page.get_by_role(
                    "textbox", name="Address Line 1 - Furigana"
                ).fill(row["Address Line 1 - Furigana"])
            if row["Neighborhood - Kanji"] != "nan":
                await page.get_by_role("textbox", name="Neighborhood - Kanji").fill(
                    row["Neighborhood - Kanji"]
                )
            if row["Neighborhood - Furigana"] != "nan":
                await page.get_by_role("textbox", name="Neighborhood - Furigana").fill(
                    row["Neighborhood - Furigana"]
                )
            if row["Enter Western Script for Address"] == "Yes":
                if row["City or Ward - Western Script"] != "nan":
                    await page.get_by_role(
                        "textbox", name="City or Ward - Western Script"
                    ).fill(row["City or Ward - Western Script"])
                if row["Address Line 1 - Western Script"] != "nan":
                    await page.get_by_role(
                        "textbox", name="Address Line 1 - Western Script"
                    ).fill(row["Address Line 1 - Western Script"])
                if row["Neighborhood - Western Script"] != "nan":
                    await page.get_by_role(
                        "textbox", name="Neighborhood - Western Script"
                    ).fill(row["Neighborhood - Western Script"])

        if row["Home Country"] in ["Brazil"]:
            await page.get_by_role("textbox", name="Street Type").fill(
                row["Address Line 1"]
            )
            await page.get_by_role("textbox", name="Street Name").fill(
                row["Address Line 2"]
            )
            await page.get_by_role("textbox", name="House Number").fill(
                row["Address Line 3"]
            )
            if await page.get_by_role(
                "textbox", name="Additional Address"
            ).is_visible():
                await page.get_by_role("textbox", name="Additional Address").fill(
                    row["Address Line 4"]
                )
            elif page.get_by_role("textbox", name="Building / Apartment").is_visible():
                await page.get_by_role("textbox", name="Building / Apartment").fill(
                    row["Address Line 4"]
                )
        elif row["Home Country"] not in ["Japan"]:
            await page.get_by_role("textbox", name="Address Line 1").fill(
                f"{row["Address Line 1"]} {row["Address Line 2"]}"
            )

        if row["Neighborhood"] != "nan" and row["Home Country"] in [
            "Mexico",
            "Costa Rica",
            "Brazil",
        ]:
            # Neighborhood
            await page.get_by_role("textbox", name="Neighborhood").fill(
                row["Neighborhood"]
            )
        if row["Home Country"] in ["United States of America", "Brazil"]:
            ## State
            await expect(page.get_by_role("textbox", name="State")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("textbox", name="State").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["State"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

        await page.get_by_role("textbox", name="Postal Code").fill(row["Postal Code"])
        if row["Home Country"] in ["Brazil"]:
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="City").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["City"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
        elif row["Home Country"] not in ["Japan"]:
            await page.get_by_role("textbox", name="City").fill(row["City"])

        if row["Home Country"] in ["Costa Rica"] and row["Province"] != "nan":
            await expect(page.get_by_role("textbox", name="Province")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("textbox", name="Province").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Province"])
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")

        await page.get_by_role("group", name="Address").get_by_label(
            "Type", exact=True
        ).click()
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

        await page.get_by_role("textbox", name="Email Address").fill(
            row["Email Address"]
        )
        await page.get_by_role("group", name="Email").get_by_placeholder(
            "Search"
        ).click()
        await page.keyboard.type(row["Email Usage Type"])
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        if row["Visibility"] != "nan":
            if row["Email Usage Type"] == "Home" and row["Visibility"] == "Yes":
                await expect(
                    page.get_by_label("Email", exact=True)
                    .get_by_label("Visibility")
                    .locator("div")
                    .filter(has_text="Public")
                    .locator("div")
                ).to_be_visible(timeout=60000)
                await page.get_by_label("Email", exact=True).get_by_label(
                    "Visibility"
                ).locator("div").filter(has_text="Public").locator("div").click()
                await page.wait_for_timeout(3000)
                await page.get_by_label("Email", exact=True).get_by_label(
                    "Visibility"
                ).locator("div").filter(has_text="Public").locator("div").click()

        await page.wait_for_timeout(3000)
        await page.get_by_text("OK").last.click()

        await page.wait_for_timeout(10000)
        error_widget_selector = 'div[data-automation-id="errorWidgetBarCanvas"]'
        if await page.is_visible(error_widget_selector):
            await page.click(error_widget_selector)
            await page.wait_for_timeout(2000)
            await page.screenshot(
                path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/hire.png"
            )
            safe_print("Error widget appeared with errors after submission.")
            return False
        else:
            if await page.get_by_role("spinbutton", name="Month").first.is_visible():
                await page.get_by_role("spinbutton", name="Month").first.click()
            else:
                await page.get_by_role("spinbutton", name="Hire Date").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Hire Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Hire Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Hire Date"][4:])
            await page.wait_for_timeout(3000)
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

            if await page.get_by_text("End Employment Date").is_visible():
                if (
                    await page.get_by_role("spinbutton", name="Month")
                    .nth(2)
                    .is_visible()
                ):
                    await page.get_by_role("spinbutton", name="Month").nth(2).click()
                else:
                    await page.get_by_role(
                        "spinbutton", name="End Employment Date"
                    ).click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["End Employment date"][:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["End Employment date"][2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(row["End Employment date"][4:])
                await page.wait_for_timeout(3000)

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

            if country in ["Japan"]:
                if row["Additional Job Classification"] != "nan":
                    await page.get_by_role(
                        "textbox", name="Additional Job Classifications"
                    ).click()
                    await page.wait_for_timeout(3000)
                    await page.keyboard.type(row["Additional Job Classification"])
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)

            if country in ["Mexico", "Japan"]:
                await page.get_by_role("textbox", name="Work Shift").click()
                await page.wait_for_timeout(3000)
                await page.get_by_text(row["Work Shift"]).click()
                await page.wait_for_timeout(3000)

            if await page.get_by_role("spinbutton", name="Month").last.is_visible():
                await page.get_by_role("spinbutton", name="Month").last.click()
            else:
                await page.get_by_role(
                    "spinbutton", name="Company Service Date"
                ).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Company Service Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Company Service Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Company Service Date"][4:])
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(10000)

            if await page.is_visible(error_widget_selector):
                await page.click(error_widget_selector)
                await page.wait_for_timeout(2000)
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/hire_{idx}.png"
                )
                safe_print("Error widget appeared with errors after submission.")
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
                    safe_print(
                        "Submission confirmation popup is visible and screenshot taken."
                    )
                    return True

    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/hire_{idx}.png"
        )
        safe_print(
            str(error).encode("utf-8", errors="replace").decode()
        )  # Safe safe_print
        return False
