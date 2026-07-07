import bs4
import requests, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

url = "https://remoteok.com/"
tags = 'dev,python'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

session = requests.Session()


def fetch_chunk(offset = 0):
    params = {
        "tags": tags,
        "action": "get_jobs",
        "premium": 0,
        "pagination": 1,
        "offset": offset,
    }
    try:
        response = session.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )
    except Exception as e:
        logger.error(e)
        return None

    data = bs4.BeautifulSoup(response.text, 'html.parser')

    if not data:
        logger.error('No data were acquired')
        return None

    return data

def process_job(job):
    #extracting data starts here
    print(job)

    print('\n\n\n')

def extract_jobs(jobs_html):
    pass


offset = 0
while True:

    jobs_html = fetch_chunk(offset = offset)

    if not jobs_html:
        break
    jobs = extract_jobs(jobs_html)

    if not jobs or len(jobs) == 0:
        break

    for job in jobs:
        process_job(job)

    offset += 50