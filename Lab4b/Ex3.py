url = input("Enter a URL: ")

cleanded_url = url.replace("https://", "")
print("Cleaned URL: ", cleanded_url)

parts = cleanded_url.split(".")
domain = parts[1]
print("Domain: ", domain)

TLD = parts[2]
TLD_cleaned = TLD.strip("/")
print("Top-Level Domain: ", TLD_cleaned)