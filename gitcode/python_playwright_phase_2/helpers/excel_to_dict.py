import pandas as pd


def parse_excel(file_path):
    try:
        data = pd.read_excel(file_path, sheet_name=None, header=1)
        first_sheet = list(data.values())[0]

        if first_sheet.empty:
            print("No data found in the Excel sheet. Exiting.")
            return None

        first_sheet.columns = first_sheet.columns.str.strip()

        for column in first_sheet.columns:
            if pd.api.types.is_datetime64_any_dtype(first_sheet[column]):
                # Format datetime columns to "MMDDYYYY"
                # NaT values will be formatted as 'NaT'
                first_sheet[column] = first_sheet[column].apply(
                    lambda x: x.strftime("%m%d%Y") if pd.notna(x) else "nan"
                )
            elif "wwid" in column.lower():
                first_sheet["WWID"] = first_sheet["WWID"].astype(float).astype(int)
            elif pd.api.types.is_numeric_dtype(first_sheet[column]):
                # Convert to float first to handle NaNs if any
                first_sheet[column] = first_sheet[column].astype(float)

            # Convert all columns to string for uniformity
            first_sheet[column] = (
                first_sheet[column]
                .astype(str)
                .str.strip()
                .str.replace("\t", "", regex=False)
            )

        first_sheet = first_sheet.replace({"<NA>": "nan", None: "nan"})

        # Convert DataFrame to list of dicts
        data_records = first_sheet.to_dict(orient="records")

        # Ensure UTF-8 compatibility
        for record in data_records:
            for key, value in record.items():
                if isinstance(value, str):
                    record[key] = value.encode("utf-8", errors="replace").decode()

        return data_records

    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return None
