## LEADBOOK PYTHON PROGRAMMING TASK

### Overview of repo

Leadbook repo has 3 directories 
* [Python-scripts](Python-scripts) - Contains the `main.py` and `Configuration.ini` files.
* [Test-cases](Test-cases) - Contains the 3 test-case files (`test_scrapping_company_index.py`, `test_company_profile.py` and `test_contact_details_parser.py`).
* [Output](Output) - Contains the 2 output files (`company_index.json` and `company_profiles.json`) for reference. 

### Architecture of the Crawler

Crawler is implemeted in a single script(`main.py`) with 3 functions. It also has the configuration file(`configuration.ini`)

* **[Main.py](Python-scripts/main.py)** 
  - It is the main script which contains the functions and logic to perform crawling.
  - Crawler has 3 functions
      - **`Scrapping_fn`** : Function to perform the data crawling of the given web url (complete page). Logic to handle requests error is implemented in this function. 
      - **`company_profiles_parser`** : Function to parse the company profiles information including all the contact persons details.
      - **`contact_details_parser`** : Function to parse the contact details from the detailed contacts page. Some cleaning and processing of the data is also perfomed here. This function is called from the `company_profiles_parser` function to get the detailed contacts.
  - Once data is crawled and procesed in the required format, the data is exported as JSON file and also data is inserted into the MongoDB Collections using `insert_many`

* **[Configuration.ini](Python-scripts/Configuration.ini)**
  - It is the basic configuration file which consists of different sections like **`GLOBAL, MONGODB and WEBPAGE`**. 
  - All the configuration details such as MongoDB credentials, Data Directory & Base_url to crawl is specified in the file.

All the python scipts were tested in **MacOS and Python 3.8.5**

#### Prerequisites to run the script
* Python 3.7 & above
* MongoDB

#### Test Cases 

Test Cases were written using **`pytest`** framework. There are 3 test cases in the [Test-cases](Test-cases) directory. Here are the details

* *Test Case 1* : [test_scrapping_company_index.py](Test-cases/test_scrapping_company_index.py) 
* *Test Case 2* : [test_company_profile.py](Test-cases/test_company_profile.py)
* *Test Case 3* : [test_contact_details_parser.py](Test-cases/test_contact_details_parser.py)

#### Output Files

Output JSON files are posted in [Output](Output) folder. There are 2 output files

1. `company_index.json` - It has all the basic details of all the companies (A to Z). 
2. `company_profiles.json` - It has company profile details with all the contact details for first 50 Companies.

#### Running the Script

* Clone or download the `Leadbook-Task` repository locally 
* Update the MongoDB `hostname`, `port`, `database`, `collection1`, 'collection2` , 'data_dir' in the **`configuration.ini`**
* Run the `Python-scripts/main.py` script in the terminal or command-prompt

#### Why Mongo DB ? 

* Mongo DB is chosen as the database engine because it is faster than the tradional SQL Databases. 
* Since MongoDB is the document database, storing the text documents & JSON type data is much suitable. 
* Schema less database , preferred in storing the raw data. 
