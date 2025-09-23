import pandas as pd

def filter_tracking_plan(
    input_csv: str = "import_data.csv",
    template_csv: str = "import_template.csv",
    tag_values: list[str] = None,
    keep_property_group_type: bool = True,
    output_csv: str = "filtered_data.csv",
) -> pd.DataFrame:
    """
    Load Amplitude tracking plan CSV, fill-down Tags, filter by given tags,
    align to the import template's column order, rename dots to spaces, and save.

    Returns the aligned DataFrame that was written to `output_csv`.
    """
    # Load data and template
    data = pd.read_csv(input_csv)
    import_template = pd.read_csv(template_csv)

    # Convert empty strings to NA so ffill works, then fill down
    if "Tags" not in data.columns:
        raise ValueError("Input CSV must contain a 'Tags' column.")
    data_fill = data.copy()
    data_fill["Tags"] = data_fill["Tags"].replace("", pd.NA).fillna(method="ffill")

    # Filter by tag values
    filtered_data = data_fill[data_fill["Tags"].isin(tag_values)].copy() 
    
    # Remove property group types so does not conflict with destination plan
    if not keep_property_group_type:
        filtered_data = filtered_data[filtered_data["Property Type"] != "Event Property Group"].copy()

    filtered_data.loc[filtered_data["Object Name"].isna(), "Tags"] = ""

    # Align to template column order
    template_columns = import_template.columns.tolist()
    missing_in_filtered = [c for c in template_columns if c not in filtered_data.columns]
    if missing_in_filtered:
        # Create any template columns that don't exist so selection won't fail
        for c in missing_in_filtered:
            filtered_data[c] = pd.NA

    aligned_dataset = filtered_data[template_columns].copy()

    # Save to output
    aligned_dataset.to_csv(output_csv, index=False)

    return aligned_dataset


# --- tiny example usage (optional) ---
if __name__ == "__main__":
    filter_tracking_plan(
        input_csv="import_data.csv",
        template_csv="import_template.csv",
        tag_values=["tag_1", "tag_2", "tag_3"],
        keep_property_group_type = True,
        output_csv="filtered_data.csv",
    )
