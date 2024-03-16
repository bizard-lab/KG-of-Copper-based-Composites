
import re
import json
import pandas as pd
import numpy as np
import enchant
import sys

from functools import singledispatchmethod
class LER_model():
    def __init__(self):
        # print()
        pass

    @singledispatchmethod
    def LER_regular(self,keywords,text):
        # print(text,keywords,'type_none')
        pass

    @LER_regular.register
    def _(self,keywords:str,text:str):
        # print(text,keywords,'type,str')
        d = enchant.Dict("en_US")
        target_index_char = []
        target_ent_out = []
        re_str = r'' + keywords
        # value_ent = re.findall(re_str, text)
        pater = re.compile(re_str)
        target_text = re.findall(pater, text)
        # print(target_text)
        temp_data = []
        if len(target_text) != 0:
            target_index_begin = 0
            last_target_end = 0
            for i in target_text:
                v_t = str(i)
                count_target = text.count(v_t)
                for target_index in range(count_target):
                    # print(count_target)
                    if target_index == 0:
                        target_index_begin = text.index(v_t)
                    elif last_target_end < len(text):
                        # print(v_t,last_target_end,text)
                        target_index_begin = text.find(v_t, last_target_end, len(text))
                    left_side = target_index_begin
                    right_side = target_index_begin+len(keywords)
                    while left_side > 0:
                        if text[left_side] != " ":
                            left_side = left_side - 1
                        if text[left_side] == " ":
                            # if text[left_side-1] != '%':
                            break
                    while right_side < len(text):
                        if text[right_side] != " ":
                            right_side = right_side + 1
                        if right_side < len(text):
                            if text[right_side] == " ":
                                last_target_end = right_side
                                break

                    if left_side != 0:
                        left_side = left_side + 1
                    if ',' in text[left_side:right_side]:
                        right_side = right_side - 1
                    if text[right_side - 1] == '.':
                        right_side = right_side - 1
                    temp_data.append({
                        'name': text[left_side:right_side],
                        'char_idx': str(left_side) + ',' + str(right_side),
                    })
        temp_data = pd.DataFrame(temp_data)
        temp_data = temp_data.drop_duplicates()
        temp_data = np.array(temp_data)
        temp_data = temp_data.tolist()
        # print(temp_data)
        for i in temp_data:
            # print(i)
            if len(i[0]) > 0:
                print(i[0],keywords)
                if i[0] != keywords:
                    if d.check(i[0]) == False or re.search(r"\W",i[0])!= None:
                        target_ent_out.append({
                            'entity' : i[0],
                            'source_text':'',
                            'source_text_process':'',
                            'source_text_word_token':'',
                            'entity_char_index' : i[1],
                            'entity_token_index': 0,
                            'entity_type':0
                        })
                        target_index_char.append(i[1])
                else:
                    target_ent_out.append({
                        'entity': i[0],
                        'source_text': '',
                        'source_text_process': '',
                        'source_text_word_token': '',
                        'entity_char_index': i[1],
                        'entity_token_index': 0,
                        'entity_type': 0
                    })
                    target_index_char.append(i[1])
                # material_index_token.append(i[2])

        return target_ent_out,target_index_char

    # def _(self,keywords:str,text:str):
    #     # print(text,keywords,'type,str')
    #     target_index_char = []
    #     target_ent_out = []
    #     re_str = r'' + keywords
    #     # value_ent = re.findall(re_str, text)
    #     pater = re.compile(re_str)
    #     target_text = re.findall(pater, text)
    #     # print(target_text)
    #     temp_data = []
    #     if len(target_text) != 0:
    #         target_index_begin = 0
    #         last_target_end = 0
    #         for i in target_text:
    #             v_t = str(i)
    #             count_target = text.count(v_t)
    #             for target_index in range(count_target):
    #                 # print(count_target)
    #                 if target_index == 0:
    #                     target_index_begin = text.index(v_t)
    #                 elif last_target_end < len(text):
    #                     # print(v_t,last_target_end,text)
    #                     target_index_begin = text.find(v_t, last_target_end, len(text))
    #                 left_side = target_index_begin
    #                 right_side = target_index_begin+len(keywords)
    #                 while left_side > 0:
    #                     if text[left_side] != " ":
    #                         left_side = left_side - 1
    #                     if text[left_side] == " ":
    #                         # if text[left_side-1] != '%':
    #                         break
    #                 while right_side < len(text):
    #                     if text[right_side] != " ":
    #                         right_side = right_side + 1
    #                     if right_side < len(text):
    #                         if text[right_side] == " ":
    #                             last_target_end = right_side
    #                             break
    #
    #                 if left_side != 0:
    #                     left_side = left_side + 1
    #                 if ',' in text[left_side:right_side]:
    #                     right_side = right_side - 1
    #                 if text[right_side - 1] == '.':
    #                     right_side = right_side - 1
    #                 temp_data.append({
    #                     'name': text[left_side:right_side],
    #                     'char_idx': str(left_side) + ',' + str(right_side),
    #                 })
    #     temp_data = pd.DataFrame(temp_data)
    #     temp_data = temp_data.drop_duplicates()
    #     temp_data = np.array(temp_data)
    #     temp_data = temp_data.tolist()
    #     # print(temp_data)
    #     for i in temp_data:
    #         # print(i)
    #         if len(i[0]) > 0:
    #             target_ent_out.append({
    #                 'entity' : i[0],
    #                 'source_text':'',
    #                 'source_text_process':'',
    #                 'source_text_word_token':'',
    #                 'entity_char_index' : i[1],
    #                 'entity_token_index': 0,
    #                 'entity_type':0
    #             })
    #             target_index_char.append(i[1])
    #             # material_index_token.append(i[2])
    #     return target_ent_out,target_index_char

    @LER_regular.register
    def _(self,keywords:list,text:str):
        # print(text,keywords,'type_list')
        target_index_char = []
        target_ent_out = []
        temp_data = []
        relation_idxs = []
        relation_idx = 0
        for keyword_idx in range(len(keywords)):
            re_str = r'' + keywords[keyword_idx]
            # value_ent = re.findall(re_str, text)
            pater = re.compile(re_str)
            target_text = re.findall(pater, text)
            # print(target_text)
            if len(target_text) != 0:
                for i in target_text:
                    v_t = str(i)
                    count_target = text.count(v_t)
                    target_index_begin = 0
                    last_target_end = 0
                    for target_index in range(count_target):
                        if target_index == 0:
                            target_index_begin = text.index(v_t)
                        elif last_target_end < len(text):
                            # print(v_t,last_value_end,text)
                            target_index_begin = text.find(v_t, last_target_end, len(text))
                        left_side = target_index_begin
                        right_side = target_index_begin + len(keywords)
                        while left_side > 0:
                            if text[left_side] != " ":
                                left_side = left_side - 1
                            if text[left_side] == " ":
                                # if text[left_side-1] != '%':
                                break
                        while right_side < len(text):
                            if text[right_side] != " ":
                                right_side = right_side + 1
                            if right_side < len(text):
                                if text[right_side] == " ":
                                    last_target_end = right_side
                                    break

                        if left_side != 0:
                            left_side = left_side + 1
                        if ',' in text[left_side:right_side]:
                            right_side = right_side - 1
                        if text[right_side - 1] == '.':
                            right_side = right_side - 1
                        temp_data.append({
                            'name': text[left_side:right_side],
                            'char_idx': str(left_side) + ',' + str(right_side),
                            'type':keyword_idx
                        })

        # print(temp_data)
        temp_data = pd.DataFrame(temp_data)
        temp_data = temp_data.drop_duplicates()
        temp_data = np.array(temp_data)
        temp_data = temp_data.tolist()
        for i in temp_data:
            # print(i)
            if len(i[0]) > 0:
                target_ent_out.append({
                    'entity_1': i[0],
                    'entity_1_char_index': i[1],
                    'entity_1_token_index': 0,
                    'entity_type': i[2]
                })
                # target_ent_out.append(i[0])
                target_index_char.append(i[1])
                # material_index_token.append(i[2])
        return target_ent_out,target_index_char
