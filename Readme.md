# RSS FEED SENDER #

Program allows user managing RSS addresses (adding, deleting, updating) and then send summarized news from all added RSS URLs to
given email address. Program uses JQuery for making API calls. Endpoints are listed below.

Program was tested and works up to 100 RSS addresses.

## Usage ##

![website](./docs/Screenshot_24.png)

This application has been build using:

* SendGrid
* Flask (with Jinja2 template engine)
* SQLAlchemy, Marshmallow
* JQuery
* PostgreSQL database
* Jenkins
* pytest
* Selenium Framework

## Endpoints ##

All responses are JSON responses.

* GET /urls - returns URL list
* GET /urls/\<id> - returns URL details
* POST /urls - adds new URL
* DELETE /urls/\<id> - deletes URL of the given ID
* PUT /urls/\<id> - updates URL of the given ID
* GET /rss - returns the parsed RSS Feed content. The example response looks like this:
  ![response](./docs/response.png)
  
---------

## Tests ##

Application contains:

- unit test
- integration tests
- e2e tests
- [test cases for manual testing](tests/test_cases.md)


## CI/CD ##

This project uses Jenkins as CI/CD tool. The pipeline was built in YAML file and consists of following steps:

Step 1. Checking code for vulnerabilities with Bandit library  
Step 2. Unit tests  
Step 3. Integration tests  
Step 4. Selenium E2E tests
Step 5. Deploying app to production  

---------

## External services ##

This application uses SendGrid API for sending emails. To learn more about SendGrid service
visit [https://sendgrid.com](https://sendgrid.com).
