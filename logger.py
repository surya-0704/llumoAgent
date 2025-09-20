import json, time, os
LOG_PATH = 'logs.json'

class Logger:
    def __init__(self, path=LOG_PATH):
        self.path = path
        # ensure file exists with empty array
        if not os.path.exists(self.path):
            with open(self.path,'w') as f:
                json.dump([],f)

    def log(self, query_id, stage, payload):
        entry = {'query_id': query_id, 'time': time.time(), 'stage': stage, 'detail': payload}
        with open(self.path,'r+') as f:
            try:
                arr = json.load(f)
            except:
                arr = []
            arr.append(entry)
            f.seek(0)
            json.dump(arr, f, indent=2)
            f.truncate()
