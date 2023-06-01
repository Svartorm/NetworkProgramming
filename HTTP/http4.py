# Print the charset property in the Content-Type of the HTTP response header on the classroom.its.ac.id page
#     Example output: utf-8

import requests

url = 'https://classroom.its.ac.id'

response = requests.get(url)

print(response.encoding)