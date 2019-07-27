# Get Profile Data Of Repo Stargazers GraghQL

This Python has almost the same function as [minimaxir / get-profile-data-of-repo-stargazers](https://github.com/minimaxir/get-profile-data-of-repo-stargazers), but rewritten using the GraphQL API of GitHub, which is much more faster and can overcome the scraw limit in page 1334 using the REST API.

![GH Limit using the REST API](./gh-api-limit.png)

I wrote this on my personal analysis project, the "StarTime-StarCount" chart in that project as below.

![](./chart.png)

This program will store stargazers' "username","name","blog", "company", "bio","avatar_url","hireable" , "num_followers", "num_following","created_at","star_time" in csv format.

# Usage

1. Get an access token from your GitHub account.

2. Set timezone in line 103 and 107, default is UTC-5.

3. Run the script with:

   ```bash
   python main.py -r 'username/reponame' -t <GitHub Token>
   ```

# Author

Nova Kwok

# LICENSE

GPLv3
