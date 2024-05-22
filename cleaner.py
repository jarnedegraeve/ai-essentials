import os
import re
from bs4 import BeautifulSoup

def clean_html(html_content):
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove all <script> and <style> tags
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # Get the text content
    text_content = soup.get_text(separator=' ')

    # Clean the text
    cleaned_text = re.sub(r'\s+', ' ', text_content).strip()  # Replace multiple spaces/newlines with a single space

    return cleaned_text

def process_files_in_directory(directory, output_directory=None):
    # Ensure the output directory exists
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.html') or filename.endswith('.htm'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                cleaned_text = clean_html(html_content)
                print(f"Cleaned text for {filename}:\n{cleaned_text}\n")

                # Optionally, save the cleaned text to a new file
                if output_directory:
                    output_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_cleaned.txt")
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        output_file.write(cleaned_text)
                    print(f"Cleaned text saved to {output_file_path}")

# Directory containing HTML files
input_directory = r"D:/ai essentials/erasmus-site-parsed"  # Use raw string or forward slashes
output_directory = r"D:/ai essentials/erasmus-site-cleaned"  # Use raw string or forward slashes

# Process all files in the directory
process_files_in_directory(input_directory, output_directory)
