import requests
from bs4 import BeautifulSoup
import json

import modules.config as config


def fetch_gened(gened_url_path='gened/2024/spring/CS'):
    # Send a GET request to the URL
    url = config.url_prefix + gened_url_path
    response = requests.get(url)

    # Ensure the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to retrieve the webpage")
        return

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # For example, to find a div with the id 'main':
    table = soup.find('table', {'id': 'gened-dt'})

    # Initialize an empty list to hold all rows' data
    rows_data = []

    # Iterate over each row in the table body
    for row in table.find('tbody').find_all('tr'):
        # For each row, get all cells
        cells = row.find_all('td')

        # Extract the text from each cell and create a dictionary for the row
        if cells[1].find('a'):
            row_data = {
                'COURSE': cells[0].get_text(strip=True),
                'SECTION_LINK': cells[1].find('a')['href'] if cells[1].find('a') else None,
                'TITLE': cells[2].get_text(strip=True),
                'ACP': cells[3].get_text(strip=True),
                'CS': cells[4].get_text(strip=True),
                'COMP1': cells[5].get_text(strip=True),
                'HUM': cells[6].get_text(strip=True),
                'NAT': cells[7].get_text(strip=True),
                'QR': cells[8].get_text(strip=True),
                'SBS': cells[9].get_text(strip=True)
            }

        # Append the dictionary to the list of rows
        rows_data.append(row_data)

    # # Convert the list of dictionaries to a JSON string
    # json_data = json.dumps(rows_data, indent=4)

    return rows_data
