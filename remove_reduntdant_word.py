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
            my_dict = {}
            for i in range(len(arr)):
                if not arr[i] in my_dict:
                    my_dict[arr[i]] = 1
                else:
                    my_dict[arr[i]] = my_dict[arr[i]] + 1
            arr.clear()
            for key in my_dict:
                arr.append(key)
    print(str(cnt) + " " + file)
    with codecs.open(file, 'w', "utf-8") as outfile:
        outfile.write(json.dumps(json_data, ensure_ascii=False))
