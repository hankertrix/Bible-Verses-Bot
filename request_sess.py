# Module that contains the request session

import httpx

# Request headers
headers = {
  "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55",
  "accept-language" : "en-US,en;q=0.9", 
  "DNT" : "1",
  "Referer" : "https://www.google.com/"
}


# Starts a httpx client to search the verses faster
s = httpx.Client(headers=headers, follow_redirects=True)