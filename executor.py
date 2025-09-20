import time, json, hashlib
from cachetools import TTLCache
from tools.retriever import Retriever
from tools.policy_lookup import PolicyLookup
from tools.calculator import Calculator
from tools.string_tools import StringTools

# simple in-memory cache
CACHE = TTLCache(maxsize=1000, ttl=300)

TOOL_MAP = {
    'Retriever': Retriever().run,
    'PolicyLookup': PolicyLookup().run,
    'Calculator': Calculator().run,
    'StringTools': StringTools().run
}

def _cache_key(tool_name, args):
    s = tool_name + json.dumps(args, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def execute_tool(tool_name, args, timeout_ms=2000, max_retries=2, cache_ttl_s=300):
    key = _cache_key(tool_name, args)
    now = time.time()
    # check cache
    if key in CACHE:
        res = CACHE[key].copy()
        res['meta']['from_cache'] = True
        return res
    # execute with retries (simple)
    attempt = 0
    last_err = None
    while attempt <= max_retries:
        try:
            start = time.time()
            fn = TOOL_MAP.get(tool_name)
            if not fn:
                raise Exception(f"Unknown tool: {tool_name}")
            result = fn(args)
            latency = int((time.time()-start)*1000)
            out = {
                'success': True,
                'tool_name': tool_name,
                'args': args,
                'result': result,
                'meta': {'latency_ms': latency, 'from_cache': False},
                'error': None
            }
            CACHE[key] = out
            return out
        except Exception as e:
            last_err = str(e)
            attempt += 1
            time.sleep(0.1 * attempt)  # backoff
    return {
        'success': False,
        'tool_name': tool_name,
        'args': args,
        'result': None,
        'meta': {'latency_ms': 0, 'from_cache': False},
        'error': last_err
    }
