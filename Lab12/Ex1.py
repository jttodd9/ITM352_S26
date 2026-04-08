# Scrape data from the city of Chicago's data portal and I want to print any line that has a title tag in it.

import urllib.request
url = "https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data"

print("Opening URL:", url)
webpage = urllib.request.urlopen(url)

# Iterate through each line in the webpage to search for the title tag
for line in webpage:
    line = line.decode('utf-8')  # Decode bytes to string
    if '<title>' in line:  # Check if the line contains the title tag
        print(f"Line with title tag: {line.strip()}")  # Print the line that contains the title tag, removing extra whitespace