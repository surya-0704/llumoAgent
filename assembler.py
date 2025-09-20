# Assemble final answer from results
def assemble_answer(user_query, results):
    parts = []
    for item in results:
        step = item['step']
        tr = item['result']
        if not tr.get('success', False):
            parts.append(f"[Tool {step['tool']} failed: {tr.get('error')}]" )
            continue
        if step['tool'] in ('Retriever','PolicyLookup'):
            hits = tr['result']
            if hits:
                parts.append(f"{step['tool']} top hit: ({hits[0]['doc_id']}) {hits[0]['title']}: {hits[0]['text']}")
            else:
                parts.append(f"{step['tool']} found no results.")
        elif step['tool'] == 'Calculator':
            res = tr['result']
            parts.append(f"Calculator: {res.get('expression')} = {res.get('value')}")
        elif step['tool'] == 'StringTools':
            parts.append(f"StringTools: {tr['result']}")
    return '\n\n'.join(parts)
