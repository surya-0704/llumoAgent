# Simple rule-based planner that maps queries to tool steps
import re, uuid

def plan_query(query: str):
    q = query.lower()
    steps = []
    sid = 1
    if 'refund' in q or 'refund policy' in q:
        steps.append({'id': sid, 'tool': 'PolicyLookup', 'args': {'query':'refund', 'k':3}, 'timeout_ms':2000, 'retries':2}); sid+=1
    if 'data retention' in q or 'retention' in q:
        steps.append({'id': sid, 'tool': 'Retriever', 'args': {'query':'data retention','k':3}, 'timeout_ms':2000, 'retries':2}); sid+=1
    # calculator detection: look for percent or arithmetic
    if re.search(r'\d+%|percent|calculate|compute|\+', query.lower()):
        # extract simple expression if present
        expr = None
        m = re.search(r'compute (.*)', query.lower())
        if m:
            expr = m.group(1)
        # fallback: look for pattern like '15% of 2000'
        m2 = re.search(r'(\d+)% of (\d+)', query.lower())
        if m2:
            percent = int(m2.group(1))/100.0
            amount = int(m2.group(2))
            expr = f"{percent}*{amount}"
        if expr:
            steps.append({'id': sid, 'tool': 'Calculator', 'args': {'expression': expr}, 'timeout_ms':500, 'retries':1}); sid+=1
        else:
            # generic calculator step for percent-only requests
            if re.search(r'\d+% of \d+', query.lower()):
                m3 = re.search(r'(\d+)% of (\d+)', query.lower())
                percent = int(m3.group(1))/100.0
                amount = int(m3.group(2))
                steps.append({'id': sid, 'tool': 'Calculator', 'args': {'expression': f"{percent}*{amount}"}, 'timeout_ms':500, 'retries':1}); sid+=1
    # extract percentages from policy:
    if 'extract all percentages' in q or 'extract percentages' in q or 'percent' in q and 'policy' in q:
        steps.append({'id': sid, 'tool': 'PolicyLookup', 'args': {'query':'refund','k':3}, 'timeout_ms':2000, 'retries':2}); sid+=1
        steps.append({'id': sid, 'tool': 'StringTools', 'args': {'action':'extract_percentages'}, 'timeout_ms':500, 'retries':1}); sid+=1
    # fallback: if no steps, call Retriever
    if not steps:
        steps.append({'id': sid, 'tool': 'Retriever', 'args': {'query': query, 'k':3}, 'timeout_ms':2000, 'retries':2})
    return steps
