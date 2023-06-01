# Print the Content-Encoding version of the HTTP response header on its.ac.id web page
#     Example output: gzip

import requests

url = 'https://www.its.ac.id'

response = requests.get(url)

print(response.headers['Content-Encoding'])