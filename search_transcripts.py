import glob
import json

files = glob.glob(r'C:\Users\D\.gemini\antigravity-ide\brain\*\.system_generated\logs\transcript.jsonl')
for f in files:
    print('Checking:', f)
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        for idx, line in enumerate(fp):
            if any(k in line.lower() for k in ['<svg', 'orange', 'particle-blue', 'c85a32', 'color']):
                try:
                    obj = json.loads(line)
                    text = json.dumps(obj)
                    if '<svg' in text:
                        # find snippet around <svg
                        pos = text.find('<svg')
                        snippet = text[pos:pos+400]
                        print(f'Match at line {idx}: {snippet}')
                except Exception as e:
                    pass
