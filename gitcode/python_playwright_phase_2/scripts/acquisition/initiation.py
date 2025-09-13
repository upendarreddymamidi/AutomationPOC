from ..login import login
import os


async def run_script(page, expect, row, env, user_id, country, idx):
    await login(page, expect, env, user_id, idx)
    try:
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("combobox", name="Search Workday").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type("start proxy")
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").press("Enter")
        await expect(page.get_by_role("link", name="Start Proxy")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("link", name="Start Proxy").click()
        await expect(
            page.get_by_role("textbox", name="User to Proxy As")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("textbox", name="User to Proxy As").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type("Aimbyl Ava Guillermo")
        await page.wait_for_timeout(2000)
        await page.get_by_role("textbox", name="User to Proxy As").press("Enter")
        await page.wait_for_timeout(2000)
        await page.get_by_role("button", name="OK").click()
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("combobox", name="Search Workday").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["WWID"])
        await page.get_by_role("combobox", name="Search Workday").press("Enter")
        await page.get_by_role("link", name=f"({row["WWID"]})").click()
        await page.get_by_text("Actions", exact=True).click()
        await expect(page.get_by_text("Additional Data")).to_be_visible(timeout=60000)
        await page.get_by_text("Additional Data").click()
        await expect(page.get_by_text("Edit Worker Effective-Dated")).to_be_visible(
            timeout=60000
        )
        # Effective Date
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date"][:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date"][2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Effective Date"][4:])
        await page.wait_for_timeout(3000)
        await expect(page.get_by_role("button", name="OK")).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(3000)
        await expect(
            page.get_by_role("button", name="Edit Additional Data")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="Edit Additional Data").click()
        await expect(page.get_by_role("button", name="Submit")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Submit").click()
        await expect(
            page.get_by_role("button", name="Edit Additional Data", exact=True)
        ).to_be_visible(timeout=60000)
        await page.get_by_role(
            "button", name="Edit Additional Data", exact=True
        ).click()
        await expect(page.get_by_role("button", name="Submit")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Submit").click()
        await expect(
            page.get_by_role("button", name="Edit Additional Data", exact=True)
        ).to_be_visible(timeout=60000)
        await page.get_by_role(
            "button", name="Edit Additional Data", exact=True
        ).click()

        if row["Acquired Company"] != "nan":
            await expect(
                page.get_by_role("listbox", name="items selected for Acquired")
            ).to_be_visible(timeout=60000)
            await page.get_by_role(
                "listbox", name="items selected for Acquired"
            ).click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Acquired Company"])
            await page.keyboard.press("Enter")

        if row["Acquisition Date current"] != "nan":
            await page.get_by_role(
                "group", name="Acquisition Date current"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Acquisition Date current"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Acquisition Date current"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Acquisition Date current"][4:])
            await page.wait_for_timeout(3000)

        if row["Latest J&J Hire Date for Acquired Employees"] != "nan":
            await page.get_by_role(
                "group", name="Latest J&J Hire Date for"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(
                row["Latest J&J Hire Date for Acquired Employees"][:2]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.type(
                row["Latest J&J Hire Date for Acquired Employees"][2:4]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.type(
                row["Latest J&J Hire Date for Acquired Employees"][4:]
            )
            await page.wait_for_timeout(3000)

        if row["Pre-J&J Hire Date for Acquired Employees"] != "nan":
            await page.get_by_role(
                "group", name="Pre-J&J Hire Date for"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(
                row["Pre-J&J Hire Date for Acquired Employees"][:2]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.type(
                row["Pre-J&J Hire Date for Acquired Employees"][2:4]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.type(
                row["Pre-J&J Hire Date for Acquired Employees"][4:]
            )
            await page.wait_for_timeout(3000)

        if row["J&J Service for Acquired Employees"] != "nan":
            await page.get_by_role(
                "group", name="J&J Service for Acquired"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["J&J Service for Acquired Employees"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["J&J Service for Acquired Employees"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["J&J Service for Acquired Employees"][4:])
            await page.wait_for_timeout(3000)

        await expect(page.get_by_role("button", name="Submit")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Submit").click()
        await expect(page.get_by_role("button", name="Skip", exact=True)).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Skip", exact=True).click()
        await expect(page.get_by_role("button", name="OK")).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="OK").click()
        await expect(page.get_by_role("button", name="Skip", exact=True)).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Skip", exact=True).click()
        await expect(page.get_by_role("button", name="OK")).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="OK").click()
        await expect(page.get_by_role("button", name="Skip", exact=True)).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Skip", exact=True).click()
        await expect(page.get_by_role("button", name="OK")).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="OK").click()
        await expect(page.get_by_role("button", name="Skip", exact=True)).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Skip", exact=True).click()
        await expect(page.get_by_role("button", name="OK")).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="OK").click()
        await expect(page.get_by_role("button", name="Skip", exact=True)).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Skip", exact=True).click()
        await expect(page.get_by_role("button", name="OK")).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_text("view details")).to_be_visible(timeout=60000)
        await page.get_by_text("view details").click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_text("Process Successfully Completed")).to_be_visible(
            timeout=60000
        )
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
