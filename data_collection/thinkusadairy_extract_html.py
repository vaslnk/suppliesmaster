import requests
from bs4 import BeautifulSoup
import sys
import os
import zipfile

def extract_company_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)
    company_links = [link['href'] for link in links if 'supplierID' in link['href']]
    return company_links

def download_and_save_html_pages(links, directory):
    for index, link in enumerate(links):
        response = requests.get(link)
        if response.status_code == 200:
            filename = os.path.join(directory, f'page_{index + 1}.html')
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
        else:
            print(f"Failed to download {link}")

def create_zip_file(directory, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)

# Check if a URL was provided
if len(sys.argv) < 2:
    print("Usage: python script_name.py <path_to_html_file> <output_zip_file>")
    sys.exit(1)

file_path = sys.argv[1]
output_zip = sys.argv[2]

# Load HTML file content
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
except FileNotFoundError:
    print("File not found. Please check the path and try again.")
    sys.exit(1)

# Extract links
company_links = extract_company_links(html_content)

# Directory to store individual HTML files
temp_directory = 'temp_html_files'
os.makedirs(temp_directory, exist_ok=True)

# Download and save HTML pages
download_and_save_html_pages(company_links, temp_directory)

# Create zip file of all HTML pages
create_zip_file(temp_directory, output_zip)

# Optionally remove the temporary directory and files after zipping
import shutil
shutil.rmtree(temp_directory)
