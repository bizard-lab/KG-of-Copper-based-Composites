import pandas as pd

from Material_Data_Miners.Words_Token_model.getMaterialData import getMaterialData
from Material_Data_Miners.Words_Token_model.pdf_loader import load_pdf



get_Material_Data = getMaterialData()

def get_Material_Data_from_pdf(filename):
    MEDIA_ROOT = r'./media/'
    file_path = MEDIA_ROOT + filename

    ret_dict = []
    pdf_data = load_pdf(file_path)
    res = pd.DataFrame()

    for index,row in pdf_data.iterrows():
        paragraphs = row['text']

        paragraphs = get_Material_Data.getMaterialData_words_token(paragraphs)
        paragraphs = get_Material_Data.classfily_data(paragraphs)
        if len(paragraphs) > 0:
            paragraphs['line_num'] = row['line_num']
            paragraphs['page_num'] = row['page_num']
            res = pd.concat([paragraphs, res])

    for index,row in res.iterrows():
         ret_dict.append(pdf_df_to_dict(row))

    return ret_dict


def df_to_dict(df):
    ret = {
        "mat_entity": df['material_entity'].values[0],
        "perf": df['relation_text'].values[0],
        "perf_value": df['value_entity'].values[0],
        "source_text": df['source_text'].values[0],
    }
    return ret

def pdf_df_to_dict(df):
    # print(type(df))
    ret = {
        "mat_entity": df['material_entity'],
        "perf": df['relation_text'],
        "perf_value": df['value_entity'],
        "source_text": df['source_text'],
        "line_num": df['line_num'],
        "page_num": df['page_num']
    }
    return ret


def get_Material_Data_from_string(text):
    data = get_Material_Data.getMaterialData_words_token(text)
    data = get_Material_Data.classfily_data(data)
    ret = df_to_dict(data)
    return ret



