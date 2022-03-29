from os import listdir
from os.path import exists

def aftercolon(line):
    return line.split(":")[1]


print(R"\begin{tabular}{|c|c|c|c|}")
allfiles = listdir("./conjure-output")
files = [f for f in allfiles if f.startswith("model-osedf") and f.endswith(".eprime-info")]
print(len(files))
for f in sorted(files):
    file = open("./conjure-output/" + f, "r+")
    lines = file.readlines()
    if aftercolon(lines[7])[:-1] != "0":
        continue

    print(R"\hline")
    attr = f.split("_")
    
    
    print(R"\texttt{SmallGroup(" + attr[1] + "," + attr[2] + ")}", end="")
    print("& $({0}, {1}, {2}, {3})$".format(attr[1], attr[5], attr[6], attr[7].split(".")[0]), end="")
    print(R"&" + aftercolon(lines[0][:-1]), end="")
    print(R"&" + aftercolon(lines[8][:-1]), end="")

    directsedfpath = "model-sedf_{0}_{1}_{2}_{3}".format(attr[1], attr[2], attr[5], attr[6])
    for f2 in allfiles:
        if f2.startswith(directsedfpath) and f2.endswith(".eprime-info"):
            file2 = open("conjure-output/" + f2, "r+")
            file2lines = file2.readlines() 
            print("&" + aftercolon(file2lines[0]), end="")
    print(R"\\")
print(R"\end{tabular}")