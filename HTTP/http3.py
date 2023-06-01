# Print the HTTP version of the HTTP response header on the its.ac.id web page
#     Example output: HTTP/1.1

import requests 

url = 'https://www.its.ac.id'

response = requests.get(url)

version = response.raw.version

print(version)