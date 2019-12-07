import json, os

import _0_hit_api

if os.path.exists('test_pulls.json'):
  os.remove('test_pulls.json')

for page in range(1, 20):
  print 'page:', page
  page_str = _0_hit_api.hit_api(
    'angular/angular', 
    None, 
    '/pulls?page={}'.format(page), 
    priority_request=True
  )
  page_list = json.loads(page_str)
  if not page_list:
    break
  json_str = json.dumps(page_list, indent=2)
  with open('test_pulls.json', 'a') as f:
    f.write(json_str + ',\n')
