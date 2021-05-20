import os
import json
import codecs
os.chdir('/home/thanhnguyen/ViTAA/datasets/cuhkpedes/text_attribute_graph')
cnt = 0
for file in os.listdir():
    cnt = cnt + 1
    with open(file,'r' ,encoding="utf-8") as f:
        json_data = json.load(f)
    for att in json_data:
        for key in att:
            arr = att[key]
            for i in range(len(arr)):
                arr[i] = arr[i].replace(" ","")
    print(str(cnt) + " " + file)
    with codecs.open(file, 'w', "utf-8") as outfile:
        outfile.write(json.dumps(json_data, ensure_ascii=False))
