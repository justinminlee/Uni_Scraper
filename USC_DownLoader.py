from urllib.request import urlopen
import os
import ssl
import time

# Base URL of UniSC bachelor degrees page
base_url = 'https://www.usc.edu.au/study/courses-and-programs/bachelor-degrees-undergraduate-programs'

# Ignore SSL certificate verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Directory to save degree pages
output_dir = "usc_degree_pages"
os.makedirs(output_dir, exist_ok=True)

# Download the page content
def download_page(url):
    try:
        response = urlopen(url, context=ssl_context)
        return response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to download the page: {e}")
        return None

# Extract links to all degree pages from the main page
def extract_degree_links(page_content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    degree_links = []
    
    # Find all links pointing to specific degree pages
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '/study/courses-and-programs/' in href:  # Filter for degree URLs
            degree_links.append(f"https://www.usc.edu.au{href}" if not href.startswith('http') else href)
    
    return list(set(degree_links))  # Remove duplicates

# Download and save all degree pages
def download_all_degree_pages(degree_links):
    for i, link in enumerate(degree_links):
        try:
            print(f"Downloading ({i+1}/{len(degree_links)}): {link}")
            page_content = download_page(link)
            if page_content:
                # Save the HTML content locally
                filename = os.path.join(output_dir, f"degree_{i+1}.html")
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(page_content)
                print(f"Saved: {filename}")
            else:
                print(f"Failed to download: {link}")
            time.sleep(1)  # Delay to avoid overwhelming the server
        except Exception as e:
            print(f"Error downloading {link}: {e}")

# Main script execution
main_page_content = download_page(base_url)
if main_page_content:
    degree_links = extract_degree_links(main_page_content)
    print(f"Found {len(degree_links)} degree links.")
    download_all_degree_pages(degree_links)
else:
    print("Failed to download the main page content.")
