import os.path

import pandas as pd
import json
from nltk.tokenize import sent_tokenize

from Material_Data_Miners.Words_Token_model.getLiteratureData import getLiteratureData
from Material_Data_Miners.Words_Token_model.LR_classifier import LR_classifier
from Material_Data_Miners.Words_Token_model.pdf_loader import load_pdf
from Material_Data_Miners.Words_Token_model.xml_loader import load_xml

# from getLiteratureData import getLiteratureData
# from LR_classifier import LR_classifier
# from pdf_loader import load_pdf

# getdata = getLiteratureData()
# lr_classifier = LR_classifier()


# ======================================================================================================================
#       老版本自定义关键词抽取代码
# ======================================================================================================================
# def df_to_dict_flag_1(df):
#     ret = {
#         "mat_entity": df['material_entity'],
#         "source_text": df['source_text'],
#         "line_num": df['line_num'],
#         "page_num": df['page_num']
#     }
#     return ret
#
#
# def df_to_dict_flag_2(df):
#     ret = {
#         "perf": df['relation_text'],
#         "perf_value": df['value_entity'],
#         "source_text": df['source_text'],
#         "line_num": df['line_num'],
#         "page_num": df['page_num']
#     }
#     return ret
#
#
# def df_to_dict_flag_3(df):
#     ret = {
#         "mat_entity": df['material_entity'],
#         "perf": df['relation_text'],
#         "perf_value": df['value_entity'],
#         "source_text": df['source_text'],
#         "line_num": df['line_num'],
#         "page_num": df['page_num']
#     }
#     return ret


# def get_keywords_flag(keywords: dict) -> int:
#     """判断关键词的成分。
#
#     Args:
#         keywords (dict): 关键词字典。
#             例子：
#                 {
#                     "material_entity": [
#                         {
#                             "describe": "铜",
#                             "entity": [
#                                 "copper",
#                                 "Cu"
#                             ]
#                         }
#                     ],
#                     "relation_entity": [
#                         {
#                             "describe": "拉伸强度",
#                             "entity": [
#                                 "ultimate tensile strength",
#                                 "Tensile strength",
#                                 "UTS",
#                                 "TS",
#                                 "tensile strength",
#                                 "Ultimate tensile strength"
#                             ],
#                             "unit_describe": "MPa",
#                             "unit_entity": [
#                                 "MPa",
#                                 " MPa",
#                                 " MPa",
#                                 " MPa"
#                             ]
#                         }
#                     ]
#                 }
#
#     Returns:
#         int: 记号变量
#             1 -> 表示只存在材料实体关键词
#             2 -> 表示只存在材料属性关键词
#             3 -> 表示即存在材料实体关键词又存在属性关键词
#     """
#     try:
#         if len(keywords['relation_entity']) == 0 and len(keywords['material_entity']) != 0:
#             return 1
#         if len(keywords['relation_entity']) != 0 and len(keywords['material_entity']) == 0:
#             return 2
#         if len(keywords['relation_entity']) > 0 and len(keywords['material_entity']) > 0:
#             return 3
#     except:
#         return 4


# def get_item_from_dict(keywords, entity):
#     ret = []
#     if entity == 'unit_entity':
#         for _item in keywords['relation_entity']:
#             ret.append(_item['unit_entity'])
#         return ret
#     for _item in keywords[entity]:
#         ret.append(_item['entity'])
#         return ret


