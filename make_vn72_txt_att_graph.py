import os
import json
import codecs
from underthesea import chunk
from underthesea import word_tokenize
UPPERBODY = 1
LOWERBODY = 2
PERSON = 5
FACE = 7
SHOE = 3
HAIR = 4
HAT = 6
BACKPACK = 8
OTHER = 10
GLASSES = 9
os.chdir('/home/thanhnguyen/Test/cuhk-vi')
myfile = 'vi-72-Copy.json'
cnt = 0
dictionary = {
    "áo": UPPERBODY,
    "phéc mơ tuya":UPPERBODY,
    "quần": LOWERBODY,
    "váy": LOWERBODY,
    "kaki":LOWERBODY,
    "người":PERSON,
    "cô gái":PERSON,
    "phụ nữ":PERSON,
    "nữ giới":PERSON,
    "đàn bà":PERSON,
    "bà":PERSON,
    "nữ":PERSON,
    "nam":PERSON,
    "đàn ông":PERSON,
    "đứa trẻ":PERSON,
    "cậu": PERSON,
    "gái":PERSON,
    "con gái":PERSON,
    "con trai":PERSON,
    "trai":PERSON,
    "quý bà":PERSON,
    "quý ông":PERSON,
    "cô":PERSON,
    "anh":PERSON,
    "sinh viên":PERSON,
    "thanh niên":PERSON,
    "giày":SHOE,
    "đôi ủng":SHOE,
    "ủng":SHOE,
    "dép":SHOE,
    "dép lê":SHOE,
    "tất":SHOE,
    "vớ":SHOE,
    "tóc":HAIR,
    "mái tóc":HAIR,
    "trọc":HAIR,
    "hói":HAIR,
    "mũ":HAT,
    "nơ":HAIR,
    "túi":BACKPACK,
    "giỏ":BACKPACK,
    "ví":BACKPACK,
    "ba lô":BACKPACK,
    "balo":BACKPACK,
    "cặp sách":BACKPACK,
    "khăn":OTHER,
    "trang phục":OTHER,
    "vai":OTHER,
    "thắt lưng":OTHER,
    "cổ":OTHER,
    "vòng":OTHER,
    "mặt": FACE,
    "da": FACE,
    "trang sức": OTHER,
    "kính":GLASSES,
    "mắt kính":GLASSES,
    "mắt kiếng":GLASSES
}
upperbody_lst = list()
lowerbody_lst = list()
person_lst = list()
shoe_lst = list()
hair_lst = list()
hat_lst = list()
backpack_lst = list()
face_lst = list()
glasses_lst = list()
other_lst = list()
map_queue = {
    UPPERBODY : upperbody_lst,
    LOWERBODY: lowerbody_lst,
    PERSON: person_lst,
    SHOE: shoe_lst,
    HAIR: hair_lst,
    HAT: hat_lst,
    BACKPACK: backpack_lst,
    FACE: face_lst,
    GLASSES: glasses_lst,
    OTHER: other_lst
}
#dummy
# chunked = [('một', 'M', 'B-NP'), ('người', 'N', 'B-NP'), ('đi', 'V', 'B-VP'), ('bộ', 'N', 'B-NP'), ('với', 'E', 'B-PP'), ('mái tóc', 'N', 'B-NP'), ('sẫm', 'N', 'B-NP'), ('màu', 'N', 'B-NP'), ('đang', 'R', 'O'), ('đi', 'V', 'B-VP'), ('giày', 'N', 'B-NP'), ('đỏ', 'A', 'B-AP'), ('và', 'C', 'O'), ('trắng', 'A', 'B-AP'), ('áo', 'N', 'B-NP'), ('trùm', 'N', 'B-NP'), ('đầu', 'N', 'B-NP'), ('màu', 'N', 'B-NP'), ('đen', 'A', 'B-AP'), ('và', 'C', 'O'), ('quần', 'N', 'B-NP'), ('đen', 'A', 'B-AP')]
# chunked = [('cô', 'Nc', 'B-NP'), ('ấy', 'P', 'B-NP'), ('mặc', 'V', 'B-VP'), ('một', 'M', 'B-NP'), ('chiếc', 'Nc', 'B-NP'), ('áo', 'N', 'B-NP'), ('ngắn', 'A', 'B-AP'), ('tay', 'N', 'B-NP'), ('màu', 'N', 'B-NP'), ('xanh lá', 'N', 'B-NP'), ('cây', 'N', 'B-NP')]
# chunked = [('người', 'Nc', 'B-NP'), ('phụ nữ', 'N', 'B-NP'), ('mặc', 'V', 'B-VP'), ('một', 'M', 'B-NP'), ('chiếc', 'Nc', 'B-NP'), ('áo dài', 'N', 'B-NP'), ('tay', 'N', 'B-NP'), ('màu', 'N', 'B-NP'), ('đen', 'A', 'B-AP'), ('tay', 'N', 'B-NP'), ('cầm', 'V', 'B-VP'), ('một', 'M', 'B-NP'), ('chiếc', 'Nc', 'B-NP'), ('túi', 'N', 'B-NP'), ('màu', 'N', 'B-NP'), ('đen', 'A', 'B-AP'), ('và', 'C', 'O'), ('mặc', 'V', 'B-VP'), ('quần', 'N', 'B-NP'), ('đen', 'A', 'B-AP'), ('và', 'C', 'O'), ('giày', 'N', 'B-NP'), ('thể thao', 'N', 'B-NP'), ('màu', 'N', 'B-NP'), ('đen', 'A', 'B-AP')]

