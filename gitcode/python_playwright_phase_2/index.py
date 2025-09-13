import sys, os
import asyncio
import time
from helpers.encoding import safe_print
from helpers.excel_to_dict import parse_excel
from helpers.report_generation import generate_report
from helpers.json_to_dict import parse_json
from helpers.screenshot_to_zip import convert_to_zip, make_sreenshot_folders
from playwright.async_api import async_playwright, expect


async def run_automation(excel_file_path, env, user_id):
    data = parse_excel(excel_file_path)
    execution_results = {}  # Dict to group results by row index (idx)
    total_duration = 0
    tenant = env.split("-")[1]

    make_sreenshot_folders(user_id)

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=False)

        for idx, row in enumerate(data):
            try:
                country = row.get("Country")
                bp = row.get("Business Process", "").lower().replace(" ", "_")

                if not country or not bp:
                    safe_print(
                        f"Skipping row {idx+1} due to missing 'Country' or 'Business Process': {row}"
                    )
                    continue

                process_json_path = f"{os.getenv('PLAYWRIGHT_FOLDER')}/helpers/process/{tenant}/{bp}.json"
                process_steps = parse_json(process_json_path)

                for name, step in process_steps.items():
                    script_path = f"scripts.{bp}.{step}"
                    try:
                        script_module = __import__(script_path, fromlist=[""])
                    except Exception as imp_err:
                        safe_print(
                            f"[Playwright] Import error: {script_path} : {imp_err}"
                        )
                        if idx not in execution_results:
                            execution_results[idx] = []
                        execution_results[idx].append(
                            (country, bp, name, "Import Error", 0)
                        )
                        break  # skip to next row

                    try:
                        safe_print(
                            f"[Playwright] Executing script: {country} -> {bp} -> {name}"
                        )

                        if hasattr(script_module, "run_script") and callable(
                            script_module.run_script
                        ):
                            start_time = time.time()
                            try:
                                page = await browser.new_page()
                                flag = await script_module.run_script(
                                    page, expect, row, env, user_id, country, idx
                                )
                                execution_time = time.time() - start_time
                                if execution_time < 15 and (flag is True):
                                    print(
                                        f"[Info] Skipping recording for subprocess lesser than 15s with status 'Passed': {execution_time:.2f}s"
                                    )
                                    pass
                                else:
                                    total_duration += execution_time
                                    result_status = "Passed" if flag else "Failed"
                                    if idx not in execution_results:
                                        execution_results[idx] = []
                                    execution_results[idx].append(
                                        (
                                            country,
                                            bp,
                                            name,
                                            result_status,
                                            execution_time,
                                        )
                                    )

                                    safe_print(
                                        f"[Playwright] {result_status}: {country} -> {bp} -> {name} (Time: {execution_time:.2f}s)"
                                    )
                                    if not flag:
                                        safe_print(
                                            "[Playwright] Stopping further executions for this row due to a failure."
                                        )
                                        break  # only breaks inner loop, not main row loop

                            except Exception as script_error:
                                safe_print(
                                    f"[Playwright] Error executing script: {country} -> {bp} -> {name}: {script_error}"
                                )
                                if idx not in execution_results:
                                    execution_results[idx] = []
                                execution_results[idx].append(
                                    (country, bp, name, "Failed", 0)
                                )
                                break

                            finally:
                                await page.close()
                        else:
                            safe_print(
                                f"[Playwright] 'run_script' is not a function: {country} -> {bp} -> {name}"
                            )
                            if idx not in execution_results:
                                execution_results[idx] = []
                            execution_results[idx].append(
                                (country, bp, name, "Missing run_script", 0)
                            )

                    except Exception as error:
                        safe_print(
                            f"[Playwright] Unexpected error: {country} -> {bp} -> {name}: {error}"
                        )
                        if idx not in execution_results:
                            execution_results[idx] = []
                        execution_results[idx].append((country, bp, name, "Failed", 0))
                        break

            except Exception as row_error:
                safe_print(f"[Playwright] Unhandled error in row {idx+1}: {row_error}")
                execution_results[idx] = [("N/A", "N/A", "N/A", "Row Failure", 0)]
                continue  # move safely to next row

        await browser.close()

    # safe_print execution results summary
    safe_print("\nExecution Summary by Row:")
    for idx, results in execution_results.items():
        safe_print(f"\nRow {idx+1}:")
        for country, bp, name, status, exec_time in results:
            safe_print(
                f"  Script: {country} -> {bp} -> {name}, Status: {status}, Time: {exec_time:.2f}s"
            )

    # Generate HTML report (grouped by rows)
    report_file_path = generate_report(user_id, execution_results, total_duration)
    safe_print(f"Execution report generated: {report_file_path}")
    convert_to_zip(user_id)
    return
