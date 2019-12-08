This project uses simple heuristics in an attempt to roughly score the quality of a project on
GitHub.  It currently takes into account the project's number of stars, its age, and the
number of open issues it has.

Other (much more elaborate) projects in the domain of dubious metrics:
  http://db-engines.com/en/ranking
  http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html

MIT License

----

# Deploy:

ssh repo_quality
cd repo_quality
git pull

# Run the polling loop in the background
sudo killall -r python
sudo python _4_separate_loop.py &> loop.txt&

# run gunicorn in the background
sudo killall -r gunicorn
sudo nohup gunicorn -w 4 app:app -b 0.0.0.0:80 --log-file=stderr.log --enable-stdio-inheritance &

# output written to: nohup.out

# debugging info
ps aux | grep python
history
df -h

# repo data written to: ~/.github_quality