#define state
READ = 0
INSERT = 1
TEMP = 2
state = READ
next_state = READ
tmp_queue = list()
caption_id = 0
file_path = ""
file_name = ""
caption = ""
chunked = []
processed_token = []
with open(myfile, 'r', encoding = "utf-8") as f0:
    json_data = json.load(f0)
os.chdir('/home/thanhnguyen/ViTAA/datasets/cuhkpedes/text_attribute_graph')
for id in range(len(json_data)):
    if "file_path" in json_data[id]:
        file_path = json_data[id]['file_path'].replace('/','-')
    if "captions" in json_data[id]:
        for cap_id in range(len(json_data[id]['captions'])):
            processed_token = json_data[id]['processed_tokens'][cap_id]
            file_name = file_path + "-" + str(cap_id) + ".json"
            caption = json_data[id]['captions'][cap_id]
            chunked = chunk(caption)
            target_queue = 999
            chunked_len = len(chunked)
            append = False
            upperbody_lst.clear()      
            lowerbody_lst.clear()      
            person_lst.clear()      
            shoe_lst.clear()      
            hair_lst.clear()  
            hat_lst.clear()      
            backpack_lst.clear()      
            glasses_lst.clear()      
            other_lst.clear()      
            face_lst.clear()
            j = 0
            temp = ""
            while j < chunked_len:
                temp = chunked[j][0]
                chunked[j][0] = temp.lower()
                state = next_state
                if state == READ:
                    if chunked[j][2] == 'B-NP':
                        next_state = READ
                        if chunked[j][0] in dictionary:
                            if dictionary[chunked[j][0]] < target_queue:
                                target_queue = dictionary[chunked[j][0]]
                        else:
                            #split and check
                            split_words = chunked[j][0].split()
                            for w in range(len(split_words)):
                                if split_words[w] in dictionary:
                                    if dictionary[split_words[w]] < target_queue:
                                        target_queue = dictionary[split_words[w]]
                                if "màu" in split_words[w]:
                                    append = True
                        if chunked[j][1] == 'N' and processed_token.count(temp) > 0:
                            if tmp_queue.count(temp) == 0:
                                tmp_queue.insert(0, temp)
                        elif chunked[j][1] == 'Nc' and target_queue == PERSON and processed_token.count(temp) > 0:
                            if tmp_queue.count(temp) == 0:
                                tmp_queue.insert(0, temp)
                    elif chunked[j][2] == 'B-AP' and processed_token.count(temp) > 0:
                        if tmp_queue.count(temp) == 0:
                            tmp_queue.insert(0, temp)
                        next_state = TEMP
                        #j = j -1
                    elif chunked[j][0] == '/':
                        next_state = READ
                    else:
                        next_state = TEMP
                        j = j - 1
                if state == TEMP:
                    if chunked[j][2] == 'B-NP':
                        next_state = INSERT
                        j = j - 1
                    elif chunked[j][2] == 'B-AP':
                        next_state = READ
                        j = j - 1
                if state == INSERT:
                    if target_queue in map_queue:
                        for i in range(len(tmp_queue)):
                            item = tmp_queue.pop()
                            #item = word_tokenize(item, format="text")
                            item = item.replace(" ","")
                            map_queue[target_queue].append(item)
                        target_queue = 999 - target_queue
                    elif append:
                        target_queue = 999 - target_queue
                        if target_queue in map_queue:
                            for i in range(len(tmp_queue)):
                                item = tmp_queue.pop()
                                #item = word_tokenize(item, format="text")
                                item = item.replace(" ","")
                                map_queue[target_queue].append(item)
                            target_queue = 999 - target_queue
                        else:
                            target_queue = 999
                    else:
                        target_queue = 999
                        tmp_queue.clear()
                    j = j - 1
                    next_state = READ
                    append = False
                j = j + 1
                if j == chunked_len:
                    if target_queue in map_queue:
                        for i in range(len(tmp_queue)):
                            item = tmp_queue.pop()
                            #item = word_tokenize(item, format="text")
                            item = item.replace(" ","")
                            map_queue[target_queue].append(item)
                    elif append:
                        target_queue = 999 - target_queue
                        if target_queue in map_queue:
                            for i in range(len(tmp_queue)):
                                item = tmp_queue.pop()
                                #item = word_tokenize(item, format="text")
                                item = item.replace(" ","")
                                map_queue[target_queue].append(item)
                            target_queue = 999 - target_queue
                        else:
                            target_queue = 999
                        append = False

            data = []
            if len(other_lst) > 0:
                data.insert(0,{"other":other_lst})
            if len(glasses_lst) > 0:
                data.insert(0,{"glasses":glasses_lst})
            if len(backpack_lst) > 0:
                data.insert(0,{"backpack":backpack_lst})
            if len(shoe_lst) > 0:
                data.insert(0,{"shoe":shoe_lst})
            if len(hair_lst) > 0:
                data.insert(0,{"hair":hair_lst})
            if len(hat_lst) > 0:
                data.insert(0,{"hat":hat_lst})
            if len(face_lst) > 0:
                data.insert(0,{"face":face_lst})
            if len(lowerbody_lst) > 0:
                data.insert(0,{"lowerbody":lowerbody_lst})
            if len(upperbody_lst) > 0:
                data.insert(0,{"upperbody":upperbody_lst})
            if len(person_lst) > 0:
                data.insert(0,{"person":person_lst})
            with codecs.open(file_name, 'w', "utf-8") as outfile:
                    outfile.write(json.dumps(data, ensure_ascii=False))         
            print(file_name)
            file_name = ""

