import json
import re

import pandas as pd
from nltk.tokenize import sent_tokenize

# import nltk.data
from Material_Data_Miners.Words_Token_model.MER_model import MER_model
from Material_Data_Miners.Words_Token_model.MR_classify_model import MR_classify_model
from Material_Data_Miners.Words_Token_model.MVR_model import MVR_model
from Material_Data_Miners.Words_Token_model.process_data import process_data


class getMaterialData():
    def __init__(self):
        self.value_ent_path = "value_schema_test.json"
        self.relation_ent_path = "relation_schema.json"
        self.material_ent_path = "material_schema_test.json"

    def load_value_schema(self):
        with open(self.value_ent_path, 'r', encoding='utf-8') as load_f:
            temp = load_f.readlines()
            for line in temp:
                dic = json.loads(line)
                txt = dic["describe"]
                re_list = dic["re"]

        return re_list

    def load_relation_schema(self):
        re_list = []
        relation_ent_path = 'Material_Data_Miners/Words_Token_model/config/relation_schema.json'
        with open(relation_ent_path, 'r', encoding='utf-8') as load_f:
            temp = load_f.readlines()
            for line in temp:
                dic = json.loads(line)

                txt = dic["describe"]
                # re_list.extend(dic["re"])
                re_ = {
                    "describe": txt,
                    "re_list": dic["re"],
                    "value_re_list": dic['value'],
                    "Similar_keywords": dic['Similar_keywords'],
                    "keywords": dic["keywords"]
                }
                re_list.append(re_)
        return re_list

    def load_material_schema(self):
        re_list = []
        with open(self.material_ent_path, 'r', encoding='utf-8') as load_f:
            temp = load_f.readlines()
            for line in temp:
                dic = json.loads(line)
                txt = dic["describe"]
                re_list.extend(dic["re"])
        return re_list

    def getMaterialData_words_token(self, origion_text):
        data_out = []
        mer_model = MER_model()
        mvr_model = MVR_model()
        data_process = process_data()
        relation_re_list = self.load_relation_schema()
        count = 0
        no_value_count = 0
        sent_tokenize_list = sent_tokenize(origion_text)
        for sent_index in range(len(sent_tokenize_list)):

            text = sent_tokenize_list[sent_index]
            origion = text
            text = data_process.replace_space(text, relation_re_list)
            # text = replace_space(text,relation_re_list)
            if text[-1:] == '.':
                text = text[:-1]
            text_token = text.split(" ")
            material_ent, material_index_char = mer_model.MER_regular(text)
            if len(material_ent) > 0:
                material_index_token = []
                words_index = 0
                for material_idx in material_ent:
                    for words in text_token:
                        # for material_idx in material_ent:
                        # print(type(material_idx))
                        if words == material_idx:
                            material_index_token.append(words_index)
                        words_index = words_index + 1
                if len(material_index_token) == 0:
                    words_index = 0
                    text = text.replace(",", " ,")
                    text_token = text.split(" ")
                    for material_idx in material_ent:
                        for words in text_token:
                            # for material_idx in material_ent:
                            if words == material_idx:
                                material_index_token.append(words_index)
                            words_index = words_index + 1

                for relations in relation_re_list:
                    value_index_box = []
                    re_list = relations['value_re_list']
                    describe = relations['describe']
                    for relation in relations['re_list']:
                        relation_text = re.findall(relation, text)
                        if len(relation_text) != 0:
                            for i in re_list:
                                # print(relation,i)
                                # re_str = r'\d+.\d+' + i
                                value_ent, value_index_char = mvr_model.MVR_regular(text, i)
                                # print(value_ent,value_index_char)
                                if len(value_ent) != 0:
                                    value_index_token = []
                                    words_index = 0
                                    for value_idx in value_ent:
                                        for words in text_token:
                                            if words == (str(value_idx)):
                                                # value_index_token.append(9999)
                                                value_index_token.append(words_index)
                                            words_index = words_index + 1

                                    if len(value_index_token) == 0:
                                        words_index = 0
                                        text = text.replace(",", " ,")
                                        text_token = text.split(" ")
                                        for value_idx in value_ent:
                                            for words in text_token:
                                                # for value_idx in value_ent:
                                                # print(words, str(value_idx), words == str(value_idx), words_index)
                                                if words == (str(value_idx)):
                                                    value_index_token.append(words_index)
                                                words_index = words_index + 1
                                    value_text = ""
                                    material_text = ""
                                    value_index_text_char = ""
                                    value_index_text_token = ""
                                    material_index_text_char = ""
                                    material_index_text_token = ""
                                    for value_idx in range(len(value_ent)):
                                        value_text = value_text + str(value_ent[value_idx]) + ","
                                    value_text = value_text.replace("(", "")
                                    value_text = value_text.replace(")", "")
                                    for material_idx in range(len(material_ent)):
                                        material_text = material_text + str(material_ent[material_idx]) + "[SEP]"

                                    for value_idx in range(len(value_index_char)):
                                        value_index_text_char = value_index_text_char + str(
                                            value_index_char[value_idx]) + "#"
                                    for value_idx in range(len(value_index_token)):
                                        value_index_text_token = value_index_text_token + str(
                                            value_index_token[value_idx]) + "#"
                                    for material_idx in range(len(material_index_char)):
                                        material_index_text_char = material_index_text_char + str(
                                            material_index_char[material_idx]) + "#"
                                    for material_idx in range(len(material_index_token)):
                                        material_index_text_token = material_index_text_token + str(
                                            material_index_token[material_idx]) + "#"
                                    single_out = {
                                        "source_text": origion,
                                        "process_text": text,
                                        "words_token_text": str(text_token),
                                        "material_entity": material_text[:-5],
                                        "material_char_index": material_index_text_char[:-1],
                                        "material_token_index": material_index_text_token[:-1],
                                        "relation_text": relation_text[0],
                                        "value_entity": value_text[:-1],
                                        "value_char_index": value_index_text_char[:-1],
                                        "value_token_index": value_index_text_token[:-1],
                                        "describe": describe,
                                        "easy_to_classify": 0
                                    }

                                    data_out.append(single_out)
                                    count = count + 1

                            break


        data_out = pd.DataFrame(data_out)
        temp_data_out = pd.DataFrame(data=data_out)

        data_out = data_out.drop_duplicates()
        data_out = data_process.easy_classify_mne_value(data_out)
        # print(len(data_out))
        return data_out

    def classfily_data(self, data):
        mr_classify_model = MR_classify_model()
        data = mr_classify_model._is_one_to_many(data)
        data = mr_classify_model.many_to_many_classfiy(data)
        data = mr_classify_model.last_step(data)
        return data
