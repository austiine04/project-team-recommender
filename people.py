import requests
import os

print "access token = %s" % os.environ['ACCESS_TOKEN']
print "api url" % os.environ['API_URL']

auth_header = {'Authorization': os.environ['ACCESS_TOKEN']}
working_offices = ['Sydney', 'Melbourne', 'Brisbane', 'Perth']
API_URL = os.environ['API_URL']

def get_page_count_for(office_name):
    url = API_URL % office_name
    response = requests.head(url, headers=auth_header)
    return int(response.headers['X-Total-Pages'])

def save_to_file(json_string, page_number, office):
    file = open('data/people/'+ office + '_page_%d' % page_number + '.json', 'w+')
    file.write(json_string)
    file.close()

def _build_url_from(office_name, page_number):
    url = API_URL % office_name
    page_query = '&page=%d' % page_number
    return url + page_query

def fetch_people_for(office_name):
    print 'fetching people for %s office' % office_name
    current_page = 1
    total_page_count = get_page_count_for(office_name)
    while current_page <= total_page_count:
        url = _build_url_from(office_name, current_page) 
        print 'fetching page %d, url %s' % (current_page, url) 
        response = requests.get(url, headers=auth_header)
        save_to_file(response.content, current_page, office_name)
        current_page += 1

for office in working_offices:
    fetch_people_for(office)
