from tools.retriever import Retriever

class PolicyLookup:
    def __init__(self):
        self.retriever = Retriever()

    def run(self, args):
        query = args.get('query','')
        k = args.get('k',3)
        hits = self.retriever.run({'query': query, 'k':k})
        # return top hit text with metadata
        out = []
        for h in hits:
            out.append({'doc_id': h['doc_id'], 'title': h['title'], 'text': h['text'], 'score': h['score']})
        return out
