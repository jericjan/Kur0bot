import os

os.system("git add .")
os.system(
    "git diff --ignore-space-at-eol -b -w --ignore-blank-lines master > diff.diff"
)
print("done")
