import os
import re
import subprocess
import sys
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup

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

print_with_timestamp("Cleaning HTML ...")
def clean_html(html_content):
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove all <script> and <style> tags
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # Get the text content
    text_content = soup.get_text(separator=' ')

    # Clean the text
    cleaned_text = re.sub(r'\s+', ' ', text_content).strip()

    return cleaned_text

def process_files_in_directory(directory, output_directory=None):
    # Ensure the output directory exists
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    # Iterate over each file in the directory
    for filename in tqdm([f for f in os.listdir(directory) if f.endswith('.html') or f.endswith('.htm')]):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            cleaned_text = clean_html(html_content)

            # Optionally, save the cleaned text to a new file
            if output_directory:
                output_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_cleaned.txt")
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(cleaned_text)
# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Relative directories containing HTML files
input_directory = os.path.join(script_dir, '../erasmus-site-parsed')
output_directory = os.path.join(script_dir, '../erasmus-site-cleaned')

# Process all files in the directory
process_files_in_directory(input_directory, output_directory)
print_with_timestamp("Websites successfully cleaned!\n")
