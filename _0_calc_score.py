import datetime

hardcoded_issue_counts = {
  # https://code.djangoproject.com/query
  'django/django': 1243
}

def calc_score(repo_dict, mean_stars_per_issue):
  repo_dict['score'] = (
    repo_dict['stargazers_count'] * .01 +
    repo_dict['stargazers_count'] / repo_dict['age'].days * 2)

  if mean_stars_per_issue is not None:
    if repo_dict['has_issues']:
      issue_count = repo_dict['open_issues_count'] - repo_dict['pull_count']
    # (can hardcode issue counts for projects which don't use github for issues)
    elif repo_dict['full_name'] in hardcoded_issue_counts:
      issue_count = hardcoded_issue_counts[repo_dict['full_name']]
    else:
      issue_count = repo_dict['stargazers_count'] / mean_stars_per_issue
    repo_dict['issue_count'] = issue_count
    repo_dict['score'] += repo_dict['stargazers_count'] / (issue_count or 1) * 20
    return repo_dict['score']

fake_repo_dict = {
  'full_name': 'fake_user/fake_repo',
  'stargazers_count': 100,
  'has_issues': True,
  'open_issues_count': 10,
  'age': datetime.timedelta(days=100),
  'pull_count': 2,
}

if __name__ == '__main__':
  # Test

  print calc_score(fake_repo_dict, mean_stars_per_issue=30)

  print calc_score({
    'full_name': 'django/django',
    'stargazers_count': 100,
    'has_issues': False,
    'age': datetime.timedelta(days=100)
  }, mean_stars_per_issue=30)
