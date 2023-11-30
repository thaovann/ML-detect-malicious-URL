import pandas as pd

# Load the existing CSV file
existing_data = pd.read_csv("./MaliciousURL.csv")

# Collect user input for new data
new_urls = []
new_types = []

num_entries = int(input("Enter the number of new entries: "))

for i in range(num_entries):
    url = input(f"Enter URL {i + 1}: ")
    new_urls.append(url)

    url_type = input(f"Enter type for URL {url}: ")
    new_types.append(url_type)

# Create a DataFrame with the new data
new_data = pd.DataFrame({"url": new_urls, "type": new_types})

# Append the new data to the existing DataFrame
updated_data = pd.concat([existing_data, new_data], ignore_index=True)

# Write the updated DataFrame back to the CSV file
updated_data.to_csv("./malicious_phish.csv", index=False)
