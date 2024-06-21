
def gitCommit(file_commit, commit_message, repo_path = config.get('config_git', {}).get('repo_path'), remote = config.get('config_git', {}).get('remote'), branch_name = config.get('config_git', {}).get('branch_name')):
    repo = Repo(repo_path)
    print(f"repo is {repo}")
    ## git switch 
    try:
      repo.git.switch(branch_name)
      print(f"Switched to branch {branch_name}.")
    except Exception as e:
      logging.exception('Switched to branch failed due to {}'.format(e))
      sys.exit()
    ## git stash
    try:
      repo.git.stash('save')
      print("Stashed changes successfully")
    except Exception as e:
      logging.exception('Create stash failed due to {}'.format(e))
      sys.exit()
    ## git pull
    try:  
      repo.remotes[remote].pull(branch_name)
      print(f"Pulled changes from {remote}/{branch_name}.")
    except Exception as e:
      logging.exception('Pull changes from github failed due to {}'.format(e))
      sys.exit()   
    ## git stash apply
    try:
      repo.git.stash('apply')
      print("Applied the latest stash successfully.")
    except Exception as e:
      logging.exception('Applied the latest stash failed due to {}'.format(e))
      sys.exit()
    ## git add
    try:
      # repo.index.add(file_commit)
      subprocess.run(['git', 'add', file_commit], cwd=repo_path)
      print("Git add successful.")
    except Exception as e:
      print("An exception occurred: %s" %e)
      sys.exit()
    ## git commit 
    try:
      # repo.index.commit(commit_message)
      subprocess.run(['git', 'commit' , '-m', commit_message], cwd=repo_path)
      print("Git commit successful.")
    except Exception as e:
      logging.exception('Git commit failed due to {}'.format(e))
      sys.exit()        
    ## git push 
    try:
      # repo.git.push(remote, branch_name)
      subprocess.run(["git", "push"], cwd=repo_path)
      print(f"Pushed to {remote}/{branch_name} successfully.")
    except Exception as e:
      logging.exception('Git push failed due to {}'.format(e))
      sys.exit()     

  ## check pull request and create git pull request to master branch
def gitpr(title, body, repo_path = config.get('config_git', {}).get('repo_path'), base_branch = config.get('config_git', {}).get('base_branch'), branch_name = config.get('config_git', {}).get('branch_name'), repo = config.get('config_git', {}).get('repo'), owner = config.get('config_git', {}).get('owner'), token_git = config.get('config_git', {}).get('token_git')):
    base_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"token {token_git}",
        "Accept": "application/vnd.github.v3+json",  # Use GitHub API v3
    } 
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        pull_requests = response.json()      
        if pull_requests:
          for pr in pull_requests:
              source_branch = pr['head']['ref']  
              print(f"Pull Request #{pr['number']}: Source Branch: {source_branch}")
              if source_branch == branch_name:
                 print(f"Pull request already exists for {owner}:{branch_name}.")
                 return True
              else:
                print(f"No existing pull request for {owner}:{branch_name}.")
                data = {
                  'title': title,
                  'body': body,
                  'head': branch_name,
                  'base': base_branch,
                }
                response = requests.post(base_url,headers=headers,json=data)
                if response.status_code == 201:
                    print("Pull request created successfully.")
                    pull_request_info = response.json()
                    print(f"Pull Request URL: {pull_request_info['html_url']}")
                else:
                    print(f"Failed to create pull request. Status code: {response.status_code}")
                    print(f"Error message: {response.text}")
    else:
        print(f"Failed to fetch pull requests. Status code: {response.status_code}")
        return False
