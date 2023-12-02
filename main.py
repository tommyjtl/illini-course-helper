import json
from tqdm import trange
import os
import time
import requests
import random
import datetime

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

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
    # https://maker.ifttt.com/use/bAq5u9DuEsVIHd44CdA2Sd
    r = requests.get(
        "https://maker.ifttt.com/trigger/cs421_monitor/json/with/key/bAq5u9DuEsVIHd44CdA2Sd")

    # Ensure the request was successful
    if r.status_code == 200:
        print(r.text)
    else:
        print("Failed to trigger event")


def main():

    # extract_gened(cat='quantitative-reasoning',
    #               gened_url_path='gened/2024/spring/QR')
    # extract_pot(term="1")
    # get_online(target_path="courses/gened/cultural-studies")
    '''

    Checking if a section is open
    '''

    # while True:
    #     print("[", datetime.datetime.now().isoformat(), "] Checking...")

    #     s = extract_course("CS 444",
    #                        config.url_prefix + "schedule/2024/spring/CS/444")

    #     # print(json.dumps(s, indent=4))
    #     for sec in s["sections"]:
    #         if sec["crn"] == "73329":  # undergrad section
    #             if sec["availability"] != "Closed":
    #                 trigger_ifttt()
    #                 print(sec["crn"], "\t", sec["availability"])
    #                 print(json.dumps(sec, indent=4))

    #     # random.seed(HASHABLE_OBJECT)
    #     offset = random.randint(-30, 10)
    #     wait_time = offset + 1 * 60
    #     # wait_time = 1

    #     # Section Status updates every 10 minutes.
    #     # No need to rush

    #     time.sleep(wait_time)

    '''
    Prints each section of a course
    '''

    # s = extract_course("CS 598",
    #                    config.url_prefix + "schedule/2024/spring/CS/598")
    # for i in range(0, len(s['sections'])):
    #     # print(json.dumps(s['sections'][i], indent=4))
    #     print(
    #         s['sections'][i]['crn'],
    #         # s['sections'][i]['section'],
    #         s['sections'][i]['sectionTitle']
    #     )

    '''
    Prints the name of the course for a list
    '''
    courses = ['CS 409', 'CS 414', 'CS 416', 'CS 417', 'CS 418', 'CS 419', 'CS 445', 'CS 448',
               'CS 465', 'CS 467', 'CS 468', 'CS 469', 'CS 519', 'CS 545', 'CS 565', 'CS 567']
    for course in courses:
        try:
            s = extract_course(course,
                               config.url_prefix + "schedule/2024/spring/" + course[:2] + "/" + course[3:])
            print(s['name'])
        except:
            # print(course, "not found")
            pass


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
