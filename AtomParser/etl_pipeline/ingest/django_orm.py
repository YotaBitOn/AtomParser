from app.models import Job, Skill, Location, Salary

from etl_pipeline.jooble.jooble_norm import normalize as normalize_jooble
from etl_pipeline.remoteok.remoteok_norm import normalize as normalize_remoteok
from etl_pipeline.workua.workua_norm import normalize as normalize_workua

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import json
with open('config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
parsers = {
     normalize_jooble : config['PARSE_JOOBLE'],
     normalize_remoteok : config['PARSE_REMOTOK'],
     normalize_workua : config['PARSE_WORKUA']
}

def save_job(job_data):
    obj, pre_existed = Job.objects.update_or_create(
        source=job_data["source"],
        external_id=job_data["external_id"],
        defaults={
            'external_id': job_data["external_id"],
            "title": job_data["title"],

            'experience': job_data["experience"],
            'employment_type': job_data["employment_type"],

            'company': job_data["company"],

            'is_remote': job_data["is_remote"],
            'source': job_data["source"],
            'link': job_data["link_to_page"],
            'last_updated': job_data["last_updated"],
            'last_parsed': job_data["last_parsed"],
            'description': job_data["description"],

        }
    )

    #skills
    skills = []

    for skill_name in job_data["tags"]:
        skill, _ = Skill.objects.update_or_create(
            name=skill_name
        )
        skills.append(skill)

    obj.skills.set(skills)

    # salary
    Salary.objects.update_or_create(
        job=obj,
        defaults={
            "currency": job_data["currency"],
            "minimum": job_data["min_salary"],
            "maximum": job_data["max_salary"],
        }
    )

    # location
    Location.objects.update_or_create(
        job = obj,
        defaults={
            "city": job_data["location_city"],
            "country": job_data["location_country"],
        }
    )

def ingest():
    for parser, enabled in parsers.items():
        if enabled:
            logger.info(f'Starting ingesting objects from {parser.__name__}')
            gen = parser()
            while True:
                try:
                    job = next(gen)
                except StopIteration:
                    logger.info('No more jobs to normalize, finishing normalization')
                    break

                if job is None:
                    logger.error('Job object is empty,  finishing normalization')
                    break

                try:
                    save_job(job)
                    logger.info(f'Saved job {job["external_id"]} from {job["source"]}')
                except Exception as e:
                    logger.error(f'Error saving job {job["external_id"]} from {job["source"]}. Error: {e}')
            logger.info(f'Finished ingesting objects from {parser.__name__}')
        else:
            continue
if __name__ == '__main__':
    ingest()