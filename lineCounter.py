import sys

from walkdir import filtered_walk, file_paths

path = "./"
if len(sys.argv) > 1:
    path = sys.argv[1]

paths = file_paths(filtered_walk(path))

extensions = [".py", ".java", ".html", ".css", ".js"]

useFullPaths = []
paths = list(paths)
for path in paths:
    for extension in extensions:
        if path.endswith(extension):
            useFullPaths.append(path.replace(".\\", "", 1))

totalFiles = 0
totalChars = 0
totalWords = 0
totalLines = 0

for path in useFullPaths:
    print(path)
    try:
        with open(path, "r") as f:
            data = f.read()
            totalFiles += 1
            totalChars += len(data) + 1
            totalWords += len(data.split())
            totalLines += data.count("\n") + 1
    except Exception as e:
        print(f"File: {path} had an error")

print("\n\n\n")
print(f"Total files: {totalFiles}")
print(f"Total words: {totalWords}")
print(f"Total chars: {totalChars}")
print(f"Total lines: {totalLines}")
