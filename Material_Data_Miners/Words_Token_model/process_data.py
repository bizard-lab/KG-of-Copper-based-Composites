class process_data():
    def replace_space(self, data, relation_re_list):
        # print(data)
        data = data.replace(" ", "").replace(" ", "").replace(" ", " ")
        data = data.replace(" wt.% ", "wt.%").replace(" wt% ", "wt%").replace(" wt% ", "wt%").replace("wt.%",
                                                                                                      "wt%").replace(
            "wt.% ", "wt%")
        data = data.replace("at.% ", "at.%")
        data = data.replace("vol.% ", "vol%").replace("vol% ", "vol%").replace(" vol%", "vol%")
        data = data.replace(" wt%", "wt%")
        for relations in relation_re_list:
            re_list = relations['value_re_list']
            for i in re_list:
                data = data.replace(" " + i, i)
        data = data.replace(" × ", "×")
        data = data.replace(" /", "/")
        data = data.replace("(m·K)", "mK")
        data = data.replace("m·K", "mK")
        data = data.replace(" ± ", "±")
        data = data.replace("% IACS", "%IACS")
        data = data.replace(",", " ,")
        data = data.replace(" + ", "+")
        return data

    def easy_classify_mne_value(self, data):
        # print(data)
        temp = data
        for index, row in temp.iterrows():
            value_entity = row['value_entity']
            material_entity = row['material_entity']
            if len(material_entity.split("[SEP]")) == 1 and len(value_entity.split(",")) == 1:

                continue
            else:

                temp.loc[index, 'easy_to_classify'] = 1
        return temp
