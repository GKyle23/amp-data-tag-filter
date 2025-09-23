[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

# amp-data-tag-filter

A tiny, pandas-based helper to slice an Amplitude tracking plan export by Tags, align it to your import template, and write a clean CSV ready to re-import. The use case is for exporting existing events/properties in an Amplitude tracking plan and filtering for the ones you need to import into another tracking plan. This is to save time so data types and descriptions don't have to be re-written.

## What it does

- Loads your tracking plan export (default: import_data.csv)
- Loads your Amplitude import template (default: import_template.csv)
- Converts empty strings in Tags to NA and fills down (ffill) so child rows inherit their parent object’s tag
- Keeps only rows whose filled Tags value is in your chosen tag_values
- Allows the option to remove property group types as these can conflict with your destination project
- Selects only the template’s columns and re-orders to match
- Writes the result to output_csv

## File expectations

- Input export CSV must include a Tags column.
- Template CSV is the Amplitude import template (export/download from Amplitude).
- Columns in the template determine the output order and which columns are kept.
- If the template includes columns missing from your filtered data, they are created empty so column selection succeeds.

## Quick start

1. Install pandas:

```bash
python -m pip install pandas
```

2. Place these alongside the script:

- `import_data.csv` – your Amplitude tracking plan export
- `import_template.csv` – the Amplitude CSV import template

3. Run the script (edit tags as needed):

```python
from script import filter_tracking_plan  # adjust if your file name differs

filter_tracking_plan(
    input_csv="import_data.csv",
    template_csv="import_template.csv",
    tag_values=["tag_1", "tag_2", "tag_3"],
    keep_property_group_type: bool = True
    # Recommended: write to a new file to avoid overwriting your source
    output_csv="filtered_data.csv",
)
```


If you kept the small if __name__ == "__main__": example in the script, you can also run:

`python amp_tag_filter_script.py`

## Function reference
```python
filter_tracking_plan(
    input_csv: str = "import_data.csv",
    template_csv: str = "import_template.csv",
    tag_values: list[str] = None,
    keep_property_group_type: bool = True,
    output_csv: str = "filtered_data.csv",
) -> pandas.DataFrame
```


- `input_csv` – tracking plan export
- `template_csv` – Amplitude import template (defines output columns/order)
- `tag_values` – list/iterable of tag strings to keep (exact match after fill-down)
- `output_csv` – path to write the aligned, filtered CSV

Returns the final DataFrame written to `output_csv`.
