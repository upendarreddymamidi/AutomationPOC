from ..login import login
import os


async def run_rescind_other_processes(page, expect, row, user_id, idx):
    try:
        i = 1
        while await page.get_by_text("You can't rescind this hire").is_visible():
            await page.wait_for_timeout(3000)
            await expect(
                page.get_by_text("Rescind Business Process", exact=True)
            ).to_be_visible(timeout=60000)
            await page.get_by_text("Rescind Business Process", exact=True).click()
            if await page.get_by_text("More").first.is_visible():
                await page.get_by_text("More").first.click()
            await page.get_by_role("button", name="Related Actions").nth(i).click()
            await page.wait_for_timeout(3000)
            await page.get_by_role("menuitem", name="Business Process").hover()
            await page.wait_for_timeout(3000)
            if await page.get_by_role("menuitem", name="Rescind").is_visible():
                await page.get_by_role("menuitem", name="Rescind").click()
            else:
                await page.get_by_role("button", name="Close", exact=True).click()
                await page.get_by_text("Rescind Business Process", exact=True).click()
                i += 1
                await page.wait_for_timeout(3000)
                await page.get_by_role("button", name="Related Actions").nth(i).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("menuitem", name="Business Process").hover()
                await page.wait_for_timeout(3000)
                await page.get_by_role("menuitem", name="Rescind").click()
            await page.wait_for_timeout(3000)
            await expect(
                page.get_by_text("Rescind Business Process", exact=True)
            ).to_be_visible(timeout=60000)
            while await page.get_by_text("RescindableNo").is_visible():
                i += 1
                await page.go_back()
                await page.wait_for_timeout(3000)
                if await page.get_by_text("More").first.is_visible():
                    await page.get_by_text("More").first.click()
                await page.wait_for_timeout(3000)
                await expect(
                    page.get_by_text("You can't rescind this hire")
                ).to_be_visible(timeout=60000)
                await page.get_by_role("button", name="Related Actions").nth(i).click()
                await page.wait_for_timeout(3000)
                await page.get_by_role("menuitem", name="Business Process").hover()
                await page.wait_for_timeout(3000)
                if await page.get_by_role("menuitem", name="Rescind").is_visible():
                    await page.get_by_role("menuitem", name="Rescind").click()
                else:
                    await page.get_by_role("button", name="Close", exact=True).click()
                    await page.get_by_text(
                        "Rescind Business Process", exact=True
                    ).click()
                    i += 1
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("button", name="Related Actions").nth(
                        i
                    ).click()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("menuitem", name="Business Process").hover()
                    await page.wait_for_timeout(3000)
                    await page.get_by_role("menuitem", name="Rescind").click()
                await page.wait_for_timeout(3000)
                await expect(
                    page.get_by_text("Rescind Business Process", exact=True)
                ).to_be_visible(timeout=60000)

            await page.wait_for_timeout(3000)
            await expect(
                page.get_by_role("textbox", name="enter your comment")
            ).to_be_visible(timeout=60000)
            await page.get_by_role("textbox", name="enter your comment").fill(
                row["Comment for Rescind"]
            )
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Submit").click()
            await page.wait_for_timeout(10000)
            i = 1
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/remove_rest_rescind_{idx}.png",
        )
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/remove_rest_rescind_{idx}.png",
        )
        print(error)  # Reraise the error after taking the screenshot
        return False


async def run_script(page, expect, row, env, user_id, country, idx):
    if row["Want to Rescind?"] != "Yes" or row["Want to correct?"] == "Yes":
        return True
    await login(page, expect, env, user_id, idx)
    try:
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("combobox", name="Search Workday").fill(
            row["WWID to Rescind"]
        )
        await page.wait_for_timeout(3000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        # Click on "Employee" link
        await expect(
            page.get_by_role("link", name=f"({row["WWID to Rescind"]})")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("link", name=f"({row["WWID to Rescind"]})").click()
        await expect(page.get_by_text("Actions")).to_be_visible(timeout=60000)

        await page.wait_for_timeout(3000)
        name = (await page.text_content("h1")).strip()

        await page.get_by_text("Actions").click()
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
        await page.get_by_role("textbox", name="Value").fill(row["Process Status"])
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Effective Date Sort and").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("spinbutton", name="Month").click()
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Rescind Effective Date"][:2])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Rescind Effective Date"][2:4])
        await page.wait_for_timeout(3000)
        await page.keyboard.type(row["Rescind Effective Date"][4:])
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Filter", exact=True).click()
        await page.wait_for_timeout(3000)
        await page.get_by_text(f"Hire: {name}", exact=True).click()
        await page.wait_for_timeout(10000)
        await expect(
            page.get_by_role("button", name="Related Actions").first
        ).to_be_visible(timeout=60000)
        await page.get_by_role("button", name="Related Actions").first.click()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Business Process").hover()
        await page.wait_for_timeout(3000)
        await page.get_by_text("Rescind").click()
        await page.wait_for_timeout(3000)
        await expect(
            page.get_by_text("Rescind Business Process", exact=True)
        ).to_be_visible(timeout=60000)
        if await page.get_by_text("You can't rescind this hire").is_visible():
            flag = await run_rescind_other_processes(page, expect, row, user_id, idx)
            if not flag:
                return flag
            await page.wait_for_timeout(3000)

        await expect(
            page.get_by_role("textbox", name="enter your comment")
        ).to_be_visible(timeout=60000)
        await page.get_by_role("textbox", name="enter your comment").fill(
            row["Comment for Rescind"]
        )
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Submit").click()
        await page.wait_for_timeout(10000)
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/success/rescind_{idx}.png",
        )
        return True
    except Exception as error:
        await page.screenshot(
            path=f"{os.getenv("SCREENSHOT_FOLDER")}/{user_id}/error/rescind_{idx}.png",
            full_page=True,
        )
        print(error)  # Reraise the error after taking the screenshot
        return False
