# -*- coding: utf-8 -*-
"""
Created on Sat Jan 09 2021

@author: Nivetha T
"""

##################################################################################################
#import packages
import requests
from requests import get
from bs4 import BeautifulSoup
import string 
import re
import json
import configparser
from time import sleep
from random import randint
from pymongo import MongoClient
from datetime import datetime

def Scrapping_fn(url):
    '''
    Function to perform the crawling of the specified url and return the html
       
    STATUS CODE CHECK : if the status code is other then "200" 
    the code will suspend the execution for approx 60-80 seconds 
    and crawl the same page(url)
    '''
    
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://www.google.com/'}
    page = requests.get(url,headers)
    request_code = page.status_code
    if request_code != requests.codes.ok:
        sleep(randint(60,80))
        page = requests.get(url,headers)
    print (page.status_code)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def company_profiles_parser(company):
    '''
    Function to parse the company details from the company details page
    
    Given a source_url, this parser function will call the Scrapping_fn, 
    pulls the HTML data, perform the parsing of the required data and 
    returns the data as Dictionary
    
    Also, this function calls the contact_details_parser to get the details 
    of all the contacts by crawling the detailed contacts pages
    '''
    
    website_base_url = "https://www.adapt.io"
    href_url = company['source_url']
    url = website_base_url + href_url
    soup = Scrapping_fn(url)

    company_name_info = soup.find('div',{"class": "info-section"}).find('h1',{"class": "title"})
    company_name = company_name_info.text if company_name_info != None else None

    company_website_info = soup.find("span", {"class": "website-url"})
    company_website = company_website_info.text if company_website_info != None else None
    company_webdomain = company_website.split("www.")[1]

    company_industry_info = soup.find('ul',{"class" : "other-info-section"}).find("span",{"class": "info-title"},text='Industry')
    company_industry = company_industry_info.findNext('span').text if company_industry_info != None else None

    company_revenue_info = soup.find('ul',{"class" : "other-info-section"}).find("span",{"class": "info-title"},text='Revenue')
    company_revenue = company_revenue_info.findNext('span').text if company_revenue_info != None else None

    company_headcount_info = soup.find('ul',{"class" : "other-info-section"}).find("span",{"class": "info-title"},text='Head Count')
    company_headcount = company_headcount_info.findNext('span').text if company_headcount_info != None else None

    company_location_info = soup.find('ul',{"class" : "other-info-section"}).find("span",{"class": "info-title"},text='Location')
    company_location = company_location_info.findNext('span').text if company_location_info != None else None

    contact_html = soup.findAll('div',{"class": "top-contact-item"})
    contact_href = [x.find("a", itemprop="url").get('href').strip() for x in contact_html]
    
    #Creating a list with all the contact details
    full_contact_list = [contact_details_parser(each_href) for each_href in contact_href]
    
    #Initialise the dictionary and adding the all the details to the dictionary
    company_dict = {}
    company_dict['company name'] = company_name
    company_dict['company_location'] = company_location
    company_dict['company_website'] = company_website
    company_dict['company_webdomain'] = company_webdomain
    company_dict['company_industry'] = company_industry
    company_dict['company_employee_size'] = company_headcount
    company_dict['company_revenue'] = company_revenue
    company_dict['contact_details'] = full_contact_list
    return company_dict


