#!/usr/bin/env python
__author__ = "Nova Kwok"
__license__ = "GPLv3"
import graphene
import csv
import datetime
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t','--token',required=True,help="The GitHub Token.")
parser.add_argument('-r','--repo',required=True,help="The GitHub Repo,in the form like 'user/repo'.")
args = parser.parse_args()

owner = args.repo.split('/')[0]
repo = args.repo.split('/')[1]

headers = {"Authorization": "token "+args.token}

fields = ["username","name","blog", "company", "bio","avatar_url","hireable" , "num_followers", "num_following","created_at","star_time"]

def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


query = """
query {{
  repository(owner:"{0}", name:"{1}") {{
    stargazers(first:100,after:{2}) {{
      pageInfo {{
        endCursor
        hasNextPage
        hasPreviousPage
        startCursor
      }}
      edges {{
        starredAt
        node {{
          login
          name
	  bio
          company
          isHireable
          avatarUrl
          createdAt
          websiteUrl
          followers(first: 0) {{
            totalCount
          }}
          following(first: 0) {{
            totalCount
          }}
        }}
      }}
    }}
  }}
}}
"""

star_list = []
hasNextPage = True
endCursor = "" # Start from begining
count = 0
with open('stargazers.csv', 'w') as stars:
    stars_writer = csv.writer(stars)
    stars_writer.writerow(fields)
    while hasNextPage:
        this_query = query.format(owner,repo,endCursor)
        result = run_query(this_query) # Execute the query
        #print(this_query)
        #print(result)
        hasNextPage = result['data']['repository']['stargazers']['pageInfo']['hasNextPage']
        endCursor = result['data']['repository']['stargazers']['pageInfo']['endCursor']
        endCursor = '"' + endCursor + '"'
        data = result['data']['repository']['stargazers']['edges']

        for item in data:
            username = item['node']['login']
            name = item['node']['name']
            num_followers = item['node']['followers']['totalCount']
            num_following = item['node']['following']['totalCount']
            hireable = item['node']['isHireable']
            company = item['node']['company']
            bio = item['node']['bio']
            avatar_url = item['node']['avatarUrl']
            blog = item['node']['websiteUrl']

            created_at = item['node']['createdAt']
            created_at = datetime.datetime.strptime(created_at,'%Y-%m-%dT%H:%M:%SZ')
            created_at = created_at + datetime.timedelta(hours=-5) # EST
            created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')

            star_time = datetime.datetime.strptime(item['starredAt'],'%Y-%m-%dT%H:%M:%SZ')
            star_time = star_time + datetime.timedelta(hours=-5) # CST
            star_time = star_time.strftime('%Y-%m-%d %H:%M:%S')
            star_list.append((username,star_time))
            stars_writer.writerow([username,name,blog,company,bio,avatar_url,hireable,num_followers,num_following,created_at,star_time])

        count = count + 100
        print(count + "users processed.")

