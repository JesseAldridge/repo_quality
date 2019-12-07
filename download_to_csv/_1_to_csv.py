import json, csv, glob, os

download_dir_path = os.path.expanduser('~/repoq-downloads')

column_labels = [
  'full_name',
  'disabled', 
  'has_projects', 
  'stargazers_count', 
  'subscribers_count', 
  'self_issue_count',
  'pushed_at',
  'pull_count',
  'network_count',
  'forks',
  'watchers',
  'open_issues',
  'has_wiki',
  'size',
  'archived',
  'fork',
  'has_downloads',
  'issue_count',
  'language',
  'created_at',
  'mirror_url',
  'has_pages',
  'updated_at',
  'id',
  'description',
]

rows = []
for json_path in glob.glob(os.path.join(download_dir_path, '*.txt')):
  with open(json_path) as f:
    json_text = f.read()
  repo_dict = json.loads(json_text)
  rows.append([repo_dict.get(field) for field in column_labels])

with open('out.csv', 'w') as f:
  writer = csv.writer(f, lineterminator='\n')
  writer.writerow(column_labels)
  for row in rows:
    writer.writerow(row)
