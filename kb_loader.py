import re

def load_kb(path='knowledgeBase.txt'):
    docs = []
    with open(path, 'r') as f:
        content = f.read()

    # Split into documents: assume each starts with [DOC-x]
    raw_docs = re.split(r'\n\s*\[DOC-', content)
    for raw in raw_docs:
        raw = raw.strip()
        if not raw:
            continue

        # put back [DOC-x] since split removed it
        raw = "[DOC-" + raw if not raw.startswith("[DOC-") else raw

        # Parse ID
        m_id = re.match(r'\[DOC-(\d+)\]', raw)
        doc_id = f"DOC_{m_id.group(1)}" if m_id else f"unknown_{len(docs)}"

        # Parse title
        m_title = re.search(r'Title:\s*(.*)', raw)
        title = m_title.group(1).strip() if m_title else ""

        # Parse text
        m_text = re.search(r'Text:\s*(.*)', raw, flags=re.DOTALL)
        body = m_text.group(1).strip() if m_text else ""

        docs.append({
            'id': doc_id,
            'title': title,
            'body': body
        })
    return docs

