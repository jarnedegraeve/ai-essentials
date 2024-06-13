import os
import subprocess
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from datetime import datetime

def print_with_timestamp(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {message}")

# Function to install packages from requirements.txt
def install_packages():
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../requirements.txt')
    if os.path.isfile(requirements_path):
        print_with_timestamp("Installing required packages ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL
                              )
    else:
        print_with_timestamp(f"No requirements.txt found at {requirements_path}")

# Ensure required packages are installed
install_packages()
print_with_timestamp("Packages successfully installed!\n")

# Base URL
base_url = "https://www.erasmushogeschool.be/nl/opleidingen"

# Make a request to the website
r = requests.get(base_url)

# Use the 'html.parser' to parse the page
soup = BeautifulSoup(r.content, 'html.parser')

# Find all links on page
links = soup.findAll('a')

print_with_timestamp("Parsing websites ...")

# Filter the links
filtered_links = []
for link in links:
    href = link.get('href')
    # select the relative links to 'opleidingen'
    if href and href.startswith('/nl/opleidingen/'):
        full_url = urljoin(base_url, href)  # Join the base URL with the relative URL
        if full_url not in filtered_links:
            filtered_links.append(full_url)
    # select the absolute links 1 level deeper than 'https://www.erasmushogeschool.be/nl/'
    elif href and href.startswith('https://www.erasmushogeschool.be/nl/') and not href.startswith('https://www.erasmushogeschool.be/nl/opleidingen') and href.count('/') == 4:
        if href not in filtered_links:
            filtered_links.append(href)

# Ensure the output directory exists
output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../erasmus-site-parsed')
os.makedirs(output_directory, exist_ok=True)

# Save the links to html files
for link in tqdm(filtered_links):
    # Make a request to the website
    r = requests.get(link)

    # Use the 'html.parser' to parse the page
    soup = BeautifulSoup(r.content, 'html.parser')

    # Generate the file name
    file_name = link.replace('https://www.erasmushogeschool.be/nl/', '').replace('/', '_') + '.html'

    # Write the parsed content to a file
    with open(os.path.join(output_directory, file_name), "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))

print_with_timestamp("Websites successfully parsed!\n")