def contact_details_parser(contact_href):
    '''
    Function to parser the contact details from the detailed contacts page
    
    Given a contact_url, this parser function calls the Scrapping_fn,
    pulls the HTML data, perform the parsing of the contacts details and 
    returns the data as dictionary
    
    It performs some of data cleaning/processing and creates a temporary 
    dictionary with all the contact detiails. 
    Required contact details can be added to the output dictionary 
    '''
    contact_dict = {}
    contact_info_html = Scrapping_fn(contact_href)
    contact_info_string = (contact_info_html.find("div",{"class": "master-contact-wrapper seo-contact-wrapper"})['ng-init']).rstrip(',;') 
    contact_info_string = re.sub(' (=) ?',r'\1', contact_info_string)  #Remove whitespaces before and after "=" symbol.   
    contact_details_list = contact_info_string.replace('\n',"").replace("'","").split(';') #Replace newline, single quotes and splits the text by semicolen and creates a list.
    contact_details_list = list(map(lambda x: x.strip(), contact_details_list))    #Stripping all whitespaces in the list
    contact_dict_temp = dict(map(lambda x: tuple(x.split('=')),contact_details_list)) #Creating a dict by transforming the list elements into a tuple by splitting with "="
    contact_dict['contact_name'] = contact_dict_temp['contactName']
    contact_dict['contact_jobtitle'] = contact_dict_temp['contactTitle']
    contact_dict['contact_department'] = contact_dict_temp['contactDepartment']
    contact_dict['contact_email_domain'] = contact_dict_temp['contactDomain']
    sleep(randint(10,20))
    return contact_dict

###############################################################################
# initialize global variables by reading the configuration file
# database details, urls, filenames and directory (where the JSON files are stored)

config = configparser.ConfigParser()
dummy = config.read('Configuration.ini')

mongo_url = config.get('MONGODB', 'db_url')
db_name = config.get('MONGODB', 'database')
index_collection = config.get('MONGODB','collection1')
profiles_collection = config.get('MONGODB','collection2')

#Getting the Base url of page for crawling from Config file
base_url = config.get('WEBPAGE','base_url')   #"https://www.adapt.io/directory/industry/telecommunications/"

data_dir = config.get('GLOBAL', 'data_dir')
index_file_name = config.get('GLOBAL','filename1')
profiles_file_name = config.get('GLOBAL','filename2')

#Creating the MongoDB connection using the url
conn = MongoClient(mongo_url)

##################################################################################################
# Loop to crawl the basic data for all companies and save as JSON file
##################################################################################################
print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Basic Company Details Crawling started...")
#Creating a list of uppercase Alphabets
alphabets_list = list(string.ascii_uppercase)

#Declaring empty output list of to store the Company name & Company url's
company_index_list = []

for alphabet in alphabets_list:
    url = base_url + str(alphabet) + "-1"
    soup = Scrapping_fn(url)
    company_div = soup.findAll("div", {"class": "list-item"})
    company_index_list = company_index_list + [{'company_name' : company.text, 'source_url': company.find('a').get('href')} for company in company_div]
    sleep(randint(2,10))
    print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Basic Company Details Crawling in-progress...")
print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Basic Company Details Crawling Complete...")

#Exporting the basic company data as a JSON file "company_index.json"  
with open(data_dir+index_file_name,'w') as outfile:
    json.dump(company_index_list,outfile)

##################################################################################################
# Insert the Basic Company Details to the MongoDB Collection
try:
    db_index = conn[db_name][index_collection]
    db_index.insert_many(company_index_list)
    print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " DB Insert Successful for the Collection : "+str(index_collection))
except:
    print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " DB Insert Failed for the Collection : "+str(index_collection))

##################################################################################################
# Loop to crawl the details data for all companies and save as JSON file
##################################################################################################
print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Company Profile Crawling started...")

#Declaring empty output list of to store the Company Details
company_profiles_list = []
i = 0
for company in company_index_list:
    try:
        company_profiles = company_profiles_parser(company)
        company_profiles_list.append(company_profiles)
    except:
        pass
    sleep(randint(4,10))
    if i > 50:
        break
    i=i+1
    print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Company Profile Crawling in-progress...")
print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Company Profile Crawling Complete")

#Exporting the basic company data as a JSON file "company_profiles.json"  
with open(data_dir+profiles_file_name,'w') as outfile:
    json.dump(company_profiles_list,outfile)


##################################################################################################
# Insert all the Company Details to the MongoDB Collection
try:
    db_profiles = conn[db_name][profiles_collection]
    db_profiles.insert_many(company_profiles_list)
    print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " DB Insert Successful for the Collection : "+str(profiles_collection))
except:
    print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " DB Insert Failed for the Collection : "+str(profiles_collection))

