import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()
# 안되는 파일들 -> 나중에 체크!
# {'name' :'react', 'key':os.getenv('REACT')},
# {'name' :'nodejs', 'key':os.getenv('NODEJS')},
projects = [
    {'name' :'Express', 'key':os.getenv('EXPRESS')},
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
            {'name' :'d3', 'key':os.getenv('D3')},
            {'name' :'lodash', 'key':os.getenv('LODASH')},
            {'name' :'redux', 'key':os.getenv('REDUX')},
            {'name' :'axios', 'key':os.getenv('AXIOS')},
            {'name' :'chartjs', 'key':os.getenv('CHARTJS')}
            ]

serverties="MAJOR,CRITICAL"
sonarqube_url ='http://localhost:9000/api/issues/search'

##
# Get SonarQube data
##
code_smell_list = []
def request_sonarQube(name, key):

    page =1
    while True:
        res = requests.get('http://localhost:9000/api/issues/search?'+'severities=' + serverties+ '&components='+ name +'&issueStatuses=CONFIRMED%2COPEN&types=CODE_SMELL&ps=500&p='+str(page),
                            headers={'Authorization' : 'Bearer ' + str(key)})
        page+=1
        issue_list = res.json()['issues']
            # No more pages
        if(len(issue_list)==0):
            break
        else: 
            for issue in issue_list:
                code_smell_list.append(issue)
        
    return code_smell_list


##
# Find all types of smells in each file for a project
##
project_code_smells = [];
def get_each_project_smells():
    issues = request_sonarQube('bower','sqp_b70a9b546111d8de5d3fd08922e1ff6e08142bfd')
    for issue in issues:
        path = issue['component'].replace('bower'+":",'',1)
        if not any(item['path']==path for item in project_code_smells):
            form = {}
            form['path'] = path;
            form['smells'] = [issue['rule']]
            project_code_smells.append(form)
        else:
            match_item = next((item for item in project_code_smells if item['path'] == path), None)
            match_item['smells'].append(issue['rule'])
            match_item['smells'] = list(set(match_item['smells']))

    print(project_code_smells)
    


##
# Calcuate the top smells across all projects
##
code_smell_types = {}
def total_code_smells():

    for project in projects:
        print(project)

        res = request_sonarQube(project['name'],project['key'])
        for issue in res:
            if issue['message'] not in code_smell_types:
                code_smell_types[issue['message']] = 1
            else:
                code_smell_types[issue['message']]= code_smell_types[issue['message']]+1

    sorted_smells = dict(sorted(code_smell_types.items(), key=lambda item: item[1], reverse=True)[:20])
    with open("code_smells.json",'w') as f:
        json.dump(sorted_smells,f)


get_each_project_smells()




