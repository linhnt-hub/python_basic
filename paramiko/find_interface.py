def find_interface(hostname, username, password):
    import paramiko
    # Create an SSH client
    client = paramiko.SSHClient()
    # Automatically add untrusted hosts (not recommended for production)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Connect to the remote server
        client.connect(hostname, username=username, password=password)
        # Execute the command to check network interfaces
        stdin, stdout, stderr = client.exec_command('netstat -i | grep ens')
        # Read the command output
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            # st.code(output)  
            line = output.split('\n')
            list_int_temp = []
            for i in line:
                sub= i.split(' ')[0]
                if ("." not in sub) and (sub != ""):
                    list_int_temp.append(sub) 
            return set(list_int_temp)          
        if error:
            print(error)
    finally:
        # Close the connection
        client.close()
