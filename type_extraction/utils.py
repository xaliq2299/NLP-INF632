"""
Don't modify this code.
"""

import sys


class Page:
    """
    This class is used to store title and content of a wiki page
    """
    __author__ = "Jonathan Lajus"

    def __init__(self, title, content):
        self.content = content
        self.title = title
        if sys.version_info[0] < 3:
            self.title = title.decode("utf-8")
            self.content = content.decode("utf-8")

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.title == other.title and self.content == other.content

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.title, self.content))

    def __str__(self):
        return 'Wikipedia page: "' + (self.title.encode("utf-8") if sys.version_info[0] < 3 else self.title) + '"'

    def __repr__(self):
        return self.__str__()

    def _to_tuple(self):
        return self.title, self.content


class Parsy:
    """
    Parse a Wikipedia file, return page objects
    """
    __author__ = "Jonathan Lajus"

    def __init__(self, wikipediaFile):
        self.file = wikipediaFile

    def __iter__(self):
        title, content = None, ""
        with open(self.file, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line and title is not None:
                    yield Page(title, content.rstrip())
                    title, content = None, ""
                elif title is None:
                    title = line
                elif title is not None:
                    content += line + " "


def eval_f1(gold_file, pred_file):

    # Dictionaries
    goldstandard = dict()
    student = dict()

    # Reading first file
    with open(gold_file, 'r', encoding="utf-8") as f:
        for line in f:
            temp = line.split("\t")
            if len(temp) != 2:
                print("The line:", line, "has an incorrect number of tabs")
            else:
                if temp[0] in goldstandard:
                    print(temp[0], " has two solutions")
                goldstandard[temp[0]] = str.lower(temp[1])

    # Reading second file
    with open(pred_file, 'r', encoding="utf-8") as f:
        for line in f:
            temp = line.split("\t")
            if len(temp) != 2:
                if not debug:
                    print("Comment :=>> The line: '", line, "' has an incorrect number of tabs")
                else:
                    print("The line: '", line, "' has an incorrect number of tabs")
            else:
                if temp[0] in student:
                    if not debug:
                        print("Comment :=>>", temp[0], "has two solutions")
                    else:
                        print(temp[0], " has two solutions")
                student[temp[0]] = str.lower(temp[1])

    true_pos = 0
    false_pos = 0
    false_neg = 0

    for key in student:
        if key in goldstandard:
            if student[key] == goldstandard[key]:
                true_pos += 1
            else:
                false_pos += 1
                print("You got", key, "wrong. Expected output: ", goldstandard[key], ",given:", student[key])

    for key in goldstandard:
        if key not in student:
            false_neg += 1
            print("No solution was given for", key)

    if true_pos + false_pos != 0:
        precision = float(true_pos) / (true_pos + false_pos) * 100.0
    else:
        precision = 0.0

    if true_pos + false_neg != 0:
        recall = float(true_pos) / (true_pos + false_neg + false_pos) * 100.0
    else:
        recall = 0.0

    beta = 0.5

    if precision + recall != 0.0:
        f05 = (1 + beta * beta) * precision * recall / (beta * beta * precision + recall)
    else:
        f05 = 0.0

    # grade = 0.75 * precision + 0.25 * recall
    grade = f05

    print("Comment :=>>", "Precision:", precision)
    print("Comment :=>>", "Recall:", recall)
    print("Simulated Grade (F0.5) :=>>", grade)
