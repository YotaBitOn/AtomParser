import logging
import remoteok_parser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

employment_types = ['Internship', 'Part Time', 'Full Time', 'Contract', 'Freelance']
experience_levels = ['Junior', 'Middle', 'Senior']
#Last updated, Locations, Tags, Salary

def norm():
    gen = remoteok_parser.parse()

    normalized_jobs = []
    counter = 0
    while True:


        job = next(gen)
        if not job:
            logger.error(f'No job found, skipping...')
            continue
        normalized_job = job.copy()

        normalized_job['location_city'] = None
        normalized_job['employment_type'] = None
        normalized_job['experience'] = None
        normalized_job['min_salary'] = None
        normalized_job['max_salary'] = None
        normalized_job['currency'] = None

        normalized_job['last_updated'] = normalized_job['last_updated'].replace('T', ' ').split('+')[0]

        for exp in experience_levels:
            if exp in normalized_job['tags']:
                normalized_job['experience'] = exp
                break
        for emp in employment_types:
            if emp in normalized_job['tags']:
                normalized_job['employment_type'] = emp
                break

        loc = normalized_job['location']
        if len(loc) > 0 and loc[0] :
            if '🌏 Worldwide' in loc:
                normalized_job['location_country'] = None
            else:
                normalized_job['location_country'] = ' '.join( loc[0].strip().split(' ')[1:] ).lower()
        else:
            normalized_job['location_country'] = None

        del normalized_job['salary']
        del normalized_job['location']

        for k, v in normalized_job.items():
            print(k, ' : ', v)

norm()