# def get_Data_from_pdf_use_keywords(filename, keywords):
#     FLAG = get_keywords_flag(keywords)
#
#     MEDIA_ROOT = r'./media/'
#     file_path = MEDIA_ROOT + filename
#     # file_path = filename
#     ret_dict = []
#     pdf_data = load_pdf(file_path)
#     res = pd.DataFrame()
#
#     for index,row in pdf_data.iterrows():
#         paragraphs = row['text']
#
#         if FLAG == 1:
#             material_list = get_item_from_dict(keywords, 'material_entity')
#             for _material_entity in material_list:
#                 for _t in _material_entity:
#                     temp_data = get_Material_Data.getLiteratureData_words_token(paragraphs, _t)
#                     if len(temp_data) > 0:
#                         paragraphs['line_num'] = row['line_num']
#                         paragraphs['page_num'] = row['page_num']
#                         res = pd.concat([paragraphs, res])
#         elif FLAG == 2:
#             relation_list = get_item_from_dict(keywords, 'relation_entity')
#             unit_list = get_item_from_dict(keywords, 'unit_entity')
#             for i in range(len(relation_list)):
#                 for j in range(len(relation_list[i])):
#                     for k in range(len(unit_list[i])):
#                         temp_data = get_Material_Data.getLiteratureData_words_token(paragraphs, [relation_list[i][j], unit_list[i][k]])
#                         if len(temp_data) > 0:
#                             paragraphs['line_num'] = row['line_num']
#                             paragraphs['page_num'] = row['page_num']
#                             res = pd.concat([paragraphs, res])
#         else:
#             material_list = get_item_from_dict(keywords, 'material_entity')
#             relation_list = get_item_from_dict(keywords, 'relation_entity')
#             unit_list = get_item_from_dict(keywords, 'unit_entity')
#             # for i in range(len(relation_list)):
#             #     for j in range(len(material_list)):
#             #         for k in range(len(relation_list[i])):
#             #             for l in range(len(material_list[j])):
#             #                 _keywords = [material_list[j][l], relation_list[i][k], unit_list[i][k]]
#             #                 temp_data = get_Material_Data.getLiteratureData_words_token(paragraphs, _keywords)
#             #                 if len(temp_data) > 0:
#             #                     paragraphs['line_num'] = row['line_num']
#             #                     paragraphs['page_num'] = row['page_num']
#             #                     res = pd.concat([paragraphs, res])
#
#             # for i in range(len(relation_list)):
#             #     for j in range(len(relation_list[i])):
#             #         for k in range(len(material_list)):
#             #             for l in range(len(material_list[k])):
#             #                 for m in range(len(unit_list[i])):
#             #                     _keywords = [material_list[k][l], relation_list[i][j], unit_list[i][m]]
#             #                     temp_data = get_Material_Data.getLiteratureData_words_token(paragraphs, _keywords)
#             #                     if len(temp_data) > 0:
#             #                         temp_data['line_num'] = row['line_num']
#             #                         temp_data['page_num'] = row['page_num']
#             #                         res = pd.concat([temp_data, res])
#             for i in range(len(relation_list)):
#                 for j in range(len(material_list)):
#                     _flag = 0
#                     for k in range(len(relation_list[i])):
#                         if _flag == 1:
#                             break
#                         for l in range(len(material_list[j])):
#                             if _flag == 1:
#                                 break
#                             for m in range(len(unit_list[i])):
#                                 if _flag == 1:
#                                     break
#                                 _keywords = [material_list[j][l], relation_list[i][k], unit_list[i][m]]
#                                 temp_data = get_Material_Data.getLiteratureData_words_token(paragraphs, _keywords)
#                                 if len(temp_data) > 0:
#                                     _flag = 1
#                                     temp_data['line_num'] = row['line_num']
#                                     temp_data['page_num'] = row['page_num']
#                                     res = pd.concat([res, paragraphs])
#
#         # res.to_excel('ans.xlsx')
#         for index, row in res.iterrows():
#             if FLAG == 1:
#                 ret_dict.append(df_to_dict_flag_1(row))
#             elif FLAG == 2:
#                 ret_dict.append(df_to_dict_flag_2(row))
#             else:
#                 ret_dict.append(df_to_dict_flag_3(row))
#
#     return ret_dict
# ======================================================================================================================


def get_keywords_flag(keywords):
    """判断用户是否传入关键词

    :param keywords:
    :return: 1-> 用户传入了关键词
             2-> 用户未传入关键词
    """
    if keywords:
        return 1
    else:
        return 2


def df_to_dict(df):
    ret = {
        "ent_name": df['entity'],
        "ent_type": df['entity_type'],
        "source_text": df['source_text'],
        "line_num": df['line_num'],
        "page_num": df['page_num'],
        "entity_char_index": df["entity_char_index"],
        "entity_token_index": df["entity_token_index"],
        "keywords": df["keywords"]
    }
    return ret


def text_df_to_dict(df):
    ret = {
        "ent_name": df['entity'],
        "ent_type": df['entity_type'],
        "source_text": df['source_text'],
        "entity_char_index": df["entity_char_index"],
        "entity_token_index": df["entity_token_index"],
        "keywords": df["keywords"]
    }
    return ret

