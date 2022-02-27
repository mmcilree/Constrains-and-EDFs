# A script to read the output of conjure and see which it found no solutions and which it simply timed out
progresstxt = open("./python/scripts/data/searchprogress.txt")

lines = progresstxt.readlines()

current_model = ""
model_finished = False

no_sols = []
timed_out = []
sols = []
allmodels = []
count = 0
for line in lines:
    if line.startswith("Savile Row"):
        count += 1
        allmodels.append(line[38:])
        if not model_finished:
            timed_out.append(current_model)
        current_model = line
        model_finished = False
    
    if line.startswith("No solutions found"):
        model_finished = True
        no_sols.append(current_model)
    elif line.startswith("Copying solution"):
        model_finished = True
        sols.append(current_model)

# print("Found solution ({0}): ".format(len(sols)))
# print("No solutions: ({0}): ".format(len(no_sols)))
# print("Timed out ({0}): ".format(len(timed_out) - 1))
# print("Overall ({0})".format(count))

[print(l, end="") for l in sorted(allmodels)]