import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

projects = [{'name' :'Express', 'key':os.getenv('EXPRESS')},
            {'name' :'bower', 'key':os.getenv('BOWER')},
            {'name' :'less', 'key':os.getenv('LESS')},
            {'name' :'request', 'key':os.getenv('REQUEST')},
            {'name' :'grunt', 'key':os.getenv('GRUNT')},
            {'name' :'jquery', 'key':os.getenv('JQUERY')},
            {'name' :'vuejs', 'key':os.getenv('VUEJS')},
            {'name' :'ramda', 'key':os.getenv('RAMDA')},
            {'name' :'reaflet', 'key':os.getenv('LEAFLET')},
            {'name' :'hexo', 'key':os.getenv('HEXO')},
            {'name' :'webpack', 'key':os.getenv('WEBPACK')},
            {'name' :'webtorrent', 'key':os.getenv('WEBTORRENT')},
            {'name' :'moment', 'key':os.getenv('MOMENT')},
            {'name' :'riot', 'key':os.getenv('RIOT')},
            # {'name' :'react', 'key':os.getenv('REACT')},
            # {'name' :'nodejs', 'key':os.getenv('NODEJS')},
            {'name' :'d3', 'key':os.getenv('D3')},
            {'name' :'lodash', 'key':os.getenv('LODASH')},
            {'name' :'redux', 'key':os.getenv('REDUX')},
            {'name' :'axios', 'key':os.getenv('AXIOS')},
            {'name' :'chartjs', 'key':os.getenv('CHARTJS')}]

# projects = [{'name' :'nodejs', 'key':os.getenv('NODEJS')}]
serverties="MAJOR,CRITICAL"
sonarqube_url ='http://localhost:9000/api/issues/search'


code_smell_types = {}
def get_code_smells():

    for project in projects:
        print(project)
        page = 1
        while True:
            res = requests.get('http://localhost:9000/api/issues/search?'+'severities=' + serverties+ '&components='+ project['name']+'&issueStatuses=CONFIRMED%2COPEN&types=CODE_SMELL&ps=500&p='+str(page),
                            headers={'Authorization' : 'Bearer ' + str(project['key'])})
            page=page+1
            issue_list = res.json()['issues']
            # No more pages
            if(len(issue_list)==0):
                break
            else: 
                for issue in issue_list:
                    if issue['message'] not in code_smell_types:
                        code_smell_types[issue['message']] = 1
                    else:
                        code_smell_types[issue['message']]= code_smell_types[issue['message']]+1
    sorted_smells = dict(sorted(code_smell_types.items(), key=lambda item: item[1], reverse=True)[:20])
    with open("code_smells.json",'w') as f:
        json.dump(sorted_smells,f)
get_code_smells()