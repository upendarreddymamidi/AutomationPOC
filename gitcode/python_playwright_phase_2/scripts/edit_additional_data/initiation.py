from ..login import login
import os, re


async def run_additional_data(page, expect, row, user_id, idx):
    try:
        await expect(
            page.get_by_role("button", name="Edit Additional Data", exact=True)
        ).to_be_visible(timeout=60000)
        await page.get_by_role(
            "button", name="Edit Additional Data", exact=True
        ).click()

        if row["Severance Benefit Health"] != "nan":
            await expect(
                page.get_by_role(
                    "group", name="Severance Benefit Health"
                ).get_by_placeholder("MM")
            ).to_be_visible(timeout=60000)
            await page.get_by_role(
                "group", name="Severance Benefit Health"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Severance Benefit Health"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Severance Benefit Health"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Severance Benefit Health"][4:])
            await page.wait_for_timeout(3000)

        if row["Severance Benefit No Health"] != "nan":
            await expect(
                page.get_by_role(
                    "group", name="Severance Benefit No Health"
                ).get_by_placeholder("MM")
            ).to_be_visible(timeout=60000)
            await page.get_by_role(
                "group", name="Severance Benefit No Health"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Severance Benefit No Health"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Severance Benefit No Health"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Severance Benefit No Health"][4:])
            await page.wait_for_timeout(3000)

        if row["Job Seniority Date"] != "nan":
            await expect(
                page.get_by_role(
                    "group", name="Job Seniority Date current"
                ).get_by_placeholder("MM")
            ).to_be_visible(timeout=60000)
            await page.get_by_role(
                "group", name="Job Seniority Date current"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Job Seniority Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Job Seniority Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Job Seniority Date"][4:])
            await page.wait_for_timeout(3000)

        if row["Job Bid Move Date"] != "nan":
            await expect(
                page.get_by_role(
                    "group", name="Job Bid Move Date current"
                ).get_by_placeholder("MM")
            ).to_be_visible(timeout=60000)
            await page.get_by_role(
                "group", name="Job Bid Move Date current"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Job Bid Move Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Job Bid Move Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Job Bid Move Date"][4:])
            await page.wait_for_timeout(3000)

        if row["Country Entry Date"] != "nan":
            await expect(
                page.get_by_role(
                    "group", name="Country Entry Date current"
                ).get_by_placeholder("MM")
            ).to_be_visible(timeout=60000)
            await page.get_by_role(
                "group", name="Country Entry Date current"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Country Entry Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Country Entry Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Country Entry Date"][4:])
            await page.wait_for_timeout(3000)

        if row["Naturalization Date"] != "nan":
            await expect(
                page.get_by_role(
                    "group", name="Naturalization Date current"
                ).get_by_placeholder("MM")
            ).to_be_visible(timeout=60000)
            await page.get_by_role(
                "group", name="Naturalization Date current"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Naturalization Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Naturalization Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Naturalization Date"][4:])
            await page.wait_for_timeout(3000)

        if row["STD Eligibility Date"] != "nan":
            await expect(
                page.get_by_role(
                    "group", name="STD Eligibility Date current"
                ).get_by_placeholder("MM")
            ).to_be_visible(timeout=60000)
            await page.get_by_role(
                "group", name="STD Eligibility Date current"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["STD Eligibility Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["STD Eligibility Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["STD Eligibility Date"][4:])
            await page.wait_for_timeout(3000)

        await expect(page.get_by_role("button", name="Submit")).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(3000)
    except Exception as e:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/additional_data_{idx}.png",
        )
        print(e)
        return False


async def run_acquisition(page, expect, row, user_id, idx):
    try:
        await expect(
            page.get_by_role("button", name="Edit Additional Data", exact=True)
        ).to_be_visible(timeout=60000)
        await page.get_by_role(
            "button", name="Edit Additional Data", exact=True
        ).click()

        if row["Acquired Company"] != "nan":
            await expect(
                page.locator("label").filter(has_text="Acquired Company")
            ).to_be_visible(timeout=60000)
            await page.locator("label").filter(has_text="Acquired Company").click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("textbox", name="Acquired Company").fill(
                row["Acquired Company"]
            )
            await page.wait_for_timeout(3000)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            if (
                await page.locator("div")
                .filter(has_text=re.compile(r"^No matches found$"))
                .first.is_visible()
            ):
                await page.screenshot(
                    path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/initiation_{idx}.png",
                )
                return False

        if row["Acquisition Date"] != "nan":
            await page.get_by_role(
                "group", name="Acquisition Date current"
            ).get_by_placeholder("MM").click()
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Acquisition Date"][:2])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Acquisition Date"][2:4])
            await page.wait_for_timeout(3000)
            await page.keyboard.type(row["Acquisition Date"][4:])
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
        await page.wait_for_timeout(3000)
    except Exception as e:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/acquisition_{idx}.png",
        )
        print(e)
        return False


async def run_script(page, expect, row, env, user_id, country, idx):
    await login(page, expect, env, user_id, idx)
    try:
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("combobox", name="Search Workday").click()
        await page.keyboard.type("Start Proxy")
        await page.keyboard.press("Enter")

        # Start proxy
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
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="OK").click()
        await expect(
            page.get_by_role("heading", name="Awaiting Your Action")
        ).to_be_visible(timeout=60000)

        await page.get_by_role("combobox", name="Search Workday").click()
        await page.wait_for_timeout(2000)
        await page.keyboard.type(row["WWID"])
        await page.wait_for_timeout(2000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
        await page.get_by_role("link", name=f"({row["WWID"]})").click()
        await expect(page.get_by_text("Actions")).to_be_visible(timeout=60000)
        await page.get_by_text("Actions").click()
        await expect(page.get_by_text("Additional Data")).to_be_visible(timeout=60000)
        await page.get_by_text("Additional Data").click()

        await expect(page.get_by_text("Edit Worker Effective-Dated")).to_be_visible(
            timeout=60000
        )
        await page.wait_for_timeout(3000)
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

        ## Employee classification
        await expect(
            page.get_by_role("button", name="Edit Additional Data", exact=True)
        ).to_be_visible(timeout=60000)
        await page.get_by_role(
            "button", name="Edit Additional Data", exact=True
        ).click()
        if country == "Mexico":
            await expect(
                page.get_by_role(
                    "heading", name="Mexico Employee Classification"
                ).get_by_label("Mexico Employee Classification")
            ).to_be_visible(timeout=60000)

            if row["Employee Classification"] != "nan":
                await page.wait_for_timeout(3000)
                await page.locator("label").filter(
                    has_text="Employee Classification"
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Employee Classification").fill(
                    row["Employee Classification"]
                )
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                if (
                    await page.locator("div")
                    .filter(has_text=re.compile(r"^No matches found$"))
                    .first.is_visible()
                ):
                    await page.screenshot(
                        path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/initiation_{idx}.png",
                    )
                    return False

            await expect(page.get_by_role("button", name="Submit")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(3000)

        ## ACQUISITION DETAILS -- COSTA RICA
        if country == "Costa Rica":
            result = await run_acquisition(page, expect, row, user_id, idx)
            if result is False:
                return False

        ## ADDITIONAL DATES
        result = await run_additional_data(page, expect, row, user_id, idx)
        if result is False:
            return False

        ## ACQUISITION DETAILS -- MEXICO
        if country == "Mexico":
            result = await run_acquisition(page, expect, row, user_id, idx)
            if result is False:
                return False

        ## COMPANY CAR
        await expect(page.get_by_role("button", name="Skip", exact=True)).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Skip", exact=True).click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_role("button", name="OK")).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(3000)

        ## ISE Indicator
        await expect(page.get_by_role("button", name="Skip", exact=True)).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Skip", exact=True).click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_role("button", name="OK")).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(3000)

        if country == "Costa Rica":
            ## ESG Indicator
            await expect(
                page.get_by_role("button", name="Skip", exact=True)
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name="Skip", exact=True).click()
            await page.wait_for_timeout(3000)
            await expect(page.get_by_role("button", name="OK")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("button", name="OK").click()
            await page.wait_for_timeout(3000)

        ## MCT Indicator
        await expect(page.get_by_role("button", name="Skip", exact=True)).to_be_visible(
            timeout=60000
        )
        await page.get_by_role("button", name="Skip", exact=True).click()
        await page.wait_for_timeout(3000)
        await expect(page.get_by_role("button", name="OK")).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="OK").click()
        await page.wait_for_timeout(3000)

        if country == "Mexico":
            ## Type of Transfer
            await expect(
                page.get_by_role("button", name="Skip", exact=True)
            ).to_be_visible(timeout=60000)
            await page.get_by_role("button", name="Skip", exact=True).click()
            await page.wait_for_timeout(3000)
            await expect(page.get_by_role("button", name="OK")).to_be_visible(
                timeout=60000
            )
            await page.get_by_role("button", name="OK").click()
            await page.wait_for_timeout(3000)

        await page.wait_for_timeout(10000)
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
