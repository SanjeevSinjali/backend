from .models import JobModel
from apps.users.models import UserModel
from datetime import datetime, timedelta

provider1 = UserModel.objects.get(pk=1)
provider2 = UserModel.objects.get(pk=13)

# Dummy job data
job_data = [
    {
        "title": "Frontend Developer",
        "description": "Build and optimize user interfaces for web applications.",
        "company_name": "Tech Innovators Inc.",
        "location": "New York, USA",
        "job_type": "full-time",
        "salary_range": "80,000 - 100,000 USD per year",
        "required_experience": "2+ years",
        "skills_required": "React, JavaScript, HTML, CSS",
        "education_level": "Bachelor's in Computer Science",
        "job_level": "mid",
        "shift": "day",
        "posted_by_id": provider1,
        "application_deadline": datetime.now() + timedelta(days=30),
        "is_active": True,
    },
    {
        "title": "Senior Backend Developer",
        "description": "Design and maintain robust server-side applications.",
        "company_name": "Cloud Solutions Ltd.",
        "location": "Remote",
        "job_type": "contract",
        "salary_range": "120,000 - 140,000 USD per year",
        "required_experience": "5+ years",
        "skills_required": "Python, Django, REST APIs, PostgreSQL",
        "education_level": "Master's in Computer Science",
        "job_level": "senior",
        "shift": "flexible",
        "posted_by_id": provider2,
        "application_deadline": datetime.now() + timedelta(days=45),
        "is_active": True,
    },
    {
        "title": "Digital Marketing Specialist",
        "description": "Develop and execute marketing campaigns for our digital platforms.",
        "company_name": "Marketing Wizards",
        "location": "Los Angeles, USA",
        "job_type": "part-time",
        "salary_range": "40,000 - 60,000 USD per year",
        "required_experience": "3+ years",
        "skills_required": "SEO, Google Ads, Social Media Management",
        "education_level": "Bachelor's in Marketing",
        "job_level": "mid",
        "shift": "day",
        "posted_by_id": provider1,
        "application_deadline": datetime.now() + timedelta(days=20),
        "is_active": True,
    },
]

for job in job_data:
    JobModel.objects.create(**job)

print("Dummy job data added successfully!")
