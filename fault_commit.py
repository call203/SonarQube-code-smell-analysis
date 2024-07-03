import subprocess
from datetime import datetime

def get_fault_introducing_commit(fix_commit_id, changed_files):
    fault_introducing_commit = None
    for file_path in changed_files:
        # Use Git blame to find the commit that last modified each line of the file
        blame_command = f'git blame -p {fix_commit_id} -- {file_path}'
        blame_output = subprocess.check_output(blame_command, shell=True, universal_newlines=True)

        # Parse blame output to find the commit that introduced changes
        lines = blame_output.splitlines()
        for line in lines:
            if line.startswith('author '):  # Skip lines related to blame info
                continue
            if line.startswith('boundary '):  # Stop at boundary line
                break
            if line.startswith('commit '):
                commit_id = line.split(' ')[1]
                commit_date = datetime.strptime(line.split(' ')[2], '%Y-%m-%d').date()
                if commit_date < fix_commit_date.date():
                    fault_introducing_commit = commit_id
                    break
    return fault_introducing_commit

# Example usage
fix_commit_id = 'a1b2c3d4e5f6'  # Replace with actual fix commit ID
fix_commit_date = datetime(2023, 6, 1)  # Replace with actual fix commit date
changed_files = ['src/main.js', 'src/utils.js']  # Replace with actual changed files

fault_introducing_commit = get_fault_introducing_commit(fix_commit_id, changed_files)
if fault_introducing_commit:
    print(f'Fault introducing commit for {fix_commit_id}: {fault_introducing_commit}')
else:
    print(f'Could not find fault introducing commit for {fix_commit_id}')
