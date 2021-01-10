## LEADBOOK PYTHON PROGRAMMING TASK

### Overview

Leadbook repo has 3 directories 
* [Python-scripts](Python-scripts) - Contains the main.py and Configuration.ini files
* [Output](Output) - Contains the 2 output files (company_index.json and company_profiles.json)
* 

All the python scipts were tested in Mac OS and Python

Requirements to run the script
* Python 3.7 & above
* MongoDB

### Architecture of the Crawler

* Main.py - It is the main script which contains the functions and logic to perform crawling. 
* Configuration.ini 
  - It is the basic configuration file which consists of different sections like *GLOBAL, MONGODB & WEBPAGE*  

#### Input


#### Output files

There are 2 output files will be created after running the script. 



#### TEST CASES 

* *Test Case 1* : [test_scrapping_company_index.py](Test-cases/test_scrapping_company_index.py)
It validates the basic company details of the company detail     
* *Test Case 2* : [test_company_profile.py](Test-cases/test_company_profile.py)
* *Test Case 3* : [test_contact_details_parser.py](Test-cases/test_contact_details_parser.py)

