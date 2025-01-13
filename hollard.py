import requests
from bs4 import BeautifulSoup
import re

# URL of the Hollard Ghana executive management page
url = "https://www.hollard.com.gh/about-us/executive-management"

def fetch_page_content(url):
    """Fetch the content of the webpage."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return None

def get_executive_details(page_content):
    """Extract names and positions of executives."""
    executives = {}
    soup = BeautifulSoup(page_content, 'html.parser')
    profile_containers = soup.find_all('div', class_=re.compile(r'^hld-u-sm-1-1 hld-u-md-1-2 hld-u-lg-1-4'))

    for container in profile_containers:
        # Extract name
        name_tag = container.find('div', class_='hld-div-blurb-small')
        name = name_tag.get_text(strip=True) if name_tag else "Unknown"

        # Extract position
        position_tag = container.find('p')
        position = position_tag.get_text(strip=True) if position_tag else "Unknown"

        if position != "Unknown":
            executives[position] = name

    return executives

def main():
    """Main function to fetch executive details."""
    page_content = fetch_page_content(url)
    if page_content:
        return get_executive_details(page_content)
    return {}

if __name__ == "__main__":
    exec_details = main()
    print(exec_details)
