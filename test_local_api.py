import requests

# url = "http://127.0.0.1:8000/posts/" # local url
url = "http://ec2-user@ec2-54-87-73-141.compute-1.amazonaws.com:8000"

post_data = {
    "title": "Post created with API",
    "content": "This is the content of the API post.",
    "authorid": "1"
    # "publisheddate" and "authorid", "blogid" are not required in the request body
}

response = requests.post(url, json=post_data)

if response.status_code == 200:
    print("Post created successfully:", response.json())
else:
    print("Error creating post:", response.text)

# use this new post for testing
new_test_post_id = response.json()['postid']

# test get all posts
url = "http://127.0.0.1:8000/posts/"
params = {
    "skip": 0,  # Offset
    "limit": 10  # Number of posts to fetch
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print("Posts retrieved successfully:", response.json())
else:
    print("Error retrieving posts:", response.text)

# Test get single post
url = f"http://127.0.0.1:8000/posts/{new_test_post_id}"

response = requests.get(url)

if response.status_code == 200:
    print("Post retrieved successfully:", response.json())
else:
    print("Error retrieving post:", response.text)


# test update single post
url = f"http://127.0.0.1:8000/posts/{new_test_post_id}"
update_data = {
    "title": "Updated Post Title",
    "content": "This is the updated content of the post.",
    "authorid": 1
}

response = requests.put(url, json=update_data)

if response.status_code == 200:
    print("Post updated successfully:", response.json())
else:
    print("Error updating post:", response.text)


url = f"http://127.0.0.1:8000/posts/{new_test_post_id}"

response = requests.delete(url)

if response.status_code == 200:
    print("Post deleted successfully:", response.json())
else:
    print("Error deleting post:", response.text)


