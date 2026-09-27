import urllib.request
response = urllib.request.urlopen("https://api.github.com")
print("Status Code:", response.status)