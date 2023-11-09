import requests
from bs4 import BeautifulSoup
import json
import re


def extract_course(course_code, url):
    response = requests.get(url)

    # Ensure the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to retrieve the webpage")
        return

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    output = {
        'code': course_code,
        'name': '',
        'credit_hour': '',
        'criterias': [],
        'sections': None,
    }

    course_info = soup.find('div', {'id': 'app-course-info'})
    # print(course_info)

    # Getting Course Title
    course_title_ = course_info.find('span', class_='app-label')
    if course_title_:
        course_title = course_title_.get_text(strip=True)
        # print(course_title)  # This will print the text within the <span> element
        output['name'] = course_title

    # Getting Credit Hour
    p_ = course_info.find('p')
    if p_:
        credit_hour = p_.get_text(strip=True)
        # print(credit_hour)
        output['credit_hour'] = credit_hour

    # Getting Criterias
    strong_ = course_info.find('ul', class_='list-unstyled sort-list')
    if strong_:
        # Find all <li> elements within the <ul>
        criterias_ = strong_.find_all('li')
        # Iterate over each <li> element and print its text content
        for li in criterias_:
            text = li.get_text(strip=True)
            # print(text)  # This will print the text within each <li> element
            output['criterias'].append(text)

    # Getting sections
    script_tags = soup.find_all('script', {'type': 'text/javascript'})
    for script in script_tags:
        if script.string is not None:
            # This will print the raw JavaScript code within the <script> tag
            pattern = re.compile(r'var sectionDataObj = (\[.*?\])')
            match = pattern.search(script.string)
            if match:
                # Extract the JSON string from the matched group
                json_string = match.group(1)

                # Parse the JSON string into a Python object
                try:
                    sections = json.loads(json_string)
                    output['sections'] = sections
                except Exception as e:
                    print(e)

                break  # Assuming we only need the first match

    # with open('courses/' + course_code + '.json', 'w', encoding='utf-8') as f:
    #     json.dump(output, f, ensure_ascii=False, indent=4)
    return output