def relation_reduce(rel_dict):
    ret = []
    for i in rel_dict:
        temp = {}
        temp = {
            "ent_1": i["ent_1"]["entity"],
            "ent_2": i["ent_2"]["entity"],
            "relation_name": i['rel_name']
        }
        ret.append(temp)
    return ret

def get_Data_from_pdf_use_keywords(filename, keywords):
    FLAG = get_keywords_flag(keywords)
    MEDIA_ROOT = r'./media/'
    file_path = MEDIA_ROOT + filename
    # file_path = filename
    relation_list = []
    entity_list = []
    res_df = pd.DataFrame()
    ret_dict = {}
    file_type = os.path.splitext(file_path)
    if file_type[1] == '.xml':
        pdf_data = load_xml(file_path)
    else:
        pdf_data = load_pdf(file_path)

    # if FLAG == 1:
    for index, row in pdf_data.iterrows():
        getdata = getLiteratureData()
        lr_classifier = LR_classifier()
        paragraphs = row['text']
        sent_tokenize_list = sent_tokenize(paragraphs)
        for sents in sent_tokenize_list:
            temp_data = getdata.getLiteratureData_words_token(sents, keywords)
            if len(temp_data) > 0:
                temp_data["line_num"] = row['line_num']
                temp_data['page_num'] = row['page_num']
                empty_df = pd.DataFrame()

                relation_data = lr_classifier.classfiy_data_by_ioc(temp_data, empty_df)
                res_df = pd.concat([res_df, temp_data])

                if len(relation_data) > 0:
                        relation_list = relation_list + relation_data

    for index, row in res_df.iterrows():
        entity_list.append(df_to_dict(row))

    ret_dict = {
        "entity": entity_list,

        "relation": relation_list
    }
    return ret_dict


def get_entity_data(filename, keywords):
    MEDIA_ROOT = r'./media/'
    file_path = MEDIA_ROOT + filename
    res_df = pd.DataFrame()
    file_type = os.path.splitext(file_path)
    if file_type[1] == '.xml':
        pdf_data = load_xml(file_path)
    else:
        pdf_data = load_pdf(file_path)

    for index, row in pdf_data.iterrows():
        getdata = getLiteratureData()
        paragraphs = row['text']
        sent_tokenize_list = sent_tokenize(paragraphs)
        for sents in sent_tokenize_list:
            temp_data = getdata.getLiteratureData_words_token(sents, keywords)
            if len(temp_data) > 0:
                temp_data["line_num"] = row['line_num']
                temp_data['page_num'] = row['page_num']
                res_df = pd.concat([res_df, temp_data])

    return res_df


def get_relation_data(new_entity, old_entity):
    lr_classifier = LR_classifier()
    relation_list = []
    relation_data = lr_classifier.classfiy_data_by_ioc(new_entity, old_entity)

    if len(relation_data) > 0:

        relation_list = relation_list + relation_data
    return relation_list







def get_Data_from_text_use_keywords(text, keywords):
    FLAG = get_keywords_flag(keywords)
    relation_list = []
    entity_list = []
    res_df = pd.DataFrame()
    ret_dict = {}

    if FLAG == 1:
        getdata = getLiteratureData()
        lr_classifier = LR_classifier()
        sent_tokenize_list = sent_tokenize(text)
        for sents in sent_tokenize_list:
            temp_data = getdata.getLiteratureData_words_token(sents, keywords)
            if len(temp_data) > 0:
                relation_data = lr_classifier.classfiy_data_by_ioc(new_entity=temp_data, old_entity=None)
                res_df = pd.concat([res_df, temp_data])
                if len(relation_data) > 0:
                    for i in relation_data:
                        for j in i:
                            relation_list.append(j)

    else:
        getdata = getLiteratureData()
        lr_classifier = LR_classifier()
        sent_tokenize_list = sent_tokenize(text)
        for sents in sent_tokenize_list:
            temp_data = getdata.getLiteratureData_words_token(sents)

            if len(temp_data) > 0:
                relation_data = lr_classifier.classfiy_data_by_ioc(temp_data)
                res_df = pd.concat([res_df, temp_data])
                if len(relation_data) > 0:
                    for i in relation_data:
                        for j in i:
                            relation_list.append(j)
    for index, row in res_df.iterrows():
        entity_list.append(text_df_to_dict(row))

    ret_dict = {
        "entity": entity_list,
        "relation": relation_list
    }
    return ret_dict