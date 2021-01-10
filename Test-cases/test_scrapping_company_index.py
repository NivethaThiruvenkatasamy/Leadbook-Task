import requests
from requests import get
from bs4 import BeautifulSoup

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


def test_Scrapping_fn():
	test_url = "https://www.adapt.io/directory/industry/telecommunications/A-1"
	test_output = {"company_name": "A & L Personnel Services", "source_url": "/company/a---l-personnel-services"}
	
	soup = Scrapping_fn(test_url)
	company = soup.find("div", {"class": "list-item"})
	crawler_output = {'company_name' : company.text, 'source_url': company.find('a').get('href')}
	assert crawler_output == test_output