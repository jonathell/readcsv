import pandas as pd

fileToScan='Maven_project_1-67-stars_pages.csv'

repoList = list()
reposToScan = list()
notGitRepo = list()

df = pd.read_csv(fileToScan)
urls = df.repo_link
name = df.name

for data in range(len(urls)):
    if("github.com" in urls[data]):
        if("//" in urls[data]):
            head, body = urls[data].split('//')

            # Ensure it is https:// before github.com
            repoURL = "https://" + body[body.find("github.com"):]
        else:
            repoURL = urls[data].replace(":", "/")
            repoURL = "https://" + repoURL[repoURL.find("github.com"):]

        # Ensure only 2 sections after github.com
        locationOfFirstSlashAfterGithub = repoURL[repoURL.find("github.com"):].find("/") + 8
        locationOfSecondSlashAfterGithub = repoURL[locationOfFirstSlashAfterGithub+1:].find("/") + locationOfFirstSlashAfterGithub + 1

        #Check if there is a 3rd slash
        locationOfThirdSlashAfterGithub = repoURL[locationOfSecondSlashAfterGithub+1:].find("/")
        if(locationOfThirdSlashAfterGithub != -1):
            repoURL = repoURL[:locationOfSecondSlashAfterGithub+locationOfThirdSlashAfterGithub+1]

        locationOfSlash = repoURL.rfind("/")

        repoName = repoURL[locationOfSlash+1:]

        if(repoName not in repoList):
            if(repoName.endswith(".git")):
                repoName = repoName.replace(".git","")
                if(repoName not in repoList): #check if after remove .git and it still not exist
                    reposToScan.append([repoName, repoURL])
                    repoList.append(repoName)
            else:
                reposToScan.append([repoName, repoURL])
                repoList.append(repoName)

    else:
        notGitRepo.append([name[data], urls[data]])
        df = pd.DataFrame(notGitRepo, columns=["repoName", "repoURL"])
        df.to_csv('notGit.csv')

# df = pd.DataFrame(reposToScan, columns=["repoName", "repoURL"])
# df.to_csv('testme.csv')

