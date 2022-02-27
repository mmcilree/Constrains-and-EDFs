from utils import all_equal
from fractions import Fraction
import itertools
from collections import defaultdict


class SetFamily:
    def __init__(self, sets, group_table, inverses=None, elstr=None):
        self.n = len(group_table)
        self.sets = sets
        self.m = len(sets)
        self.group_table = group_table
        self.inverses = inverses or self.get_inverses()
        self.elstr = elstr

    def sets_str(self):
        """Return the sets in the family in latex format."""
        latex_str = ""
        for j, s in enumerate(self.sets):
            latex_str += "\{"
            for i, x in enumerate(s):
                latex_str += self.el_as_str(x)
                if i != (len(s) - 1):
                    latex_str += ", "
            latex_str += "\}" + ("" if j == self.m - 1 else ", ")
        return latex_str

    def op_as_str(self):
        """
            Return the difference operation of the group (multiply by inverse 
            by default) as a string.
        """
        return R"\times (\;\cdot\;)^{-1}"

    def get_inverses(self):
        """Create a table of inverses for each element"""
        return [self.group_table[i].index(0) for i in range(self.n)]

    def mult(self, x, y):
        """Find the product of two elements, according to the group table."""
        return self.group_table[x][y]

    def inv(self, x):
        """Find the inverse of an element, according to the group table."""
        return self.inverses[x]

    def diff(self, x, y):
        """
        Get the difference (xy^-1) between two elements, according to the
        group multiplication.
        """
        return self.group_table[x][self.inv(y)]

    def has_disjoint_sets(self):
        """Check if all the sets are disjoint (empty intersection)"""
        return len(list(set([x for s in self.sets for x in s]))) == sum(
            [len(s) for s in self.sets]
        )

    def external_differences(self, i, j):
        """Get all the external diferences between the ith and jth sets."""
        ed_dict = {}
        for el1 in self.sets[i]:
            for el2 in self.sets[j]:
                ed_dict[tuple([el1, el2])] = self.diff(el1, el2)
        return ed_dict

    def is_edf(self):
        """Check if this set family is an External Difference Family"""
        return self.has_equal_set_size() and self.has_disjoint_sets() and self.is_oedf()

    def is_sedf(self):
        """Check if this set family is a Strong External Difference Family"""
        return (
            self.has_equal_set_size() and self.has_disjoint_sets() and self.is_osedf()
        )

    def has_equal_set_size(self):
        """Check if all the sets are the same size"""
        return all_equal([len(s) for s in self.sets])

    def is_rwedf(self):
        """Check if this set family is a Reciprocally Weighted External Difference Family"""
        sums = [self.get_rweighted_sum(i) for i in range(1, self.n)]
        return all_equal(sums)

    def is_gsedf(self):
        """Check if this set family is a Generalised Strong External Difference Family"""
        for i in range(self.m):
            if not all_equal(self.get_counts_from_set(i)):
                return False
        return True

    def is_pedf(self):
        """Check if this set family is a Partitioned External Difference Family"""
        sets_with_length = defaultdict(list)
        for i, s in enumerate(self.sets):
            sets_with_length[len(s)].append(i)
        for k in sets_with_length.keys():
            count_sums = [0 for _ in range(1, self.n)]
            for i in sets_with_length[k]:
                counts = self.get_counts_from_set(i)
                count_sums = [count_sums[i] + counts[i] for i in range(0, self.n - 1)]
            if not all_equal(count_sums):
                return False
        return True

    def is_oedf(self):
        """
        An OEDF is an External Difference family without the sets being
        necessarily disjoint or equal length
        """
        all_ext_diffs = {}
        for i in range(self.m):
            for j in range(self.m):
                if i != j:
                    all_ext_diffs.update(self.external_differences(i, j))

        counts = [
            sum([v == val for v in all_ext_diffs.values()]) for val in range(1, self.n)
        ]
        print(counts)
        return all_equal(counts)

    def is_osedf(self):
        """
        Likewise an OSEDF is a Strong External Difference family without the
        sets being necessarily disjoint or equal length
        """
        all_counts = []
        for i in range(self.m):
            count_sums = [0 for _ in range(1, self.n)]
            for j in range(self.m):
                if i != j:
                    ext_diffs = self.external_differences(i, j)

                    counts = [
                        sum([v == val for v in ext_diffs.values()])
                        for val in range(1, self.n)
                    ]

                    count_sums = [
                        count_sums[i] + counts[i] for i in range(0, self.n - 1)
                    ]
            print(count_sums)
            all_counts.append(count_sums)

        return all_equal(all_counts)

    def is_bimodal(self):
        """
            Check if if the number if times an element occurs as a difference
            from any set is either 0 or the size of the set.
        """
        for i in range(self.m):
            count_sums = self.get_counts_from_set(i)
            for el in range(1, self.n):
                if count_sums[el - 1] != 0 and count_sums[el - 1] != len(self.sets[i]):
                    return False
        return True

    def el_as_str(self, el):
        """String representation of element: may be overridden in subclasses."""
        return self.elstr[el] if self.elstr else str(el)

    def get_external_differences_str(
        self, sort_by=None, headings=None, latex=True, perline=5
    ):
        """Get all the external differences as a long string of equations."""
        ed_str = ""
        ed = {}
        for i in range(self.m):
            for j in range(self.m):
                if i != j:
                    ed.update(self.external_differences(i, j))

        if sort_by == "value":
            ed = dict(sorted(ed.items(), key=lambda item: item[1]))

        count = 0
        for diff in ed.keys():

            edstr += ("& " if latex else " ") + self.el_as_str(
                diff[0]
            ) + " - " + self.el_as_str(diff[1]) + " = " + self.el_as_str(ed[diff]), +" "

            count += 1
            if count % perline == 0:
                edstr += "\\\\" if latex else ""
        edstr += "\n"

    def get_external_differences_tables_str(self, combine=False):
        """Get all the external difference as latex-formatted tables."""
        tables_str = ""
        for i in range(self.m):
            if combine:
                tables_str += "\\begin{array}{ c|" + "c" * len(self.sets[i]) + " }\n"

                for el in self.sets[i]:
                    tables_str += " & " + self.el_as_str(el)

                tables_str += R"\\" + "\n"
                tables_str += self.op_as_str() + R" & \\" + "\n"

            for j in range(self.m):
                if i != j:
                    ed = self.external_differences(i, j)
                    if not combine:
                        tables_str += (
                            "\\begin{array}{ c|" + "c" * len(self.sets[i]) + " }\n"
                        )

                        for el in self.sets[i]:
                            tables_str += " & " + self.el_as_str(el)

                        tables_str += R"\\" + "\n"
                        tables_str += self.op_as_str() + R" & \\" + "\n"
                    tables_str += R"\hline" + "\n"

                    for el2 in self.sets[j]:
                        tables_str += self.el_as_str(el2)
                        for el1 in self.sets[i]:
                            tables_str += " & " + self.el_as_str(ed[(el1, el2)])
                        tables_str += R"\\" + "\n"
                    if not combine:
                        tables_str += R"\end{array}" + "\n\n"
            if combine:
                tables_str += R"\end{array}" + "\n\n"
        return tables_str

    def get_counts_from_set_str(self, i):
        """
            Count the number of times each non-zero elements occurs as an external
            difference starting from the ith set.
        """
        count_sums = [0 for _ in range(1, self.n)]
        for j in range(self.m):
            if i != j:
                ext_diffs = self.external_differences(i, j)

                counts = [
                    sum([v == val for v in ext_diffs.values()])
                    for val in range(1, self.n)
                ]

                count_sums = [count_sums[i] + counts[i] for i in range(0, self.n - 1)]

        return count_sums

    def get_Ns_str(self, i):
        """Return all the counts from the ith set in the form `N_i(el) = count`"""
        count_sums = self.get_counts_from_set(i)
        ns_str = ""
        for el in range(1, self.n - 1):
            ns_str += "N_{0}({1}) = {2}; ".format(
                i + 1, self.el_as_str(el), count_sums[el - 1]
            )
        return ns_str

    def get_rweighted_sum(self, el):
        """
            Return the reciprocally weighted sum (as a fraction) of counts across 
            all sets for a particular element.
        """
        setcounts = [self.get_counts_from_set(i) for i in range(self.m)]
        return sum(
            [
                Fraction(1, len(self.sets[i])) * setcounts[i][el - 1]
                for i in range(self.m)
            ]
        )

    def get_rweighted_sums_str(self):
        """
            Return all the reciprocally weighted sums as latex formatted equations.
        """
        ws_str = ""
        setcounts = [self.get_counts_from_set(i) for i in range(self.m)]
        for el in range(1, self.n):
            for i in range(self.m):
                ws_str += (
                    "{ 1 \over "
                    + str(len(self.sets[i]))
                    + "}"
                    + " N_{0}({1})".format(i + 1, self.el_as_str(el))
                )
                if i != self.m - 1:
                    ws_str += " + "
            ws_str += " &= "
            for i in range(self.m):

                summand = Fraction(1, len(self.sets[i])) * setcounts[i][el - 1]
                ws_str += (
                    "{ "
                    + str(summand.numerator)
                    + "\over "
                    + str(summand.denominator)
                    + "}"
                )
                if i != self.m - 1:
                    ws_str += " + "

            res = self.get_rweighted_sum(el)

            if res.denominator != 1:
                ws_str += (
                    " &= {"
                    + str(res.numerator)
                    + " \over "
                    + str(res.denominator)
                    + "}\\\\"
                )
            else:
                ws_str += " &= " + str(res.numerator) + "\\\\"

            ws_str += "\n\n"
        return ws_str


