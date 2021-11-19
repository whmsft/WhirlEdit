import os, sys
if len(sys.argv) == 1:
    commit_message = "updates"
else:
    commit_message = " ".join(sys.argv[1:])
os.system('git add . && git commit -m "{}" && git push origin main'.format(commit_message))