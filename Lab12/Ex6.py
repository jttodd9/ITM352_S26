#Use the requests package to retrieve a page of mortgage rate info from the Hawaii Board of Realtors site that lists current local mortgage rates: 

import requests
from bs4 import BeautifulSoup

# load the url
url = "https://www.hicentral.com/hawaii-mortgage-rates.php"
print("Retrieveing data from URL:" , url)
webpage = requests.get(url)  # Send a GET request to the URL

# Find the rate table and extract each row.
soup = BeautifulSoup(webpage.content, 'html.parser')  # Parse the webpage content with BeautifulSoup
rate_table = soup.find("table")  # There's only one table on the page — the rates table

# Extract each row as a list of cell values
rows = []
for tr in rate_table.find_all("tr"):
    cells = [cell.get_text(strip=True) for cell in tr.find_all(["th", "td"])]
    rows.append(cells)

# First row is the header, the rest are rate entries
header = rows[0]
data_rows = rows[1:]

print("Header:", header)
print(f"Found {len(data_rows)} rate rows:\n")
for r in data_rows:
    print(r)

# Output the name of each bank and its current rates per row.
for row in data_rows:
    bank_name = row[0]  # First cell is the bank name
    rates = row[1:]  # The rest of the cells are the rates
    print(f"the rates for {bank_name}: {', are '.join(rates)}")  # Print the bank name and its rates