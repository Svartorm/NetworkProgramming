# Print the status code and its description from the HTTP response header on its.ac.id page
#    Example output: 200 OK

import requests

url = 'https://www.its.ac.id'

response = requests.get(url)

print(response.status_code, response.reason)