class CyclicSetFamily(SetFamily):
    """Represent a family of sets with elements from the cyclic group Z_n"""

    def __init__(self, sets, mod):
        group_table = [[(i + j) % mod for i in range(mod)] for j in range(mod)]
        inverses = [(-i) % mod for i in range(mod)]
        super(CyclicSetFamily, self).__init__(sets, group_table, inverses=inverses)

    def op_as_str(self):
        return "-"


class CyclicProductSetFamily(SetFamily):
    """
    Represent a family of sets with elements from a direct product of cyclic
    groups Z_a1 x Z_a2 x ... Z_ak
    """

    def __init__(self, sets, mod):
        """Expect sets of tuples for initialisation."""
        if type(mod) is not list:
            # If a single integer is given as mod, assume all groups in the
            # product have that size.
            mod = [mod for _ in range(len(sets[0][0]))]

        groups = [range(m) for m in mod]
        self.elements = list(itertools.product(*groups))
        elements = self.elements
        sets = [list(map(elements.index, s)) for s in sets]

        group_table = [
            [
                elements.index(
                    tuple(
                        [
                            (elements[i][k] + elements[j][k]) % mod[k]
                            for k in range(len(mod))
                        ]
                    )
                )
                for i in range(len(elements))
            ]
            for j in range(len(elements))
        ]

        inverses = [
            elements.index(tuple([-elements[i][k] % mod[k] for k in range(len(mod))]))
            for i in range(len(elements))
        ]

        super(CyclicProductSetFamily, self).__init__(
            sets, group_table, inverses=inverses
        )

    def op_as_str(self):
        return "-"

    def el_as_str(self, el):
        return str(self.elements[el])


if __name__ == "__main__":
    mod_5_mult = [
        [0, 1, 2, 3, 4],
        [1, 2, 3, 4, 0],
        [2, 3, 4, 0, 1],
        [3, 4, 0, 1, 2],
        [4, 0, 1, 2, 3],
    ]

    test = CyclicSetFamily([[0, 1], [2, 4]], 5)
    print(test.mult(2, 3))
    print(test.diff(4, 1))
    print(test.diff(2, 3))
    print(test.is_edf())  # True
    print(test.is_sedf())  # True
    test.print_external_differences(sort_by="value")

    test2 = CyclicProductSetFamily(
        [
            [(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)],
            [(0, 1), (0, 3), (1, 3), (2, 0), (3, 1)],
            [(0, 2), (1, 0), (1, 1), (3, 0), (3, 3)],
        ],
        4,
    )
    print(test2.is_edf())  # True
    print(test2.is_sedf())  # False
