"""
=== Purpose ===

The goal of this lab is to disambiguate entities in a text. For example, given a Wikipedia article:

    <Paris_17>
    Paris is a figure in the Greek mythology.

the goal is to determine that <Paris_17> = <Paris_(mythology)>.
Here, <Paris_17> is an artificial title of the Wikipedia article, and <Paris_(mythology)> is the unambiguous entity in the YAGO knowledge base.
(https://yago-knowledge.org/graph/%22Paris%22@en?relation=all&inverse=1)

=== Provided Data ===

We provide
1. a preprocessed version of the Simple Wikipedia wikipedia-ambiguous.txt, which contains ambiguous article titles with their content, as above.
2. a simplified version of the YAGO knowledge base.
3. a template for your code, disambiguator.py
4. a gold standard sample.

=== Task ===

Your task is to complete the function disambiguate() in this file.
It receives as input (1) the ambiguous Wikipedia title ("Paris" in the example), and (2) the article content.
The method shall return the unambiguous entity from YAGO.
In order to ensure a fair evaluation, do not use any non-standard Python libraries except nltk.
The lab will be graded by a variant of the F1 score that gives higher weight to precision (with beta=0.5).

Input:
<Babilonia_0>
Babilonia is a 1987 Argentine drama film directed and written by Jorge Salvador based on a play by Armando Discépolo.

Output:
<Babilonia_0> TAB <Babilonia>

=== Development and Testing ===

In YAGO, the entities have readable ids, as in <Ashok_Kumar_(British_politician)>. This is, however, not the case in all knowledge bases. Therefore, your algorithm should not rely on the suffix "British Politician"!

To enforce this, we deliver two versions of the lab:
1. Development: With readable entity ids
The corresponding YAGO knowledge base is dev_yago.tsv, and the gold standard is dev_gold_samples.tsv
2. Testing: Without readable entity ids
The corresponding YAGO knowledge base is test_yago.tsv. Here, the British politician has the id <Ashok_Kumar_1081507>. This is the file that you will be evaluated on!
   
=== Submission ===

1. Take your code, any necessary resources to run the code, and the output of your code on the test dataset (no need to put the other datasets!)
2. ZIP these files in a file called firstName_lastName.zip
3. submit it here before the deadline announced during the lab:

https://www.dropbox.com/request/aFP23kphMb4isbYGz0gm


=== Contact ===

If you have any additional questions, you can send an email to: nedeljko.radulovic@telecom-paris.fr
"""

# import custom packages
from utils import Parsy
from utils import KnowledgeBase
from utils import evaluate

# a preprocessed version of the Simple Wikipedia wikipedia-ambiguous.txt,
# which contains ambiguous article titles with their content.
wikipedia_file = "wikipedia-ambiguous.txt"

# development dataset (suffix is readable)
# [ dev_kb_file ] a simplified YAGO knowledge base
# [ dev_result_file ] generate your prediction
# [ dev_gold_file ] a certain number of gold standard samples
dev_kb_file = "dev_yago.tsv"
dev_result_file = "dev_results.tsv"
dev_gold_file = 'dev_gold_samples.tsv'

# test dataset (suffix is un-readable)
# [ test_kb_file ] a simplified YAGO knolwdge base
# [ test_result_file ] generate your prediction
# [ test_gold_file ] a certain number of gold standard samples
test_kb_file = "test_yago.tsv"
test_result_file = "results.tsv"
test_gold_file = 'test_gold_samples.tsv'


# YOUR CODE GOES HERE
def disambiguate(entityName, text, kb):
    '''

    :param entityName: a string, name appearing in wikipedia-ambiguous.txt
    :param text: a corresponding context
    :param kb: knowledge base
    :return: return a correct entity from this kb
    '''
    print(entityName, text)
    return "<Elvis>"


def evaluate_on_dev():
    '''
    evaluate your model on the development dataset.
    In the development dataset, each entity name (suffix) is readable.
    :return:
    '''

    # load YAGO knowledge base
    # example: kb.facts["<Babilonia>"]
    kb = KnowledgeBase(dev_kb_file)

    # predict each record and generate results.tsv file
    with open(dev_result_file, 'w', encoding="utf-8") as output:
        for page in Parsy(wikipedia_file):
            result = disambiguate(page.label(), page.content, kb)
            if result is not None:
                output.write(page.title+"\t"+result+"\n")

    # evaluate
    evaluate(dev_result_file, dev_gold_file)


def evaluate_on_test():
    '''
    evaluate your model on the test dataset.
    In the test dataset, each entity name (suffix) is un-readable.
    We hide all suffixes.
    :return:
    '''

    # load YAGO knowledge base
    # example: kb.facts["<Babilonia_1049451>"]
    kb = KnowledgeBase(test_kb_file)

    # predict each record and generate results.tsv file
    with open(test_result_file, 'w', encoding="utf-8") as output:
        for page in Parsy(wikipedia_file):
            result = disambiguate(page.label(), page.content, kb)
            if result is not None:
                output.write(page.title + "\t" + result + "\n")

    # evaluate
    evaluate(test_result_file, test_gold_file)


# evaluate
evaluate_on_dev()
evaluate_on_test()
