from os import listdir

def aftercolon(line):
    return line.split(":")[1]

print(R"\begin{tabular}{|c|c|c|}")
files = [f for f in listdir("./conjure-output") if f.endswith(".eprime-info")]
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
    print(R"\\")
print(R"\end{tabular}")