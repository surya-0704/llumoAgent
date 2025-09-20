import json, uuid, time
from planner import plan_query
from executor import execute_tool
from logger import Logger
from assembler import assemble_answer

logger = Logger('logs.json')

def handle_query(user_query):
    qid = str(uuid.uuid4())
    start = time.time()
    logger.log(qid, 'received', {'query': user_query})
    plan_steps = plan_query(user_query)
    logger.log(qid, 'plan', {'plan': plan_steps})
    results = []
    for step in plan_steps:
        logger.log(qid, 'tool_call', {'step': step})
        tr = execute_tool(step['tool'], step.get('args', {}),
                          timeout_ms=step.get('timeout_ms',2000),
                          max_retries=step.get('retries',2),
                          cache_ttl_s=step.get('cache_ttl_s',300))
        logger.log(qid, 'tool_return', {'step_id': step['id'], 'tool_result': tr})
        results.append({'step': step, 'result': tr})
        # simple critic
        if not tr.get('success', False):
            logger.log(qid, 'critic', {'step_id': step['id'], 'issue': tr.get('error')})
    final_answer = assemble_answer(user_query, results)
    latency_ms = int((time.time()-start)*1000)
    logger.log(qid, 'final', {'answer': final_answer, 'latency_ms': latency_ms})
    return {'query_id': qid, 'final_answer': final_answer, 'latency_ms': latency_ms}

if __name__ == '__main__':
    # run sample queries
    sample_queries = [
        "What is LLUMO AI's core value proposition?",
        "What does the LLUMO Debugger show that helps isolate failures?",
        "What are the official working hours and overtime rules?",
        "How do reimbursements work and how long do they take after approval?",
        "Compute: (125 * 6) - 50 and 15% of 640"
    ]
    outputs = []
    for q in sample_queries:
        out = handle_query(q)
        print('Query:', q)
        print('Answer:', out['final_answer'])
        print('Latency_ms:', out['latency_ms'])
        print('---')
        outputs.append(out)
    # Save a separate file with the run summary
    with open('run_summary.json','w') as f:
        json.dump(outputs,f,indent=2)
