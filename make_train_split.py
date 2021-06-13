import os
import json
import codecs
os.chdir('/home/thanhnguyen/ViTAA/datasets/cuhkpedes/annotations')
myfile = 'reid_raw.json'
cnt = 0
with open(myfile, 'r', encoding = "utf-8") as f0:
    json_data = json.load(f0)
for id in range(len(json_data)):
    print(str(cnt))
    cnt = cnt + 1
    if "TRAINNING_DATA" in json_data[id]['file_path']:
        json_data[id]['split']="train"
with codecs.open(myfile, 'w', "utf-8") as outfile:
    outfile.write(json.dumps(json_data, ensure_ascii=False))
