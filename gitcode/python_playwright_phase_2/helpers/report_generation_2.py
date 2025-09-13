import os


def generate_report(user_id, execution_results, total_duration):
    # Get base report folder from environment variable
    base_folder = os.getenv("REPORT_FOLDER")
    if not base_folder:
        raise ValueError("Environment variable 'REPORT_FOLDER' is not set.")

    # Create user-specific folder
    user_folder = os.path.join(base_folder, str(user_id))
    os.makedirs(user_folder, exist_ok=True)  # Ensure the folder exists

    # Define path for the report HTML file inside the user folder
    report_path = os.path.join(user_folder, "execution_report.html")
    report_content = """
    <html>
    <head>
        <title>Automation Execution Report</title>
        <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f4;
        }
        h1 {
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        thead {
            background-color: rgb(236, 47, 47); 
        }
        tbody {
            background-color: #ffffff;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            color: white;
        }
        .status-pass {
            color: green;
            font-weight: bold;
        }
        .status-fail {
            color: red;
            font-weight: bold;
        }
        .process-button {
            cursor: pointer;
            background-color: #b4e1f0;
            color: white;
            padding: 10px 15px;
            border: 2px solid rgb(255, 60, 0); 
            border-radius: 5px;
            margin: 5px;
        }
        .sub-process {
            display: none;
            margin-left: 20px;
            padding: 10px;
            border-left: 2px solid #e7e7e7;
            background-color: #eef1f3;
        }
        </style>
        <script>
            function toggleSubProcess(elem) {
                var subProcessRow = elem.parentElement.parentElement.nextElementSibling;
                if (subProcessRow.style.display === "table-row") {
                    subProcessRow.style.display = "none";
                } else {
                    subProcessRow.style.display = "table-row";
                }
            }
        </script>
    </head>
    <body>
        <h1>Automation Execution Report</h1>
        <table>
            <thead>
                <tr>
                    <th>Row #</th>
                    <th>Country</th>
                    <th>Business Process</th>
                    <th>Sub Processes</th>
                    <th>Status</th>
                    <th>Duration (s)</th>
                </tr>
            </thead>
            <tbody>
    """

    # execution_results is expected
    # {
    #   idx: [ (country, bp, sub_process, status, exec_time), ... ],
    #   ...
    # }

    for idx, results in execution_results.items():
        if not results:
            continue

        country = results[0][0]
        bp = results[0][1]
        total_row_duration = sum(exec_time for _, _, _, _, exec_time in results)
        primary_status = (
            "Pass"
            if all(sub_status.lower() == "passed" for _, _, _, sub_status, _ in results)
            else "Fail"
        )
        status_class = "status-pass" if primary_status == "Pass" else "status-fail"

        report_content += f"""
            <tr>
                <td><button class="process-button" onclick="toggleSubProcess(this)">{idx+1}</button></td>
                <td>{country}</td>
                <td>{bp}</td>
                <td>{len(results)}</td>
                <td class="{status_class}">{primary_status}</td>
                <td>{total_row_duration:.2f}</td>
            </tr>
            <tr class="sub-process">
                <td colspan="6">
                    <div>
                        <strong>Sub-Processes:</strong>
                        <ul>
        """

        for _, _, sub_process, sub_status, sub_exec_time in results:
            sub_status_class = (
                "status-pass" if sub_status.lower() == "passed" else "status-fail"
            )
            report_content += f"""
                <li class="{sub_status_class}">{sub_process} - {sub_status} (Time: {sub_exec_time:.2f}s)</li>
            """

        report_content += """
                        </ul>
                    </div>
                </td>
            </tr>
        """
    report_content += f"""
            </tbody>
        </table>
        <h2>Total Duration: {total_duration:.2f} seconds</h2>
    </body>
    </html>
    """

    # Write report to an HTML file
    with open(report_path, "w") as report_file:
        report_file.write(report_content)

    return os.path.abspath(report_path)
