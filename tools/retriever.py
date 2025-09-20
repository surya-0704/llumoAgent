# # Very simple keyword-based retriever using knowledgeBase.txt
# import os, re, json
# from kb_loader import load_kb

# class Retriever:
#     def __init__(self):
#         self.docs = load_kb()

#     def run(self, args):
#         query = args.get('query','').lower()
#         k = args.get('k',3)
#         results = []
#         if not query:
#             return results
#         q_terms = re.findall(r"\\w+", query)
#         for doc in self.docs:
#             text = (doc.get('title','') + ' ' + doc.get('body','')).lower()
#             score = 0
#             for t in q_terms:
#                 score += text.count(t)
#             if score>0:
#                 results.append({'doc_id': doc['id'], 'title':doc.get('title',''), 'text':doc.get('body',''), 'score':score})
#         results.sort(key=lambda x: x['score'], reverse=True)
#         return results[:k]


import re
import os,sys
from kb_loader import load_kb

class Retriever:
    def __init__(self):
        self.docs = load_kb()

    def run(self, args):
        query = args.get('query','')
        if not query:
            return []
        query = query.lower()
        k = args.get('k',3)

        # normalize query terms to lowercase
        q_terms = [t.lower() for t in re.findall(r"\w+", query)]

        results = []
        for doc in self.docs:
            text = (doc.get('title','') + ' ' + doc.get('body','')).lower()
            score = sum(text.count(t) for t in q_terms)
            if score > 0:
                results.append({
                    'doc_id': doc['id'],
                    'title': doc.get('title',''),
                    'text': doc.get('body',''),
                    'score': score
                })

        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:k]
