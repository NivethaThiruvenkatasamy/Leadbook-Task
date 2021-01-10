import requests
from requests import get
from bs4 import BeautifulSoup
import re

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
    return contact_dict



def test_contact_details_parser():
    test_url = "https://www.adapt.io/contact/jim-mason/876039702"
    test_output = {"contact_name": "Jim Mason", "contact_jobtitle": "Club Director", "contact_department": "Other", "contact_email_domain": "cac.net"}
    
    crawler_output = contact_details_parser(test_url)
    assert crawler_output == test_output