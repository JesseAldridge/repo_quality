import subprocess, time

debug = 0
while True:
  subprocess.Popen(['python', '_3_update_cache_loop.py', str(debug)])

  if debug:
    time.sleep(1)
  else:
    time.sleep(60 * 60 * 24)
