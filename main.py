import json
from tqdm import trange
import os

from modules.extract import fetch_gened, fetch_pot
from modules.course import extract_course
import modules.config as config


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


def get_online(target_path):
    get_ls = os.listdir(target_path)
    online_courses = []
    for j in get_ls:
        if ".json" in j:
            with open(target_path + "/" + j, "r") as f:
                data = json.load(f)
                # print(data)
                is_us = False
                if any("US Minority" in item for item in data['criterias']):
                    is_us = True

                if is_us:
                    for section in data['sections']:
                        if "Online" in section['type']:
                            online_courses.append(
                                {
                                    'code': data['code'],
                                    'name': data['name'],
                                    'date': section['sectionDateRange']
                                }
                            )
                            break

    for course in online_courses:
        print(json.dumps(course, indent=4))


def main():
    # extract_gened(cat='quantitative-reasoning',
    #               gened_url_path='gened/2024/spring/QR')

    # extract_pot(term="1")

    get_online(target_path="courses/gened/cultural-studies")


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
