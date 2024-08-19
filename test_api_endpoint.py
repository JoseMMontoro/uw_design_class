import time
from pprint import pprint

import requests

base_url = "http://50.17.204.48:8000"

## GET
# test get all posts
pprint("GET ALL POSTS==")
url = f"{base_url}/posts"
params = {
    "skip": 0,  # Offset
    "limit": 10  # Number of posts to fetch
}

response = requests.get(url, params=params)

if response.status_code == 200:
    pprint(response.json())
else:
    pprint(response.text)

time.sleep(3)
pprint("GET SINGLE POST==")
# Test get single post
url = f"{base_url}/posts/1"

response = requests.get(url)

if response.status_code == 200:
    pprint(response.json())
else:
    pprint(response.text)

time.sleep(3)
## POST
pprint("POST CREATE POST==")
url = f"{base_url}/posts/"
post_data = {
    "title": "Post created with API",
    "content": "This is the content of the API post.",
    "authorid": "1"
    # "publisheddate" and "authorid", "blogid" are not required in the request body
}

response = requests.post(url, json=post_data)

if response.status_code == 200:
    pprint(response.json())
else:
    pprint(response.text)

# use this new post for testing
new_test_post_id = response.json()['postid']

time.sleep(3)
## UPDATE
pprint("UPDATE SINGLE POST==")
# test update single post
url = f"{base_url}/posts/{new_test_post_id}"
update_data = {
    "title": "Updated Post Title",
    "content": "This is the updated content of the post.",
    "authorid": 1
}

response = requests.put(url, json=update_data)

if response.status_code == 200:
    pprint(response.json())
else:
    pprint(response.text)

time.sleep(3)
## DELETE
pprint("DELETE SINGLE POST")
url = f"{base_url}/posts/{new_test_post_id}"

response = requests.delete(url)

if response.status_code == 200:
    pprint(response.json())
else:
    pprint(response.text)


