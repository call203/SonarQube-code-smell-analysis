
import re
import git
from git import GitCommandError
import argparse
import json
from datetime import datetime


def is_fix_contained(commit_message):
    if not isinstance(commit_message, str):
        return False
    match = re.search("fix", commit_message);
    return bool(match)

def  get_fix_commits():
    commits = repo.iter_commits();
    fixed_commits = []

    bug_id_regex = r'(#\d+|gh-\d+)' 
    fix_keywords = ['fix', 'fixed', 'fixes']  


    for commit in commits:
        commit_message = commit.message.lower()
        if re.search(bug_id_regex, commit_message) and any(keyword in commit_message for keyword in fix_keywords):
            fixed_commits.append(commit)

    return fixed_commits




def search_candidate_commit_szz(bug_fix_commit):
    all_candidate_commits = []

    if bug_fix_commit.parents is not None:
        parent_commit = bug_fix_commit.parents[0]
        diff = repo.git.diff(bug_fix_commit.hexsha, parent_commit.hexsha, '-U0', '--histogram')
        
        changes_dict = generate_changes_dict(diff)
        print(changes_dict)
        all_candidate_commits = get_recent_candidate_commits(parent_commit, changes_dict)
    return all_candidate_commits




def get_recent_candidate_commits(parent_commit, changes_dict):

    recent_commit = None
    for file_path, line_numbers in changes_dict.items():
        try:
            blame_result = repo.git.blame(parent_commit.hexsha, file_path, "--line-porcelain")
        except GitCommandError: 
            continue

        candidate_commits = get_candidate_commits(blame_result, file_path, changes_dict)
        for commit in candidate_commits:
            if recent_commit is None or commit_is_more_recent(commit[0],recent_commit[0]):
                recent_commit = commit + (file_path,)
        
    return recent_commit  




def get_candidate_commits(blame_result, file_path, changes_dict):
    pattern = re.compile(r'([a-f0-9]+)\s+(\d+)\s+(\d+)?(?:\s+(\d+))?\nauthor\s+([^\n]+)')

    commit_set = set()
    most_recent_commit = None
    matches = pattern.findall(blame_result)

    for match in matches:
        commit_hash, first_number, second_number, third_number, author = match
        if int(second_number) in changes_dict.get(file_path, []):
            commit_obj = repo.commit(commit_hash)
            commit_date = commit_obj.committed_datetime

            if args.recent:  
                if most_recent_commit is None or commit_is_more_recent(commit_date, most_recent_commit[2]):
                    most_recent_commit = (commit_hash, author,commit_date)
            else:
                
                commit_set.add((commit_hash, author,commit_date))

    if args.recent and most_recent_commit is not None:
        commit_set = {most_recent_commit}
    return commit_set



def commit_is_more_recent(commit1_datetime, commit2_datetime):
    return commit1_datetime > commit2_datetime



def generate_changes_dict(diff):
        file_path_pattern = re.compile(r'^\+\+\+ b/(.*)$')
        line_number_pattern = re.compile(r'^@@ -(\d+)(,(\d+))? \+(\d+)(,(\d+))? @@')

        #mapping file paths to lists of line numbers
        result_dict = {}
        #Track of the current file path being processed in the diff
        current_file_path = None
        numbers_list= [] 


        diff_lines = diff.split("\n")
        for line in diff_lines:
            
            file_path_match = file_path_pattern.match(line)
            line_number_match = line_number_pattern.match(line)
            #check if the line matches `++b/<file_path>`
            if file_path_match:
                if current_file_path and numbers_list:
                    result_dict[current_file_path] = numbers_list
                    numbers_list = []

                current_file_path = file_path_match.group(1) 

            #checks if the line matches `@@ -<start_line>[,<num_lines>] +<start_line>[,<num_lines>] @@`   
            elif line_number_match:
                start_line = int(line_number_match.group(1))
                num_lines = 1 if line_number_match.group(3) is None else int(line_number_match.group(3))

                if not match_comment(line):
                    numbers_list.extend(range(start_line, start_line + num_lines))

        if current_file_path and numbers_list:
            result_dict[current_file_path] = numbers_list    

        return result_dict             


def match_comment(line):
    comment_pattern = re.compile(r'^\s*(\'\'\'|"""|#|//|<!--|/\*)|(?:.*?--!>|.*?\*/|\'\'\'|""")\s*$')

    return comment_pattern.match(line[1:])  # Ignora il primo carattere perchè le linee iniziano per '-'




def ssz():
    total_candidate_commit = []
    #Get all fixed commits
    fixed_commits = get_fix_commits()
    print(len(fixed_commits))
    for commit in fixed_commits:
        data  = search_candidate_commit_szz(commit)
        if data:
            form = {}
            dt1 = datetime.fromisoformat(str(commit.committed_datetime))
            dt2 = data[2]
            hours_diff = (dt1- dt2).total_seconds()/3600
        
            if not any(item['path']==data[3] for item in total_candidate_commit):
                form['path'] = data[3]
                form['time'] = round(hours_diff)
                total_candidate_commit.append(form)
            else:
                match_item = next((item for item in total_candidate_commit if item['path'] == data[3]), None) 
                if int(match_item['time']) <int(hours_diff):
                    match_item['time'] = round(hours_diff)

    project_name = repo.remotes.origin.url.split('/')[-1].replace('.git', '')
    with open( "./szz/"+project_name+ "_SZZ_data.json",'w') as f:
        json.dump(total_candidate_commit,f)
                 
        
    
        
    
    
repo = None
args = None
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Insert repository name""")
    parser.add_argument('--repo-path', type=str, help="The absolute path to a local copy of the git repository from "
                                                      "where the git log is taken.")
    parser.add_argument('-r', '--recent', action='store_true',
                        help="Show only the most recent commit for each bug-fix commit")
    args = parser.parse_args()
    path_to_repo = args.repo_path
    repo = git.Repo(path_to_repo)
    
    ssz()


## express