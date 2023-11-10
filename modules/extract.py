import requests
from bs4 import BeautifulSoup
import json
from tqdm import trange

import modules.config as config
from modules.course import extract_course


def fetch_pot(pot_url_path="schedule/2024/spring?sess=A"):
    url = config.url_prefix + pot_url_path
    response = requests.get(url)

    # Ensure the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to retrieve the webpage")
        return

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'term-dt'})

    rows_data = []
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        row_data = {
            'SUBJ_CODE': cells[0].get_text(strip=True),
            'SUBJ_NAME': cells[1].get_text(strip=True),
            'SUBJ_LINK': cells[1].find('a')['href']
        }
        rows_data.append(row_data)

    pot_outout = {}

    # print(json.dumps(rows_data, indent=4))
    for i in trange(0, len(rows_data)):
        pot_outout[rows_data[i]['SUBJ_CODE']] = {
            "code": rows_data[i]['SUBJ_CODE'],
            "name": rows_data[i]['SUBJ_NAME'],
            "link": rows_data[i]['SUBJ_LINK'],
            "courses": fetch_pot_subj(subj_url_path=rows_data[i]['SUBJ_LINK'][1:])
        }
        # print(pot_outout[rows_data[i]['SUBJ_CODE']])

    # print(json.dumps(pot_outout, indent=4))
    return pot_outout


def fetch_pot_subj(subj_url_path="/schedule/2024/spring/AAS/201?sess=A"):
    url = config.url_prefix + subj_url_path
    response = requests.get(url)

    # Ensure the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to retrieve the webpage")
        return

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'default-dt'})

    rows_data = []
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        row_data = {
            'code': cells[0].get_text(strip=True),
            'name': cells[1].get_text(strip=True),
            'link': cells[1].find('a')['href'],
            'detail': extract_course(cells[0].get_text(strip=True),
                                     config.url_prefix + cells[1].find('a')['href'][1:])
        }
        rows_data.append(row_data)

    return rows_data


def fetch_gened(gened_url_path="gened/2024/spring/CS"):
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


'''
Extraction
'''


def extract_gened(cat, gened_url_path):
    gened_data = fetch_gened(gened_url_path=gened_url_path)

    with open(cat + '.json', 'w', encoding='utf-8') as f:
        json.dump(gened_data, f, ensure_ascii=False, indent=4)

    print(gened_data[0]['COURSE'])
    for i in trange(0, len(gened_data)):
        # print(gened_data[i]['COURSE'])
        output = extract_course(gened_data[i]['COURSE'],
                                config.url_prefix + gened_data[i]['SECTION_LINK'])

        with open('courses/gened/' + cat + '/' + gened_data[i]['COURSE'] + '.json',
                  'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)


def extract_pot(term="A"):
    pot_data = fetch_pot(pot_url_path="schedule/2024/spring?sess=" + term)

    with open('pot-' + term + '.json', 'w', encoding='utf-8') as f:
        json.dump(pot_data, f, ensure_ascii=False, indent=4)

    # print(gened_data[0]['COURSE'])
    # for i in trange(0, len(gened_data)):
    #     # print(gened_data[i]['COURSE'])
    #     output = extract_course(gened_data[i]['COURSE'],
    #                             config.url_prefix + gened_data[i]['SECTION_LINK'])

    #     with open('courses/gened/' + cat + '/' + gened_data[i]['COURSE'] + '.json',
    #               'w', encoding='utf-8') as f:
    #         json.dump(output, f, ensure_ascii=False, indent=4)
