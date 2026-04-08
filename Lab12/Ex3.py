# Parse the ITM Department website to find the people (faculty, grads, lecturers)

import urllib.request
from bs4 import BeautifulSoup

itm_url = "https://shidler.hawaii.edu/itm/people"

itm_html = urllib.request.urlopen(itm_url).read()  # Open the URL and read the HTML content
html_to_parse = BeautifulSoup(itm_html, 'html.parser')  # Create a BeautifulSoup object to parse the HTML

# Print the first few lines of the prettified HTML to understand its structure
print("\n".join(html_to_parse.prettify().splitlines()[:10]))

# Find all ITM people - they're inside <h2 class="title"> tags
list_of_faculty = html_to_parse.find_all("h2", class_="title")

# Build a list of the people's names
itm_faculty = [person.get_text(strip=True) for person in list_of_faculty]

# Print each person and the total number found
print("ITM People:")
for name in itm_faculty:
    print(" -", name)

print(f"\nNumber of people found: {len(itm_faculty)}")