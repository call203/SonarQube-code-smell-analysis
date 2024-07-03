
import re
import json
import git
import argparse


def is_fix_contained(commit_message):
    if not isinstance(commit_message, str):
        return False
    match = re.search("fix", commit_message);
    return bool(match)

def  get_fix_commits():
    commits = repo.iter_commits();
    fixed_commits = []
    for commit in commits:
        commit_message = commit.message.lower()
        match = is_fix_contained(commit_message);
        if match:
           fixed_commits.append(commit);
    
    return fixed_commits

def search_candidate_commit_szz(fixed_commit):
    if fixed_commit is not None:
        parent_commit = fixed_commit.parents[0]
        diff = repo.git.diff(fixed_commit.hexsha, parent_commit.hexsha,'-U0', '--histogram')
        print(diff)

def ssz():
    total_candidate_commit = {}
    #Get all fixed commits
    fixed_commits = get_fix_commits()
    print(len(fixed_commits))
    for commit in fixed_commits:
        # total_candidate_commit[commit] = 
        search_candidate_commit_szz(commit)
        
        
        
    


    
repo = None;
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Insert repository name""")
    parser.add_argument('--repo-path', type=str, help="The absolute path to a local copy of the git repository from "
                                                      "where the git log is taken.")
    args = parser.parse_args()
    path_to_repo = args.repo_path
    repo = git.Repo(path_to_repo)
    
    ssz()
