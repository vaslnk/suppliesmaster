import os
import sys
from bs4 import BeautifulSoup
import pyperclip  # Import pyperclip for clipboard operations

def extract_data(html_file):
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, 'html.parser')

    data_keys = [
        "Brand Name", "Url", "Category", "Items", "Phone Number", "Email",
        "Location", "City", "State", "Zip Code", "Address", "Description", "Data Source"
    ]

    url_tag = soup.find('a', {'id': 'website_link_id'})
    url = url_tag.get('href') if url_tag else ""

    email_tag = soup.find('a', href=lambda href: href and "mailto:" in href)
    email = email_tag.get('href').split(':')[1] if email_tag else ""

    city_state_zip = soup.find_all('span')[-3].text.strip().split(',')

    data = {
        "Brand Name": soup.find('h1', {'class': 'no-margin'}).get_text(strip=True) if soup.find('h1', {'class': 'no-margin'}) else "",
        "Url": url,
        "Category": "Dairy Products",
        "Items": ", ".join([p.get_text(strip=True) for p in soup.select('.supplier-category strong')]),
        "Phone Number": soup.find('span', {'id': 'phone_id'}).get_text(strip=True) if soup.find('span', {'id': 'phone_id'}) else "",
        "Email": email,
        "Location": "",
        "City": city_state_zip[0].strip(),
        "State": soup.find('span', string="State:").next_sibling.strip() if soup.find('span', string="State:") else "",
        "Zip Code": soup.find('span', string="Zip Code:").next_sibling.strip() if soup.find('span', string="Zip Code:") else "",
        "Address": ", ".join([span.get_text(strip=True) for span in soup.select('.address span')]),
        "Description": soup.find('div', {'class': 'summary'}).get_text(strip=True) if soup.find('div', {'class': 'summary'}) else "",
        "Data Source": "www.thinkusadairy.org"
    }

    return "\t".join(str(data.get(key, "")) for key in data_keys)

def process_directory(directory):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            result = extract_data(filepath)
            results.append(result)
    return results

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_html_data.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    all_results = process_directory(directory_path)
    results_string = "\n".join(all_results)  # Combine all results with a newline
    pyperclip.copy(results_string)  # Copy results to clipboard
    print("Data has been copied to clipboard.")

if __name__ == "__main__":
    main()
