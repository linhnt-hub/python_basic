def push_file_to_server_by_ftp(hostname, username, password, local_path, remote_path):
    import paramiko
    # Define the SFTP connection parameters
    # hostname = ''
    port = 22
    # username = ''
    # password = ''

    # Define the local file path and the remote destination path
    # local_path = '/path/to/local/file.txt'
    # remote_path = '/path/to/remote/destination/file.txt'

    # Establish an SSH transport and SFTP session
    transport = paramiko.Transport((hostname, port))
    try:
        transport.connect(username=username, password=password)
    except Exception as e:
        print(f'Error connect to server, Error: {e}')
    sftp = paramiko.SFTPClient.from_transport(transport)
    # Upload the file
    sftp.put(local_path, remote_path)
    # Close the SFTP session and the SSH transport
    sftp.close()
    transport.close()
