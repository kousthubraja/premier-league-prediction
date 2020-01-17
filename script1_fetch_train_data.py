import requests

url = "http://www.football-data.co.uk/mmz4281/1920/E0.csv"

print("--- Fetching data... ---")
request = requests.get(url)
with open('E0.csv', 'wb') as f:
    f.write(request.content)
print("--- Fetching data complete ---")
