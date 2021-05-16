import os
import json
import codecs
from underthesea import chunk
from underthesea import word_tokenize

os.chdir('/home/thanhnguyen/Test/cuhk-vi')
myfile = 'cuhk_vi_20202.json'
processed_tokens = list()
cnt= 0
with open(myfile, 'r', encoding = "utf-8") as f0:
    json_data = json.load(f0)
for id in range(len(json_data)):
    if "processed_tokens" in json_data[id]:
        processed_tokens = json_data[id]['processed_tokens']
        for i in range(len(processed_tokens)):
            processed_token = processed_tokens[i]
            for ii in range(len(processed_token)):
                processed_token[ii] = word_tokenize(processed_token[ii], format="text")
    if "captions" in json_data[id]:
        for cap_id in range(len(json_data[id]['captions'])):
            json_data[id]['captions'][cap_id] = word_tokenize(json_data[id]['captions'][cap_id], format="text")
    cnt = cnt + 1
    print(str(cnt))
with codecs.open('reid_raw.json', 'w', "utf-8") as outfile:
    outfile.write(json.dumps(json_data, ensure_ascii=False))
