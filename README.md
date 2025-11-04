# Skills manager

![Skills Manager](skillsManager/static/skillsManager/skillsManagerLogo.png)

Management of skills, certificates and projects for consulting companies.

![Static Badge](https://img.shields.io/badge/Made_with-Django-support)

# Installation

## Docker/Container deployment

Start the container with the [configured environment variables](#configuration) and expose the port 8000, e.g. with podman:

    podman run --rm -it -e DEBUG=true -e DJANGO_SUPERUSER_USERNAME=app -e DJANGO_SUPERUSER_PASSWORD=admin -e DJANGO_SUPERUSER_EMAIL=admin@company.com -e SECRET_KEY=verysecret -P gchr.io/devobagmbh/skillsmanager:latest

## Python native

Create a venv locally and activate it:

    python -m venv .venv
	. .venv/bin/activate

Install the requirements:

    pip -r requirements.txt

Set the required environment variables (see [below](#configuration)).

    export SECRET_KEY=secret

Initialize the database

    python manage.py migrate

Create a superuser

    python manage.py createsuperuser

For local testing, use 

    python manage.py runserver

For production deployment, use one of the recommended techniques as described in the [Django documentation](https://docs.djangoproject.com/en/5.2/howto/deployment/).

# Usage

# Configuration

Skills manager is configured using the following environment variables:

* DATABASE_URL: Database configuration for Django. See [the dj-database-url documentation](https://pypi.org/project/dj-database-url/) for details
* SECRET_KEY: The Django secret key
* APPLICATION_HOST: Host the application runs on (e.g. skills.company.com). Required if DEBUG is not set to true.
* DEBUG: Whether to run the application in Django debug mode [False]
* AZURE_ENABLED: Whether login via Azure entra id is enabled. See [the django-azure-auth documentation](https://pypi.org/project/django-azure-auth/) for details
* AZURE_CLIENT_ID: Azure client id
* AZURE_CLIENT_SECRET: Azure client secret
* AZURE_TENANT_ID: Azure tenant id
* AZURE_PROMPT: Whether to just accept the login (`none`) force to user to `login`, `consent` again or select an account (`select_account`) [none]
* AZURE_ROLES: Role to Django group mapping in JSON form. e.g.:
```json
{
        "95170e67-2bbf-4e3e-a4d7-e7e5829fe7a7": "GroupName1", # mapped to one Django group
        "3dc6539e-0589-4663-b782-fef100d839aa": ["GroupName2", "GroupName3"] # mapped to multiple Django groups
}
```


# Development

## Database design

```mermaid
erDiagram
	direction TB
	Profile {
		string given_name  "Given name of person"  
		string last_name  "Last name of person"  
		string email  "E-Mail address of person"  
		date active_since  "Person is available since"  
		date active_until  "Person is available until"  
	}

	ProfileMeta {
		ref profile FK "Reference to profile"  
		date birthday  "Birthday of person"  
		image photo  "Photo of person"  
	}

	Skill {
		string name  "Skill name"  
		text description  "Description of skill"  
		ref related_skills FK "Other skills related to this skill"  
	}

	ProfileSkillReference {
		ref profile FK "Referenced profile"  
		ref skill FK "Referenced skill"  
		int level  "A level of proficiency"  
		int favorite  "How much the referenced person likes to provide the skill"  
		text remarks  "Additional remarks about this reference"  
	}

	CertificateVendor {
		string name  "Name of vendor"  
	}

	Certificate {
		ref vendor FK "Referenced certificate vendor"  
		string name  "Name of certificate"  
		text description  "Certificate description"  
	}

	ProfileCertificateReference {
		ref profile FK "Referenced profile"  
		ref certificate  "Referenced certificate"  
		date active_since  "Certificate is assigned to person since"  
		date active_until  "Certificationis valid until this date"  
	}

	Customer {
		string name  "Name of the customer"  
		ref parent_customer FK "Parent customer"  
		date active_since  "Active customer since"  
		date active_until  "Active customer until"  
	}

	Project {
		ref customer FK "Referenced customer"  
		string name  "Name of project"  
		text description  "Description of project"  
		date active_since  "Project is active since this date"  
		date active_until  "Project ended at this date"  
	}

	ProfileProjectReference {
		ref profile FK "Referenced profile"  
		ref project FK "Referenced project"  
		date active_since  "Person is active in this project since this date"  
		date active_until  "Person is active in this project until this date"  
		text remarks  "Additional remarks"  
	}

	ProjectLog {
		ref project FK "Referenced project"  
		timestamp timestamp  "Timestamp of log entry"  
		text notice  "Log about project"  
	}

	CustomerLog {
		ref customer FK "Referenced customer"  
		timestamp timestamp  "Timestamp of log"  
		text notice  "Notice about customer"  
	}

	Profile||--||ProfileMeta:"contains private data"
	Profile||--o{ProfileSkillReference:"has skill"
	Skill||--o{ProfileSkillReference:"is linked to"
	CertificateVendor||--o{Certificate:"issues"
	Certificate||--o{ProfileCertificateReference:"is linked to"
	Profile||--o{ProfileCertificateReference:"is certified"
	Customer||--o{Project:"manages"
	Project||--o{ProfileProjectReference:"linked to"
	Profile||--o{ProfileProjectReference:"is engaged in"
	Customer||--o{CustomerLog:"describes"
	Project||--o{ProjectLog:"describes"


```