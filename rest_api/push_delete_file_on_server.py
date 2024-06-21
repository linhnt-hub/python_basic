def push_file_to_server_rest_api(server, port, file_path):
    import requests
    # Replace 'http://your-server-url.com/upload' with the actual URL of your server endpoint
    url = f'http://{server}:{port}/upload'

    # Path to the file you want to send
    # file_path = '/home/juniper/python/data.csv'

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Send a POST request with the file attached
        response = requests.post(url, files={'file': file})

    # Check the response
    if response.status_code == 200:
        print("File uploaded successfully.")
        return 200
    else:
        print("Error occurred while uploading file:", response.status_code)
def delete_file_on_server(server, port, file_path):
    import requests

    url = f'http://{server}:{port}/delete'

    # Make a POST request to the server to delete the file
    response = requests.post(url, data={'filename': file_path})

    # Check the response
    if response.status_code == 200:
        print("File deleted successfully.")
    elif response.status_code == 404:
        print("File not found on the server.")
    else:
        print("Error occurred while deleting file:", response.status_code)
