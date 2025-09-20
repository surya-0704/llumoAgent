import re
from kb_loader import load_kb

class StringTools:
    def __init__(self):
        self.docs = load_kb()

    def run(self, args):
        action = args.get('action')
        if action == 'extract_percentages':
            # naive scan of all docs for percentages
            out = []
            for d in self.docs:
                text = d.get('body','')
                nums = re.findall(r'\\b(\\d+)%', text)
                if nums:
                    out.append({'doc_id': d['id'], 'percentages': [int(n) for n in nums]})
            return out
        if action == 'extract_numbers':
            q = args.get('text','')
            nums = re.findall(r'\\d+', q)
            return [int(n) for n in nums]
        return []
