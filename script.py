import pandas as pd

# Load the Amplitude tracking plan data to filter
file_path = "import_data.csv"
data = pd.read_csv(file_path)

# Import the tracking plan import template
import_template = pd.read_csv("import_template.csv")

# Prepare data for data fill (convert empty strings to NaN for fill down)
data['Tags'].replace("", pd.NA, inplace=True)

# Fill down the Tags column to propagate the object name to related rows
data_fill = data.fillna(method='ffill')

# Set the tag values for the data you want to import
tag_values = ["tag_1", "tag_2", "tag_3"]

# Filter the data
filtered_data = data_fill[data_fill['Tags'].isin(tag_values)]
filtered_data.loc[filtered_data['Object.Name'] == "", 'Tags'] = ""

# Get template column names
template_columns = import_template.columns.tolist()

# Map to import layout: Select only matching columns, reorder, and rename
aligned_dataset = filtered_data[template_columns]
aligned_dataset.columns = aligned_dataset.columns.str.replace(".", " ")

# Save the cleaned data
aligned_dataset.to_csv("import_data.csv", index=False)
