import time
from math import ceil

import requests, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

API_KEY = "badb15ef-f252-4028-91e5-681556c7975c"
url = f"https://jooble.org/api/{API_KEY}"

payload = {
    "keywords": "Software Engineer, Web Developer",
    "page": 1,
}

def fetch_page(page = 1):
    local_payload = payload.copy()
    local_payload['page'] = page

    try:
        response = requests.post(
            url,
            json=local_payload,
            timeout=15
        )
    except Exception as e:
        logger.error(e)
        return None

    if response.status_code == 200:
        logger.info(f"Successfully got response. Status code: {response.status_code}")
    else:
        logger.error(f"Something went wrong. Status code: {response.status_code}")
        return None

    data = response.json()

    if not data:
        logger.error('No data were acquired')
        return None
    elif 'error' in data:
        logger.error(data['error'])
        return None

    return data

def process_job(job):
    print("title: ", job.get('title'))
    print("location: ", job.get('location'))
    print("snippet: ", job.get('snippet'))
    print("salary: ", job.get('salary'))
    print("source: ", job.get('source'))
    print("type: ", job.get('type'))
    print("company: ", job.get('company'))

    print('\n\n\n')
#doing first fetch
basic_data = fetch_page()
if not basic_data:
    logger.warning(f"First page is empty, breaking parsing process")
    quit()
for job in basic_data["jobs"]:
    process_job(job)

#metadata for loop
jobs_per_page = len(basic_data['jobs'])
jobs_total = basic_data['totalCount']

MAX_PAGES = ceil(jobs_total / jobs_per_page)

for page in range(2, MAX_PAGES+1):
    logger.info(f"Fetching page {page}")


    data = fetch_page(page)
    if not data:
        logger.warning(f"Page {page} is empty, breaking parsing process")
        break

    for job in data['jobs']:
        process_job(job)

    logger.info(f"Successfully processed page {page}")
    time.sleep(1)