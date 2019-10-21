import collections, glob, json, os, re

raw_repo_lists = []
for path in glob.glob('lists/*.txt'):
  print 'loading path:', path
  with open(path) as f:
    text = f.read()
  lines = text.strip().splitlines()
  lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('//')]
  clean_lines = []
  for line in lines:
    if re.match(r'^[\-_0-9A-Za-z\.]+/[\-_0-9A-Za-z\.]+$', line):
      clean_lines.append(line)
    else:
      print 'bad repo name:', line

  list_name = os.path.basename(path).rsplit('.', 1)[0]
  raw_repo_lists.append((list_name, clean_lines))

repo_lists = collections.OrderedDict()
for name, repo_list in sorted(raw_repo_lists, key=lambda t: t[0]):
  repo_lists[name] = repo_list

if __name__ == '__main__':
  print repo_lists['web_frameworks']
