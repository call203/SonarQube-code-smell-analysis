import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

projects = [
        {'name' :'Express', 'key':os.getenv('EXPRESS')},
        {'name' :'chartjs', 'key':os.getenv('CHARTJS')},
        {'name' :'bower', 'key':os.getenv('BOWER')},
        {'name' :'less', 'key':os.getenv('LESS')},
        {'name' :'request', 'key':os.getenv('REQUEST')},
        {'name' :'grunt', 'key':os.getenv('GRUNT')},
        {'name' :'jquery', 'key':os.getenv('JQUERY')},
        {'name' :'vuejs', 'key':os.getenv('VUEJS')},
        {'name' :'ramda', 'key':os.getenv('RAMDA')},
        {'name' :'leaflet', 'key':os.getenv('LEAFLET')},
        {'name' :'hexo', 'key':os.getenv('HEXO')},
        {'name' :'webpack', 'key':os.getenv('WEBPACK')},
        {'name' :'webtorrent', 'key':os.getenv('WEBTORRENT')},
        {'name' :'moment', 'key':os.getenv('MOMENT')},
        {'name' :'riot', 'key':os.getenv('RIOT')},
        {'name' :'react', 'key':os.getenv('REACT')},
        {'name' :'nodejs', 'key':os.getenv('NODEJS')},
        {'name' :'d3', 'key':os.getenv('D3')},
        {'name' :'lodash', 'key':os.getenv('LODASH')},
        {'name' :'redux', 'key':os.getenv('REDUX')},
        {'name' :'axios', 'key':os.getenv('AXIOS')},
 
 ]

serverties="MAJOR,CRITICAL,BLOCKER"
sonarqube_url ='http://localhost:9000/api/issues/search'

##
# Get SonarQube data
##
def request_sonarQube(name, key):
    code_smell_list = []
    page =1
    while True:
        res = requests.get('http://localhost:9000/api/issues/search?'+ '&components='+ name +"&severities=" +serverties +'&issueStatuses=CONFIRMED%2COPEN&types=CODE_SMELL&ps=500&p='+str(page),
                            headers={'Authorization' : 'Bearer ' + str(key)})
        
        page+=1
        try:
            issue_list = res.json()['issues']
        except KeyError:
             break

        if(len(issue_list)==0):
            break
        else: 
            for issue in issue_list:
                code_smell_list.append(issue)
 
    return code_smell_list


##
# Find all types of smells in each file for a project
##

def get_each_project_smells(name, key):
    project_code_smells = [];
    issues = request_sonarQube(name,key)
    for issue in issues:
        path = issue['component'].replace(name+":",'',1)
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
    with open( name+ "_project_code_smells.json",'w') as f:
        json.dump(project_code_smells,f)
    


##
# Calcuate the top smells across all projects
##
code_smell_types = {}
severity = {'block':[], 'critical':[], 'major':[],'minor':[],'info':[]}
def total_code_smells():

    for project in projects:
        print(project)

        res = request_sonarQube(project['name'],project['key'])
        for issue in res:
            if issue['rule'] not in code_smell_types:
                code_smell_types[issue['rule']] = 1
            else:
                code_smell_types[issue['rule']]= code_smell_types[issue['rule']]+1

    sorted_smells = dict(sorted(code_smell_types.items(), key=lambda item: item[1], reverse=True))
    print(len(sorted_smells))

    with open("top_20_code_smells.json",'w') as f:
        json.dump(sorted_smells,f)



total_code_smells()
# for i in projects:
#     get_each_project_smells(i['name'],i['key'])




