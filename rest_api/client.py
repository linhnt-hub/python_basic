import requests

# Replace 'http://your-server-url.com/upload' with the actual URL of your server endpoint
url = 'http://10.99.94.2:5000/upload'

# Path to the file you want to send
file_path = '/home/juniper/python/data.csv'

# Open the file in binary mode
with open(file_path, 'rb') as file:
    # Send a POST request with the file attached
    response = requests.post(url, files={'file': file})

# Check the response
if response.status_code == 200:
    print("File uploaded successfully.")
else:
    print("Error occurred while uploading file:", response.status_code)
