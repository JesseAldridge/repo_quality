import re

import github_quality


def classify(paths):
  non_software_matches = []
  software_matches = []
  for path in paths:
    repo_info = github_quality.pull_repo(path, None)
    description, has_issues = repo_info['description'], repo_info['has_issues']
    non_ascii = False
    if description:
      ascii_count = 0
      for ch in description:
        if ord(ch) < 128:
          ascii_count += 1
      if ascii_count < len(description) * .95:
        non_ascii = True
    if(not has_issues or (description and re.search(r'\blist\b', description)) or non_ascii):
      non_software_matches.append(path)
    else:
      software_matches.append(path)
  return software_matches, non_software_matches

if __name__ == '__main__':

  non_software = [
    'tiimgreen/github-cheat-sheet',
    'MaximAbramchuck/awesome-interviews',
    'faif/python-patterns',
    'moklick/frontend-stuff',
    'kilimchoi/engineering-blogs',
    'ipader/SwiftGuide',
    'sindresorhus/awesome',
    'numbbbbb/the-swift-programming-language-in-chinese',
    'JacksonTian/fks',
    'davidsonfellipe/awesome-wpo'
  ]

  software = [
    'lodash/lodash',
    'jlmakes/scrollreveal.js',
    'carhartl/jquery-cookie',
    'qrohlf/trianglify',
    'tobiasahlin/SpinKit',
    'Alamofire/Alamofire',
    'jwagner/smartcrop.js',
    'sahat/hackathon-starter',
    'roots/sage',
    'SnapKit/Masonry'
  ]

  def print_repos(repos):
    for path in repos:
      repo = github_quality.pull_repo(path, None)
      print ' ', path, repo['size'], repo['description'].encode('utf8')

  software_matches, non_software_matches = classify(software + non_software)

  missed_software = set(software) - set(software_matches)
  print 'missed software:'
  print_repos(missed_software)

  missed_non_software = set(non_software) - set(non_software_matches)
  print 'missed non:'
  print_repos(missed_non_software)
