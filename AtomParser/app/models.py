from django.db import models

# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Job(models.Model):
    external_id = models.CharField(max_length=255)

    title = models.CharField(max_length=500)

    experience = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    employment_type = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    company = models.CharField(max_length=255, null=True, blank=True)

    is_remote = models.BooleanField(null=True)

    # salary and location are not included in the main table because they are dexlared as foreign tables
    skills = models.ManyToManyField(Skill)

    source = models.CharField(max_length=50)
    link = models.URLField(max_length=1000)

    last_updated = models.DateTimeField(null=True, blank=True)
    last_parsed = models.DateTimeField(auto_now=True)

    description = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "external_id"],
                name="unique_job_source_id"
            )
        ]


# foreign  tables
class Salary(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="salary")

    period = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    currency = models.CharField(max_length=3, null=True, blank=True)
    minimum = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    maximum = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

class Location(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="location")
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

