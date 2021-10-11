# YOUR CODE GOES HERE
def jaccard_sim(doc1, doc2):    
    words_doc1 = set(doc1.lower().split()) 
    words_doc2 = set(doc2.lower().split())
    
    intersection = words_doc1.intersection(words_doc2)
    union = words_doc1.union(words_doc2)
        
    return float(len(intersection)) / len(union)

def weighted_jaccard(doc1, doc2):
    # necessary imports
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
    
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([doc1, doc2])
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    result = cosine_similarity(np.array(denselist[0]).reshape(1,-1), np.array(denselist[1]).reshape(1,-1))
    return result

def disambiguate(entityName, text, kb):
    '''
    :param entityName: a string, name appearing in wikipedia-ambiguous.txt
    :param text: a corresponding context
    :param kb: knowledge base
    :return: return a correct entity from this kb
    '''
    
#     print('entityName=', entityName)
#     print('text:', text)
        
    best_match = None
    score_best = 0
    all_candidates = set()
    for ikey in kb.inverseFacts:
        if entityName in ikey and ikey[0] == '\"': # todo \"
#             print('ikey=', ikey)
            if '<label>' in kb.inverseFacts[ikey]: # todo
                all_candidates = set.union(all_candidates, kb.inverseFacts[ikey]['<label>'])
#             elif '<image>' in kb.inverseFacts[ikey]: # todo
#                 all_candidates = set.union(all_candidates, kb.inverseFacts[ikey]['<image>'])
            elif '<description>' in kb.inverseFacts[ikey]: # todo
                all_andidates = set.union(all_candidates, kb.inverseFacts[ikey]['<description>'])
            elif '<name>' in kb.inverseFacts[ikey]: # todo
                all_candidates = set.union(all_candidates, kb.inverseFacts[ikey]['<name>'])
            elif '<also_known_as>' in kb.inverseFacts[ikey]: # todo
                all_candidates = set.union(all_candidates, kb.inverseFacts[ikey]['<also_known_as>'])
            else: # todo: deal with the candidates that have an attribute in which the surface form appears
#                 print("no label key:", kb.inverseFacts[ikey])
#                 for attr in kb.inverseFacts[ikey]:
#                     if attr != '<label>':
#                         print(text, '[]', entityName)
#                         print(kb.inverseFacts[ikey][attr]) 
                return None # todo
#     print('all candidates:', all_candidates)

    for key in all_candidates: # key = candidate
#         print('candidate:', key)
#         if '<label>' in kb.facts[key]:
#             print(kb.facts[key]['<label>'])
        # label similarity: between the provided entityName and some attribute details
        hand_selected_attr = ['<label>', '<description>', '<name>'] # todo
#         hand_selected_attr = ['<label>']
        long_details = ""
        for attr in hand_selected_attr:
            if attr in kb.facts[key]: # if the attribute exists (to avoid the error)
                info = kb.facts[key][attr]
                # print('info:', info)
                info = next(iter(kb.facts[key][attr]))[1:-1]
                long_details += (info + ' ')
        # print("long details:", long_details)
#         print('provided infos for Jaccard sim computation:', entityName, ' and ', long_details)
        score_label_sim = jaccard_sim(text, long_details)
#         print('score of label similarity:', score_label_sim)

#         if score_label_sim > score_best:
#             score_best = score_label_sim
#             best_match = key
    
#         Todo: the next few lines
#         if score_label_sim == 1:
#             return key

        # context similarity
        long_details = ""
        for attr in kb.facts[key]:
            info = kb.facts[key][attr]
#             print('info:', info)
            for i in info: # for every element of set
                # print(i)
                if i[0] == '<': # facts key (id)
                    if i in kb.facts:
#                         print('kb facts of', i, ':', kb.facts[i])
                        if '<label>' in kb.facts[i]: # ading info to long_details (working with labels)
                            for word in kb.facts[i]['<label>']:
                                if word[0] == '\"':
                                    word = word[1:-1]
                                long_details += (word + ' ')

#                             word = next(iter(kb.facts[i]['<label>']))
#                             if word[0] == '\"':
#                                 word = word[1:-1]
#                             long_details += (word + ' ')
#                 elif i[0] == '\"':
#                     print(i)
#                     long_details += (i + ' ')
                    # if i in kb.inverseFacts:
                        # print(kb.inverseFacts[i])
                # long_details += (i[1:-1]+' ')
#         print(long_details)

#         score_context_sim = jaccard_sim(text, long_details)
        score_context_sim = weighted_jaccard(text, long_details)
#         cur_score = score_context_sim
        cur_score = 0.5*score_label_sim+0.5*score_context_sim
        if cur_score > score_best:
            score_best = cur_score
            best_match = key
#     print()
    NIL_threshold = 0.05
    if score_best > NIL_threshold:
        return best_match

    return None
    