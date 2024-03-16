import json
import re

import pandas as pd
from nltk.tokenize import sent_tokenize
# from process_data import process_data
# from LER_model import LER_model
# from MR_classify_model import MR_classify_model
from Material_Data_Miners.Words_Token_model.process_data import process_data
from Material_Data_Miners.Words_Token_model.LER_model import LER_model
from Material_Data_Miners.Words_Token_model.MR_classify_model import MR_classify_model

class getLiteratureData():
    def __init__(self):
        self.value_ent_path = "Material_Data_Miners/Words_Token_model/config/value_entity_default.json"
        self.perf_ent_path = "Material_Data_Miners/Words_Token_model/config/perf_entity_default.json"
        self.material_ent_path = "Material_Data_Miners/Words_Token_model/config/material_entity_default.json"
        self._replace_space_list_path = 'Material_Data_Miners/Words_Token_model/config/relation_schema.json'


    def load_relation_schema(self):
        re_list = []
        relation_ent_path = self._replace_space_list_path
        with open(relation_ent_path, 'r', encoding='utf-8') as load_f:
            temp = load_f.readlines()
            for line in temp:
                dic = json.loads(line)

                txt = dic["describe"]
                re_ = {
                    "describe": txt,
                    "re_list": dic["re"],
                    "value_re_list": dic['value'],
                    "Similar_keywords": dic['Similar_keywords'],
                    "keywords": dic["keywords"]
                }
                re_list.append(re_)
        return re_list


    def load_entity_schema(self):
        keywords_list = []

        with open(self.material_ent_path, 'r', encoding='utf-8') as load_f:
            injson = json.load(load_f)
            temp = []
            for line in injson:
                temp.append(line)
            keywords_list.append(temp)
        with open(self.perf_ent_path, 'r', encoding='utf-8') as load_f:
            injson = json.load(load_f)
            temp = []
            for line in injson:
                temp.append(line)
            keywords_list.append(temp)
        with open(self.value_ent_path, 'r', encoding='utf-8') as load_f:
            injson = json.load(load_f)
            temp = []
            for line in injson:
                temp.append(line)
            keywords_list.append(temp)
        return keywords_list

    def getLiteratureData_words_token(self, origion_text,keywords=None):

        out_data = []
        count = 0
        no_value_count = 0

        keywords_list = []
        data_process = process_data()
        replace_list = self.load_relation_schema()
        ler_model = LER_model()
        if keywords != None:

            for i in keywords:
                keywords_list.append(i)
        if len(keywords_list) == 0:
            return None

        text = origion_text
        origion = text
        text = data_process.replace_space(text, replace_list)

        if text[-1:] == '.':
            text = text[:-1]
        text_token = text.split(" ")
        for keyword_item in keywords_list:
            for keyword in keyword_item:
                for keyword_ in keyword['keywords'].split(","):
                    res, res_idx = ler_model.LER_regular(keyword_, text)

                    if len(res) > 0:

                        for res_item in res:
                            temp = res_item
                            temp['entity_type'] = keyword['entity_type']
                            temp['keywords'] = keyword_
                            if len(temp['entity'].split(" ")) == 1:
                                words_index = 0
                                flag = False
                                for words in text_token:

                                    if words == temp['entity']:
                                        temp['entity_token_index'] = words_index
                                        flag = True
                                    words_index = words_index + 1
                                if flag == False:
                                    text = text.replace(",", " ,")
                                    text_token = text.split(" ")
                                    words_index = 0
                                    for words in text_token:

                                        if words == temp['entity']:
                                            temp['entity_token_index'] = words_index
                                            flag = True
                                        words_index = words_index + 1
                                temp['source_text'] = origion_text
                                temp['source_text_process'] = text
                                temp['source_text_word_token'] = text_token
                                out_data.append(temp)

                            else:
                                words_index = 0
                                flag = False
                                left = int(temp['entity_char_index'].split(",")[0])
                                right = int(temp['entity_char_index'].split(",")[1])
                                left_text = text[:left]
                                words_index = len(left_text.split(" "))
                                temp['entity_token_index'] = words_index - 1
                                # temp['source_text'] = text
                                temp['source_text'] = origion_text
                                temp['source_text_process'] = text
                                temp['source_text_word_token'] = text_token
                                out_data.append(temp)

        ret_data = pd.DataFrame(out_data)
        return ret_data

    def classfily_data(self, data):
        mr_classify_model = MR_classify_model()
        data = mr_classify_model._is_one_to_many(data)
        data = mr_classify_model.many_to_many_classfiy(data)
        data = mr_classify_model.last_step(data)
        return data
