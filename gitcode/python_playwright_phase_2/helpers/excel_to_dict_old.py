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
                first_sheet[column] = first_sheet[column].dt.strftime("%m%d%Y")
            else:
                first_sheet[column] = (
                    first_sheet[column]
                    .astype(str)
                    .str.strip()
                    .str.replace("\t", "", regex=False)
                )

        return first_sheet.to_dict(orient="records")

    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return None
