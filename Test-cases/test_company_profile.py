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

def company_profiles_parser(company):
    '''
    Function to parse the company details from the company details page
    
    Given a source_url, this parser function will call the Scrapping_fn, 
    pulls the HTML data, perform the parsing of the required data and 
    returns the data as Dictionary
    
    Also, this function calls the contact_details_parser to get the details 
    of all the contacts by crawling the detailed contacts pages
    '''
    
    #website_base_url = "https://www.adapt.io"
    #href_url = company['source_url']
    #url = website_base_url + href_url
    url = company
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
    return contact_dict



def test_company_profiles_parser():
    test_url = "https://www.adapt.io/company/a---l-personnel-services"
    test_output = {"company name": "A & L Personnel Services", "company_location": "Gregory, Michigan", "company_website": "http://www.cac.net", "company_webdomain": "cac.net", "company_industry": "Telecommunications", "company_employee_size": None, "company_revenue": None, "contact_details": [{"contact_name": "Doug Waite", "contact_jobtitle": "Owner", "contact_department": "Finance & Administration", "contact_email_domain": "cac.net"}, {"contact_name": "Jim Mason", "contact_jobtitle": "Club Director", "contact_department": "Other", "contact_email_domain": "cac.net"}]}
    crawler_output = company_profiles_parser(test_url)
    assert crawler_output == test_output
