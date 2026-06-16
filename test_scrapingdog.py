import requests

API_KEY = "6a2be943bc8b6ea014acec5a"
VIDEO_ID = "c64hqovEG-U"

url = "https://api.scrapingdog.com/youtube/transcripts"

params = {
    "api_key": API_KEY,
    "v": VIDEO_ID
}

response = requests.get(url, params=params)

print("STATUS CODE:")
print(response.status_code)

print("\nRAW RESPONSE:")
print(response.text)

try:
    print("\nJSON:")
    print(response.json())
except Exception as e:
    print("\nJSON PARSE ERROR:")
    print(e)