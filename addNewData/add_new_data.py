import pandas as pd
existing_data = pd.read_csv("./MaliciousURL.csv")

new_urls = []
new_types = []

num_entries = int(input("Enter the number of new entries: "))

for i in range(num_entries):
    url = input(f"Enter URL {i + 1}: ")
    new_urls.append(url)

    url_type = input(f"Enter type for URL {url}: ")
    new_types.append(url_type)

new_data = pd.DataFrame({"url": new_urls, "type": new_types})

updated_data = pd.concat([existing_data, new_data], ignore_index=True)
updated_data.to_csv("./malicious_phish.csv", index=False)
