install.packages("dplyr")
install.packages("tidyr")

library(dplyr)
library(tidyr)


# Load the Amplitude tracking plan data to filter
file_path <- "import_data.csv"
data <- read.csv(file_path, stringsAsFactors = FALSE)

# Import the tracking plan import template
import_template <-read.csv("import_template.csv", stringsAsFactors = FALSE)

# Prepare data for data fill
data$Tags[data$Tags == ""] <- NA 

# Fill down the Tags column to propagate the object name to related rows
data_fill <- data %>% fill(Tags, .direction = "down")

#Set the tag values for the data you want to import.
tag_values <-c("tag_1,"tag_2","tag_3")

#Filter the data
filtered_data <- data_fill %>%
  filter(Tags %in% tag_values) %>%
  mutate(Tags = if_else(Object.Name != "", Tags, ""))

template_columns <- colnames(import_template)

#Map to to import layout
aligned_dataset <- filtered_data %>%
  select(any_of(template_columns)) %>%  # Select only matching columns gracefully
  select(all_of(template_columns))  %>% # Reorder based on template
  # Rename columns to remove dots
  rename_with(~ gsub("\\.", " ", .x))       

  
write.csv(aligned_dataset, "import_data.csv", row.names = FALSE)
