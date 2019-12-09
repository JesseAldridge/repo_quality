import json

import _0_hit_api

json_str = _0_hit_api.hit_api(
  'angular/angular',
  None,
  priority_request=True
)

print json.dumps(json.loads(json_str), indent=2)
