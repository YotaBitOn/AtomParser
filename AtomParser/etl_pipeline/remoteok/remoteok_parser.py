import datetime
import time

import bs4
import requests, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

url = "https://remoteok.com/"
tags = 'python'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

session = requests.Session()


def fetch_page(link):
    local_url = url + link
    try:
        response = requests.get(
            local_url,
            headers=headers,
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

    html = bs4.BeautifulSoup(response.text, 'html.parser')

    return html

def fetch_chunk(offset = 0):
    params = {
        "tags": tags,
        "action": "get_jobs",
        "premium": 0,
        "pagination": 1,
        "offset": offset,
    }
    try:
        logger.info(f'Fetching from RemoteOK with offset {offset} and tags {tags}')
        response = session.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )
    except Exception as e:
        logger.error(e)
        return None

    html = bs4.BeautifulSoup(response.text, 'html.parser')

    if html is None or html.text.strip() == '':
        logger.error('No data were acquired')
        return None

    logger.info(f'Successfully fetched data from offset {offset}, extracting job links...')

    return html

def process_job(job, link):
    source = 'remoteok'
    link_to_page = url+link
    last_parsed = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')



    container = job.select_one("tr.job.active")
    if container is None:
        logger.info(f'No job info were found, stopping...')
        return

    external_id = link.split('/')[-1]

    full_title = container.find('h2', attrs={'itemprop': "title"})
    full_title = full_title.get_text(strip=True) if full_title else None

    company = container.find('h3', attrs={'itemprop': "name"})
    company = company.get_text(strip=True) if company else None

    locations = []
    locations_html = container.find_all('div', attrs={'class': 'location' })

    for location in locations_html:
        if location and location.get_text(strip=True) != '':
            locations.append(location.get_text(strip=True))
    locations = locations[:-1]

    last_updated_container = job.find("td", class_="time").find('time')
    last_updated = last_updated_container['datetime'] if last_updated_container else None

    local_tags = []
    tags_container = container.find('td', attrs={'class': 'tags'})
    if tags_container:
        tags_hrefs = tags_container.find_all('a')
        for tag in tags_hrefs:
            local_tags.append(tag.get_text(strip=True))

    #description container
    description_container = job.select_one('tr.expand.active')
    description = (description_container.find('div', attrs={'class': 'html'}) or
                   description_container.find('div', attrs={'class': 'markdown'}))
    description = description.get_text(strip=True) if description else None

    salary_heading = description_container.find(string="Salary and compensation")
    salary = salary_heading.find_next().find_next().text.strip() if salary_heading else None
    if not salary or salary == 'Upgrade to Premium':
        salary = None

    print("External id: ", external_id)
    print("Title: ", full_title)
    print("Salary: ", salary)
    print("Tags: ", local_tags)
    print("Company: ", company)
    print("Locations: ", locations)
    print("Is remote: ", True)
    print("Source: ", source)
    print("Link to page: ", link_to_page)
    print("Last updated: ", last_updated)
    print("Last parsed: ", last_parsed)
    print("Description: ", description, '...')

def extract_job_links(jobs_html):
    links = jobs_html.find_all('a', attrs={'class': 'action-apply' })

    links = [link.get('href') for link in links] #href extraciton

    links = list(set(links)) #deduplicaton

    return links

offset = 0
while True:

    jobs_html = fetch_chunk(offset = offset)

    if not jobs_html:
        break

    links = extract_job_links(jobs_html)

    print(len(links))

    if not links:
        logger.info(f'No job links for {tags} were found, stopping...')
        break

    logger.info(f'Found {len(links)} job links for {tags}, parsing job pages...')

    i = offset+1
    for link in links:

        html = fetch_page(link)

        if not html:
            logger.info(f'No page on link {link} were found, skipping...')
            continue

        logger.info(f'Processing job on {link} ...')
        process_job(html, link)
        i+=1
    offset += 50

    time.sleep(1)