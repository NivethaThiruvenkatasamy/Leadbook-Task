## LEADBOOK PYTHON PROGRAMMING TASK

### Overview

Leadbook repo has 3 directories 
* [Python-scripts](Python-scripts) - Contains the main.py and Configuration.ini files
* [Output](Output) - Contains the 2 output files (company_index.json and company_profiles.json)
* [Test-cases](Test-cases) - Contains the 3 different 

All the python scipts were tested in **MacOS and Python 3.8.5**

### Architecture of the Crawler

* **[Main.py](Python-scripts/main.py)** 
  - It is the main script which contains the functions and logic to perform crawling.
  - Crawler has 3 functions
      - **Scrapping_fn** : Function to perform the data crawling of the given web url (complete page). Logic to handle requests error is implemented in this function. 
      - **company_profiles_parser** : Function to parse the company profiles information including all the contact persons details.
      - **contact_details_parser** : Function to parse the contact details from the detailed contacts page. This function is called from the company_profiles_parser function to get the detailed contacts.

* [Configuration.ini](Python-scripts/Configuration.ini)
  - It is the basic configuration file which consists of different sections like *GLOBAL, MONGODB & WEBPAGE*. 
  - All the configuration details such as MongoDB credentials, Data Directory & Base_url to crawl is specified in the file.

#### Requirements to run the script
* Python 3.7 & above
* MongoDB

#### Input


#### Output files

There are 2 output files will be created after running the script. 

#### TEST CASES 

* *Test Case 1* : [test_scrapping_company_index.py](Test-cases/test_scrapping_company_index.py)
It validates the basic company details of the company detail     
* *Test Case 2* : [test_company_profile.py](Test-cases/test_company_profile.py)
* *Test Case 3* : [test_contact_details_parser.py](Test-cases/test_contact_details_parser.py)

