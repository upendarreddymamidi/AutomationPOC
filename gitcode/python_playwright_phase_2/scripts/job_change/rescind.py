from ..login import login
import os


# async def Previous_Rescind(page, expect, row, env, user_id, country, idx):
#     await page.wait_for_timeout(3000)
#     await page.get_by_role("button", name="Related Actions").nth(2).click()
#     await page.wait_for_timeout(3000)
#     await page.get_by_text("Business Process").hover()
#     await page.wait_for_timeout(3000)
#     await page.get_by_text("Rescind").click()
#     await expect(
#         page.get_by_text("Rescind Business Process", exact=True)
#     ).to_be_visible(timeout=60000)


async def Contract_Rescind(page, expect, row, env, user_id, country, idx):
    if (
        "add" in row["What changes you made?"].lower()
        or "fixed" in row["What changes you made?"].lower()
    ):
        different_contract = page.locator(
            '[data-automation-id="promptOption"][data-automation-label="Open"]'
        )
    elif "close" in row["What changes you made?"].lower():
        different_contract = page.locator(
            '[data-automation-id="promptOption"][data-automation-label="Closed"]'
        )

    Contract_Type = row["Contract Type-R"]
    contract_type = (
        page.locator('[data-automation-id="promptOption"]')
        .get_by_text(Contract_Type)
        .first
    )

    links = await page.get_by_text("Contract").all()

    print(links)
    for page_link in links:
        await page.wait_for_timeout(3000)
        await page_link.click()

        await page.wait_for_timeout(3000)
        if (
            await page.get_by_text("Contract").first.is_visible()
            and await different_contract.is_visible()
            and await contract_type.is_visible()
        ):
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Related Actions").nth(2).click()
            await page.wait_for_timeout(3000)
            await page.get_by_text("Business Process").hover()
            await page.wait_for_timeout(3000)
            await page.get_by_text("Rescind").click()
            await expect(
                page.get_by_text("Rescind Business Process", exact=True)
            ).to_be_visible(timeout=60000)

            # non_rescindable = await page.locator(
            #     'li:has-text("Rescindable")[data-automation-id="textView"]:has-text("No")'
            # ).is_visible()
            # if non_rescindable:
            #     await Previous_Rescind(page, expect, row, env, user_id, country, idx)

            await page.get_by_role("textbox", name="enter your comment").fill(
                row["Comment for Rescind"]
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(10000)
            # Check for alert message presence
            alert_element = await page.query_selector(
                '[data-automation-id="errorWidgetBarMessageCountCanvas"]'
            )
            alert_text = await alert_element.inner_text() if alert_element else ""
            if "Alert" in alert_text or "Alerts" in alert_text:
                await page.get_by_role("button", name="Submit").click()
                await page.wait_for_timeout(20000)

            event_locator = page.locator("#bpSlimConclusionHeaderText")
            await event_locator.wait_for(state="visible", timeout=15000)

            if await event_locator.is_visible():
                await page.wait_for_timeout(5000)
                await page.screenshot(
                    path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_rescind_{idx}.png"
                )
                print("Submission confirmation popup is visible and screenshot taken.")
                return True

        await page.go_back()
        await page.wait_for_timeout(5000)
        await expect(
            page.get_by_role("button", name="Status Sort and filter column")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="Status Sort and filter column").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").fill("Successfully Complete")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Effective Date Sort and").click()
        await page.wait_for_timeout(3000)

        # Format effective date for correction
        Effective_Date = row["Rescind Effective Date"]
        Effective_Date = Effective_Date.replace("/", "")
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(Effective_Date[:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(Effective_Date[2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(Effective_Date[4:])
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)

    await page.wait_for_timeout(5000)
    await page.screenshot(
        path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_rescind_{idx}.png"
    )
    return False


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Rescind"] != "Yes":
        return True
    if row["Correction"] == "Yes":
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
        await expect(
            page.get_by_role("button", name="Status Sort and filter column")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="Status Sort and filter column").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("textbox", name="Value").fill("Successfully Complete")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Effective Date Sort and").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        Effective_date = row["Rescind Effective Date"]
        Effective_date = Effective_date.replace("/", "")
        await page.keyboard.type(Effective_date[:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(Effective_date[2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(Effective_date[4:])
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)

        if "contract" in row["What changes you made?"].lower():
            await page.wait_for_timeout(3000)
            if not await Contract_Rescind(
                page, expect, row, env, user_id, country, idx
            ):
                return False
            else:
                return True

        else:
            process_name = row["Rescind Process Name"]

            links = await page.get_by_text(process_name).all()

            print(links)
            for page_link in links:
                await page.wait_for_timeout(3000)
                await page_link.click()

                await page.wait_for_timeout(3000)
                if await page.get_by_text(
                    row["What changes you made?"]
                ).first.is_visible():
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("button", name="Related Actions").nth(
                        1
                    ).click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_text("Business Process").hover()
                    await page.wait_for_timeout(3000)
                    await page.get_by_text("Rescind").click()
                    await expect(
                        page.get_by_text("Rescind Business Process", exact=True)
                    ).to_be_visible(timeout=60000)
                    await page.get_by_role("textbox", name="enter your comment").fill(
                        row["Comment for Rescind"]
                    )
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("button", name="Submit").click()
                    await page.wait_for_timeout(10000)

                    # Check for alert message presence
                    alert_element = await page.query_selector(
                        '[data-automation-id="errorWidgetBarMessageCountCanvas"]'
                    )
                    alert_text = (
                        await alert_element.inner_text() if alert_element else ""
                    )
                    if "Alert" in alert_text or "Alerts" in alert_text:
                        await page.get_by_role("button", name="Submit").click()
                        await page.wait_for_timeout(20000)

                    event_locator = page.locator("#bpSlimConclusionHeaderText")
                    await event_locator.wait_for(state="visible", timeout=15000)

                    if await event_locator.is_visible():
                        await page.wait_for_timeout(5000)
                        await page.screenshot(
                            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/success/job_change_rescind_{idx}.png"
                        )
                        print(
                            "Submission confirmation popup is visible and screenshot taken."
                        )
                        return True

                await page.go_back()
                await page.wait_for_timeout(5000)
                await expect(
                    page.get_by_role("button", name="Status Sort and filter column")
                ).to_be_visible(timeout=60000)
                await page.get_by_role(
                    "button", name="Status Sort and filter column"
                ).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox", name="Value").fill(
                    "Successfully Complete"
                )
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Filter", exact=True).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Effective Date Sort and").click()
                await page.wait_for_timeout(3000)

                # Format effective date for correction
                Effective_Date = row["Rescind Effective Date"]
                Effective_Date = Effective_Date.replace("/", "")
                await page.get_by_role("spinbutton", name="Month").click()
                await page.wait_for_timeout(3000)
                await page.keyboard.type(Effective_Date[:2])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(Effective_Date[2:4])
                await page.wait_for_timeout(3000)
                await page.keyboard.type(Effective_Date[4:])
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Filter", exact=True).click()
                await page.wait_for_timeout(3000)
            await page.wait_for_timeout(5000)
            await page.screenshot(
                path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_rescind_{idx}.png"
            )
            return False
    except Exception as error:
        await page.wait_for_timeout(5000)
        await page.screenshot(
            path=f"{os.getenv('SCREENSHOT_FOLDER')}/{user_id}/error/job_change_rescind_{idx}.png"
        )
        print(f"Error: {error}")
        return False
