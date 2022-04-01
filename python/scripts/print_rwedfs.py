import json
from operator import itemgetter
from data.group_tables_to_ten import group_tables
from setfamily import *

# The main script for producing the RWEDF table in Appendix A of the report.
∑
# Generated using gap: cyclic_product_reps.g
cyclicProductReps = {
    (4, 2): [ [ 0, 0 ], [ 1, 0 ], [ 0, 1 ], [ 1, 1 ] ],
    (8, 2): [ [ 0, 0 ], [ 3, 1 ], [ 2, 0 ], [ 1, 1 ], [ 3, 0 ], [ 1, 0 ], [ 0, 1 ], [ 2, 1 ] ],
    (8, 5): [ [ 0, 0, 0 ], [ 1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, 1 ], [ 1, 1, 0 ], [ 1, 0, 1 ], [ 0, 1, 1 ], [ 1, 1, 1 ] ],
    (9, 2): [ [ 0, 0 ], [ 1, 0 ], [ 2, 0 ], [ 0, 1 ], [ 0, 2 ], [ 1, 1 ], [ 2, 2 ], [ 2, 1 ], [ 1, 2 ] ]
}

def small_group_latex(n, i):
    tolatex = [
        ["", "\\emptyset"],
        ["", "\\{e\\}"],
        ["", "\\mathbb"],
        ["", "\\mathbb Z_3"],
        ["", "\\mathbb Z_4", "\\mathbb Z_2 \\times \\mathbb Z_2"],
        ["", "\\mathbb Z_5"],
        ["", "S_3", "\\mathbb Z_6"],
        ["", "\\mathbb Z_7"],
        ["", "\\mathbb Z_8", "\\mathbb Z_4 \\times \\mathbb Z_2", "D_8", "Q_8", "\\mathbb Z_2^3"],
        ["", "\\mathbb Z_9", "\\mathbb Z_3 \\times \mathbb Z_3"],
        ["", "D_{10}", "\\mathbb Z_{10}"]
    ]
    return tolatex[n][i]
           
def repToStr(rep):
    return str(tuple(rep))

def sub_1(arr2d):
    return [[x - 1 for x in s] for s in arr2d]

def get_obj(n, i, sets):
    group_table = sub_1(group_tables[n-3][n_id-1])

    if n == 4 and i == 2 or \
        n == 8 and i == 2 or \
        n == 8 and i == 5 or \
        n == 9 and i == 2:
            elstr = [repToStr(t) for t in cyclicProductReps[(n, i)]]
            rwedf = SetFamily(sets, group_table, elstr=elstr)
    elif n==6 and i == 1:
        elstr = [ "()", "(1,2)(3,6)(4,5)", "(1,3,5)(2,4,6)", "(1,4)(2,3)(5,6)", "(1,5,3)(2,6,4)", 
  "(1,6)(2,5)(3,4)" ]
        rwedf = SetFamily(sets, group_table, elstr=elstr)
    elif n == 8 and i == 4:
        elstr = ["1", "j", "-1", "-j", "i", "-i", "k", "-k"]
        rwedf = SetFamily(sets, group_table, elstr=elstr)
    elif n == 8 and i == 3:
        elstr = [
            "e",
            "\\alpha",
            "\\alpha^2",
            "\\alpha^3",
            "\\beta",
            "\\beta\\alpha",
            "\\beta\\alpha^2",
            "\\beta\\alpha^3",
        ]
        rwedf = SetFamily(sets, group_table, elstr=elstr)
    elif n == 10 and i == 1:
        elstr = [
            "e",
            "\\alpha",
            "\\alpha^2",
            "\\alpha^3",
            "\\alpha^4",
            "\\beta",
            "\\beta\\alpha",
            "\\beta\\alpha^2",
            "\\beta\\alpha^3",
            "\\beta\\alpha^4",
        ]
        rwedf = SetFamily(sets, group_table, elstr=elstr)
    else:
        rwedf = SetFamily(sets, group_table)
    return rwedf


rwedffile = open("allrwedfs.json", "r+")

rwedfjson = json.load(rwedffile)

rwedfjson = sorted(rwedfjson, key=itemgetter("group", "numsets", "setsize"))
print(R"\begin{table}")
print(R"\caption{RWEDF search results}")
print(R"$$")
print(R"\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}")
print(R"\hline")
print(R"\textbf{Group} & \textbf{RWEDF} & n & m & k_1 \dots k_m & \lambda & \textbf{Bmdl?} & \textbf{GSEDF?} & \textbf{PEDF?} \\ \hline")
for i, item in enumerate(rwedfjson):
    n = item["group"][0]
    n_id = item["group"][1]
    raw_sets = item["rwedf"]
    # print("SmallGroup " + str(n) + ", " + str(n_id))
   
    sets = sub_1([[x for x in s if x != 0] for s in raw_sets])
    
    rwedf = get_obj(n, n_id, sets)

    ks = ",".join([str(k) for k in item["setsize"]])
    l = rwedf.get_rweighted_sum(1)
    if l.denominator == 1:
        l = l.numerator
    else:
        l = "{" + str(l.numerator) + "\\over" + str(l.denominator) + "}"
    # print("$({0};{1};{2};{3})$-RWEDF:".format(rwedf.n, rwedf.m, ks, l))
    # print("$$\n" + rwedf.latex_str() + "\n$$")
    # print("bimodal? " + str(rwedf.is_bimodal()))
    # print("gsedf? " + str(rwedf.is_gsedf()))
    group = small_group_latex(n, n_id)
    sets_str_lst = [s + "," for s in rwedf.sets_str().split(",")]
    sets_str_lst[-1] = sets_str_lst[-1][:-1]
    sets_str_chunks = []
    chunk = ""
    for s in sets_str_lst:
        
        if len(chunk) < 50:
            chunk = chunk + s
        else:
            sets_str_chunks.append(chunk)
            chunk = s
    sets_str_chunks.append(chunk)
    

    print("{0} & {1} & {2} & {3} & {4} & {5}& {6} & {7} & {8}\\\\"
            .format(
                group, 
                sets_str_chunks[0],
                n,
                rwedf.m,
                ks,
                str(l).replace(R"\over", "/"),
                R"\checkmark" if rwedf.is_bimodal() else "",
                R"\checkmark" if rwedf.is_gsedf() else "",
                R"\checkmark" if rwedf.is_pedf() else "",
                ))
                
    for i in range (1, len(sets_str_chunks)):
        print("& " + sets_str_chunks[i] + "&&&&&&& \\\\")
    print(R"\hline")

    if i % 44 == 43:
        print(R"\end{array}")
        print(R"$$")
        print(R"\end{table}")
        print(R"\begin{table}")
        print(R"\caption{RWEDF search results (continued)}")
        print(R"$$")
        print(R"\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}")
        print(R"\hline")
        print(R"\textbf{Group} & \textbf{RWEDF} & n & m & k_1 \dots k_m & \lambda & \textbf{Bmdl?} & \textbf{GSEDF?} & \textbf{PEDF?} \\ \hline")

print(R"\end{array}")
print(R"$$")
print(R"\end{table}")
    