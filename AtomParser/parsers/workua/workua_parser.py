import datetime
import random
import time

import bs4
import requests, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

url = "https://www.work.ua"
tags = 'python'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    #"Referer": "https://www.google.com/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


session = requests.Session()


def fetch_job_page(link):
    local_url = url + link
    try:
        response = session.get(
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

def fetch_search_results(page = 1):
    local_url = url + '/jobs-' + tags
    print(local_url)
    params = {
        "page": page,
    }
    try:
        logger.info(f'Fetching from WorkUa with page {page} and tags {tags}')
        response = session.get(
            local_url,
            headers=headers,
            params=params,
            timeout=15
        )
    except Exception as e:
        logger.error(e)
        return None

    html = bs4.BeautifulSoup(response.text, 'html.parser')

    if html is None or html.get_text(strip=True) == '':
        logger.error('No data were acquired')
        return None

    logger.info(f'Successfully fetched data from page {page}, extracting job links...')

    return html

def process_job(job, link):
    source = 'workua'
    link_to_page = url+link
    external_id = link.rstrip("/").split("/")[-1]
    last_parsed = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    employment_type = None
    experience = None
    is_remote = False
    salary = None
    location = None
    local_tags = []

    full_title = job.find(attrs={'id': 'h1-name'})
    full_title = full_title.get_text(strip=True) if full_title else None

    time_container = job.find('time')
    last_updated = time_container['datetime'] if time_container else None

    container = job.find('div', attrs={'class': 'wordwrap'})
    info_list = container.find('ul', recursive=False)

    company_container = info_list.find('a', attrs={'class': 'inline'})
    company = company_container.get_text(strip=True) if company_container else None

    is_remote_container_prev = info_list.find('span', attrs={'class': 'glyphicon-remote'})

    is_remote = (is_remote_container_prev != None)

    et_ex_container = None
    location_container = None
    salary_container = None

    li_elements = info_list.find_all('li')
    for li_element in li_elements:
        if li_element.find('span', attrs={'class': 'glyphicon-hryvnia-fill'}):
            salary_container = li_element

        if li_element.find('span', attrs={'class': 'glyphicon-map-marker'}):
            location_container = li_element

        if li_element.find('span', attrs={'class': 'glyphicon-tick'}):
            et_ex_container = li_element

    salary = salary_container.get_text(strip=True) if salary_container else None

    location = location_container.get_text(strip=True) if location_container else None

    if et_ex_container:
        et_ex_text = et_ex_container.get_text(strip=True)

        et_ex = et_ex_text.split('.')

        employment_type = et_ex[0]
        experience = et_ex[1]

    description = (container.find('div', attrs={'class': 'description'}) or
                   container.find('div', attrs={'class': 'company-description'}) or
                   container.find('div', attrs={'id': 'job-description'}))
    description = description.get_text(" ", strip=True) if description else None

    tags_container = container.find('ul', attrs={'class': 'flex-wrap'})
    if tags_container:
        local_tags = [
            tag.get_text(strip=True)
            for tag in tags_container.find_all("li")
        ]
    print("External id: ", external_id)
    print("Title: ", full_title)
    print("Salary: ", salary)
    print("Experience: ", experience)
    print("Employment type: ", employment_type)
    print("Tags: ", local_tags)
    print("Company: ", company)
    print("Location: ", location)
    print("Is remote: ", is_remote)
    print("Source: ", source)
    print("Link to page: ", link_to_page)
    print("Last updated: ", last_updated)
    print("Last parsed: ", last_parsed)
    print("Description: ", description, '...')

def extract_job_links(jobs_html):
    links = []

    #print(jobs_html)
    link_containers = jobs_html.find_all('div', attrs={'class': 'card-hover' })

    print(f'Found {len(link_containers)} job links')
    for container in link_containers:
        link = container.find('a')['href']
        links.append(link)
    return links

page = 1

#link = '/jobs/8119980/'
#html = fetch_job_page(link)
#process_job(html, link)
#quit()
while True:

    search_results_html = fetch_search_results(page = page)

    if not search_results_html:
        break

    links = extract_job_links(search_results_html)

    if not links:
        logger.info(f'No job links for {tags} were found, stopping...')
        break

    logger.info(f'Found {len(links)} job links for {tags}, parsing job pages...')


    for link in links:

        html = fetch_job_page(link)

        if not html:
            logger.info(f'No page on link {link} were found, skipping...')
            continue

        logger.info(f'Processing job on {link} ...')
        process_job(html, link)
    page += 1
    time.sleep(random.uniform(2,5))