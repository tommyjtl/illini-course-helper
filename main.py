import json
from tqdm import trange
import os
import time
import requests

from modules.extract import fetch_gened, fetch_pot, extract_gened, extract_pot
from modules.course import extract_course
import modules.config as config


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


def trigger_ifttt():
    r = requests.get(
        "https://maker.ifttt.com/trigger/cs421_monitor/json/with/key/bAq5u9DuEsVIHd44CdA2Sd")

    # Ensure the request was successful
    if r.status_code == 200:
        print(r.text)
    else:
        print("Failed to trigger event")
        return


def main():
    # https://maker.ifttt.com/use/bAq5u9DuEsVIHd44CdA2Sd

    # extract_gened(cat='quantitative-reasoning',
    #               gened_url_path='gened/2024/spring/QR')
    # extract_pot(term="1")
    # get_online(target_path="courses/gened/cultural-studies")

    while True:

        s = extract_course("CS 421",
                           config.url_prefix + "schedule/2024/spring/CS/421")
        # print(json.dumps(s, indent=4))
        for sec in s["sections"]:
            if sec["crn"] == "31375":
                if sec["availability"] != "Closed":
                    trigger_ifttt()
                    print(sec["crn"], "\t", sec["availability"])

        time.sleep(5)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
