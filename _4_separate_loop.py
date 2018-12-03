import subprocess, time
from datetime import datetime

debug = 0
while True:
  print 'launching subprocess at {}'.format(datetime.now())
  subprocess.Popen(['python', '_3_update_cache_loop.py', str(debug)]).communicate()
  print 'completed subprocess at {}'.format(datetime.now())

  if debug:
    time.sleep(1)
  else:
    time.sleep(60 * 60 * 24)
