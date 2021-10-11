"""
Don't modify this code.
"""
import sys


class Page:
    '''
    This class is used to store title and content of a wiki page
    '''
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
        return (self.title, self.content)

    # Only used for Disambiguation TP
    def label(self):
        return self.title[1:self.title.rindex("_")].replace("_", " ")


class Parsy:
    '''
    Parses a Wikipedia file, returns page objects
    '''
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
            yield Page(title, content.rstrip())


def clean(entity):
    '''
    clean entity
    :param entity: example "<http://yago-knowledge.org/resource/Lochaber>"
    :return: <Lochaber>
    '''
    if entity[0] == '<':
        entity = entity[1:]
        entity = entity[entity.rfind("/")+1:]
        entity = entity[entity.rfind("#")+1:]
        entity = "<"+entity
    elif entity[0] == '"':
        entity = entity[0:entity.rfind('"')+1]
    return entity


class KnowledgeBase:
    '''
    A simple knowledge base. Don't modify this code.

    Load the knowledge base:
        kb = KnowledgeBase("yago.tsv")

    Access facts:
        albumsOfElvis = kb.facts["<Elvis>"]["<albums>"]

    Access inverse facts:
        entitiesCalledParis = kb.inverseFacts['"Paris"']["<label>"]
    '''
    __author__ = "Fabian Suchanek"

    def __init__(self, yagoFile):
        self.facts = {}
        self.inverseFacts = {}
        with open(yagoFile, encoding="utf-8") as file:
            print("Loading", yagoFile, end="...", flush=True)
            for line in file:
                split_line = line.split('\t')
                if len(split_line)<3:
                    raise RuntimeError("The file is not a valid KB file")
                subject = clean(split_line[0])
                relation = clean(split_line[1])
                obj = clean(split_line[2])
                self.facts.setdefault(subject, {})
                self.facts[subject].setdefault(relation,set())
                self.facts[subject][relation].add(obj)
                self.inverseFacts.setdefault(obj, {})
                self.inverseFacts[obj].setdefault(relation,set())
                self.inverseFacts[obj][relation].add(subject)
        print("done", flush=True)


def evaluate(student_file, goldstandard_file):
    '''
    run this code to evaluate your model on a gold standard dataset.
    :param student_file: a result file generated by you
    :param goldstandard_file: a gold standard dataset
    :return:
    '''
    # Dictionaries
    goldstandard = dict()
    student = dict()

    # Reading first file
    with open(goldstandard_file, 'r', encoding='utf-8') as f:
        for line in f:
            temp = line.strip().split("\t")
            if len(temp) != 2:
                print("The line:", line, "has an incorrect number of tabs")
            else:
                if temp[0] in goldstandard:
                    print(temp[0], " has two solutions")
                goldstandard[temp[0]] = temp[1]

    # Reading second file
    with open(student_file, 'r', encoding='utf-8') as f:
        for line in f:
            temp = line.strip().split("\t")
            if len(temp) != 2:
                print("The line: '", line, "' has an incorrect number of tabs")
            else:
                if temp[0] in student:
                    print(temp[0], " has two solutions")
                student[temp[0]] = temp[1]

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
            if false_neg < 500:
                print("No solution was given for", key)
            elif false_neg == len(goldstandard):
                print("Other solutions not found...")

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

    print("Precision:", precision)
    print("Recall:", recall)
    print("F0.5:", f05)