import json
import pandas as pd


def get_business_process(bp, file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    valid_step_types = {"Initiation", "Action", "To Do", "Edit Additional Data"}
    filtered_data = []

    # Stop processing entries after finding the first completion step equal to "1"
    for row in data["Report_Entry"][0]["Business_Process_Steps_group"]:
        if row["Step_Type"] in valid_step_types:
            # Create a filtered dictionary
            d = {
                "order": row["Order"],
                "step": row["Step_Type"],
                "completion": row["Completion_Step"],
                "if": row.get("Entry_Conditions_from_Workflow_Step_and_Allowed_Action"),
                "task": row.get("Task"),
                "group": row.get("Security_Groups"),
                "to_do": row.get("To_Do") if row["Step_Type"] == "To Do" else None,
            }
            filtered_data.append(d)

            # Break the loop if Completion_Step is "1"
            if row["Completion_Step"] == "1":
                break

    df = pd.DataFrame(filtered_data)
    df.to_json(rf"./process/{bp}.json", orient="table", index=False)
    print("Data has been converted to DataFrame and saved as json")
