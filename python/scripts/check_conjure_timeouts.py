import os

# Script used to parse conjure output and display the examples it timed out for.
files = os.listdir("./conjure-output/")
for name in files:
    if name.endswith("info"):
        file = open("./conjure-output/" + name, "r+")
        lines = file.readlines()
        timeout = int(lines[7].split(":")[1])
        if timeout != 0:
            print(name + " timed out")