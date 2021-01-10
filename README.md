## LEADBOOK PYTHON PROGRAMMING TASK

### Overview of repo

Leadbook repo has 3 directories 
* [Python-scripts](Python-scripts) - Contains the `main.py` and `Configuration.ini` files
* [Test-cases](Test-cases) - Contains the 3 test-case files (`test_scrapping_company_index.py`, `test_company_profile.py` and `test_contact_details_parser.py`)
* [Output](Output) - Contains the 2 output files (`company_index.json` and `company_profiles.json`) for reference

### Architecture of the Crawler

Crawler is implemeted in a single script(`main.py`) with 3 functions. It also has the configuration file(`Configuration.ini`)

* **[Main.py](Python-scripts/main.py)** 
  - It is the main script which contains the functions and logic to perform crawling.
  - Crawler has 3 functions
      - **`Scrapping_fn`** : Function to perform the data crawling of the given web url (complete page). Logic to handle requests error is implemented in this function. 
      - **`company_profiles_parser`** : Function to parse the company profiles information including all the contact persons details.
      - **`contact_details_parser`** : Function to parse the contact details from the detailed contacts page. Some cleaning and processing of the data is also perfomed here. This function is called from the `company_profiles_parser` function to get the detailed contacts.
  - Once data is crawled and procesed in the required format, the data is exported as JSON file and also data is inserted into the MongoDB Collections using `insert_many`

* **[Configuration.ini]**(Python-scripts/Configuration.ini)
  - It is the basic configuration file which consists of different sections like **`GLOBAL, MONGODB and WEBPAGE`**. 
  - All the configuration details such as MongoDB credentials, Data Directory & Base_url to crawl is specified in the file.

All the python scipts were tested in **MacOS and Python 3.8.5**

#### Prerequisites to run the script
* Python 3.7 & above
* MongoDB

#### Test Cases 

Test Cases were written using **`pytest`** framework. There are 3 test cases in the [Test-cases](Test-cases) directory. Here are the details

* *Test Case 1* : [test_scrapping_company_index.py](Test-cases/test_scrapping_company_index.py)
It validates the basic company details of the company detail     
* *Test Case 2* : [test_company_profile.py](Test-cases/test_company_profile.py)
* *Test Case 3* : [test_contact_details_parser.py](Test-cases/test_contact_details_parser.py)

