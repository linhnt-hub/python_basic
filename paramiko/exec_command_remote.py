def execute_remote_command(host, username, command):
    ssh_command = ['ssh', f'{username}@{host}', command]
    result = subprocess.run(ssh_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return result.stdout.strip()  # Return the output of the command
    else:
        print(f"Error executing command: {result.stderr.strip()}")
        return None
def execute_remote_command_use_passwd(host, username, passwd , command):
    import paramiko
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Connect to the remote server
        client.connect(host, username=username, password=passwd)
        # Execute the command to check network interfaces
        stdin, stdout, stderr = client.exec_command(f'{command}')
        # Read the command output
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            line = output.split('\n')
            for time in line:
                if time != '':
                    return time
                else: continue
        if error:
            print(error)
            return 0
    finally:
        # Close the connection
        client.close()
