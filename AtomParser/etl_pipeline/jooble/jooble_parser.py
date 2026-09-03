import datetime
import time
from math import ceil

import requests, logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import os
from dotenv import load_dotenv

API_KEY = os.getenv('JOOBLE_API')

url = f"https://jooble.org/api/{API_KEY}"

payload = {
    "keywords": "Software Engineer, Web Developer",
    "page": 1,
}

session = requests.Session()

def process_details(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as e:
        logger.error(e)
        return None, None

    header_container = soup.find('div', attrs={'data-test-name': '_remoteJobLabel'})
    employment_type_container = header_container.find('div', attrs={'class': 'blapLw q40Pqk fhg31q NTN-BG'})
    employment_type = employment_type_container.get_text(strip=True) if employment_type_container else None

    description_container = soup.find('div', attrs={'data-test-name': '_jobDescriptionBlock'})
    description = description_container.get_text(strip=True) if description_container else None

    return employment_type, description

def fetch_job_list(page = 1):
    local_payload = payload.copy()
    local_payload['page'] = page

    try:
        response = session.post(
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

    #print(job.keys())

    external_id = job.get('id')
    title = 'Software Engineer'
    full_title = job.get('title')
    salary = job.get('salary')

    local_tags = []
    company = job.get('company')
    location = job.get('location')
    is_remote = job.get('location') == 'Remote'
    source = job.get('source')
    link_to_page = job.get('link')
    last_updated = job.get('updated')
    last_parsed = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Not provided
    experience = None
    employment_type = None
    description = None


    ##print("External id: ", external_id)
    ##print("Title: ", title)
    ##print("Salary: ", salary)
    ##print("Experience: ", experience)
    ##print("Employment type: ", employment_type)
    ##print("Tags: ", local_tags)
    ##print("Company: ", company)
    ##print("Location: ", location)
    ##print("Is remote: ", is_remote)
    ##print("Source: ", source)
    ##print("Link to page: ", link_to_page)
    ##print("Last updated: ", last_updated)
    ##print("Last parsed: ", last_parsed)
    ##print("Description: ", description, '...')
    #print('\n\n\n')


#doing first fetch
def parse():
    basic_data = fetch_job_list()
    if not basic_data:
        logger.warning(f"First page is empty, breaking parsing process")
        quit()

    for job in basic_data["jobs"]:
        try:
            processed_job = process_job(job)
            if processed_job:
                yield processed_job
            else:
                logger.error(f"Failed to process job: {job}")
        except Exception as e:
            logger.error(f"Error processing job: {job}. Error: {e}")

    #metadata for loop
    jobs_per_page = len(basic_data['jobs'])
    jobs_total = basic_data['totalCount']

    MAX_PAGES = ceil(jobs_total / jobs_per_page)

    for page in range(2, MAX_PAGES+1):
        logger.info(f"Fetching page {page}")

        data = fetch_job_list(page)
        if not data or not data.get('jobs') or len(data['jobs']) == 0:
            logger.warning(f"Page {page} is empty, breaking parsing process")
            break

        for job in data['jobs']:
            try:
                processed_job = process_job(job)
                if processed_job:
                    logger.info(f"Successfully processed job: {processed_job}")
                    yield processed_job
                else:
                    logger.error(f"Failed to process job: {job}")
            except Exception as e:
                logger.error(f"Error processing job: {job}. Error: {e}")

        logger.info(f"Successfully processed page {page}")
        time.sleep(1)