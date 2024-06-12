import requests

Headers = {'Authorization' : 'Bearer sqp_9898e77366b225bdbbb5a7cd8760a981e1921157'}
serverties="MAJOR,CRITICAL"
project_name = "chartjs"
sonarqube_url ='http://localhost:9000/api/issues/search'


code_smell_types = {}

def get_code_smells():
    page = 1
    while True:
        res = requests.get(sonarqube_url+'?severities='+serverties+'&components=chartjs&types=CODE_SMELL&issueStatuses=CONFIRMED%2COPEN&ps=500&'+'p='+str(page),headers=Headers)
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
            
    print(code_smell_types)

get_code_smells()