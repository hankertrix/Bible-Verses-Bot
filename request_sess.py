# Module that contains the request session

import httpx

# Request headers
headers = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.3",
  "Accept-Language": "en-US,en;q=0.9",
  "DNT": "1",
  "Referer": "https://www.google.com/"
}


# Starts a httpx client to search the verses faster
s = httpx.Client(headers=headers, follow_redirects=True)
