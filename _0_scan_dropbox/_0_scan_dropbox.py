import os, subprocess, csv

rows = [('name', 'lines_of_code')]
root_dir = os.path.expanduser('~/Dropbox')
filenames = os.listdir(root_dir)
for i, filename in enumerate(filenames):
  print '{}/{} filename: {}'.format(i, len(filenames), filename)
  path = os.path.join(root_dir, filename)
  if not os.path.isdir(path):
    continue
  cmd_arr = ['tokei', path]
  proc = subprocess.Popen(cmd_arr, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  out_str = proc.communicate()[0]
  out_lines = out_str.splitlines()
  lines_of_code = int(out_lines[-2].split()[3])
  print 'lines_of_code:', lines_of_code
  rows.append((filename, lines_of_code))

with open(os.path.expanduser('~/scan_dropbox.csv'), 'w') as f:
  writer = csv.writer(f, lineterminator='\n')
  writer.writerow(rows[0])
  for i in range(1, len(rows)):
    writer.writerow(rows[i])
