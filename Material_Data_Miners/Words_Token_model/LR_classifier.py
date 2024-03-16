import pandas as pd
import itertools
class LR_classifier():
    def __init__(self):
        # print()
        pass

    def classfiy_data_by_ioc(self,new_entity,old_entity):

        out_data = []
        group_data_new = pd.DataFrame()
        if old_entity.empty == False:
            temp = new_entity.append(old_entity,ignore_index=True)
            temp = temp.drop_duplicates(subset='entity', ignore_index=True)
            group_data_new = self.group_data_by_type(temp)

        else:
            temp = new_entity.drop_duplicates(subset='entity', ignore_index=True)
            group_data_new = self.group_data_by_type(temp)
        if len(group_data_new) > 2:
            if len(group_data_new[0]) * len(group_data_new[1]) == len(group_data_new[2]):
                out_data = self.logical_classifiy(group_data_new)
            else:
                if len(group_data_new[0]) == 1 :
                    out_data = self.greedy_classifiy(group_data_new)
                if len(group_data_new[0]) > 1 :
                    out_data = self.shortest_classifiy(group_data_new)
        elif len(group_data_new) == 2:
            out_data = self.full_connection_classfiy(group_data_new[0], group_data_new[1])
        else:
            out_data = []

        return out_data

    def group_data_by_type(self,data):

        temp_data = []
        for i in range(len(data['entity_type'].unique())):
            temp_data.append(
                {
                    'entities': [],
                    'type': data['entity_type'].unique()[i]
                }
            )
        for index, row in data.iterrows():
            for j in temp_data:
                if row['entity_type'] == j['type']:
                    j['entities'].append(row.to_dict())
        group_data = []
        for i in temp_data:
            group_data.append(
                pd.DataFrame(i['entities'])
            )
        out_data = []

        temp_out_data = []
        perf = []
        mat = []
        value = []
        for i in group_data:
            if i.iloc[0]['entity_type'] == 'MAT':
                mat = (i.sort_values(by='entity_token_index', ascending=True,ignore_index=True))

            if i.iloc[0]['entity_type'] == 'Perf':
                perf = (i.sort_values(by='entity_token_index', ascending=True,ignore_index=True))

            if i.iloc[0]['entity_type'] == 'value':
                value = (i.sort_values(by='entity_token_index', ascending=True,ignore_index=True))

        if len(mat) > 0:
            temp_out_data.append(mat)
        if len(perf) > 0:
            temp_out_data.append(perf)
        if len(value)> 0:
            temp_out_data.append(value)

        return temp_out_data

    def check_pos(self,pref_data,value_data):
        pref_loc = []
        value_loc = []
        for i,r in pref_data.iterrows():
            pref_loc.append(r['entity_token_index'])
        for i,r in value_data.iterrows():
            value_loc.append(r['entity_token_index'])
        # print(pref_loc)
        # print(value_loc)
        for i in value_loc:
            for j in pref_loc:
                if j > i:
                    return True

        return False

    def full_connection_classfiy(self,data_1,data_2,type=1):

        temp_list = []

        if type == 0:
            for index in range(len(data_1)):
                for index_ in range(len(data_2)):
                    temp_list.append({
                        'ent_1': data_2.loc[index_].to_dict(),
                        'ent_2': data_1.loc[index].to_dict(),
                        'rel_name': data_2.loc[index_]['entity_type'] + '-' + data_1.loc[index]['entity_type']
                    })
        if type == 1:
            for index in range(len(data_1)):
                for index_ in range(len(data_2)):
                    temp_list.append({
                        'ent_1': data_1.loc[index].to_dict(),
                        'ent_2': data_2.loc[index_].to_dict(),
                        'rel_name': data_1.loc[index]['entity_type'] + '-' + data_2.loc[index_]['entity_type']
                    })

        return temp_list
    def cross_(self,data_1,data_2):
        temp_list = []
        data_1_temp = pd.DataFrame()
        for i in range(int(len(data_2)/len(data_1))):
            data_1_temp = data_1_temp.append(data_1, ignore_index=True)
        data_1_temp = data_1_temp.sort_values(by='entity_token_index',ignore_index=True)
        for index, row in data_2.iterrows():
            temp_list.append({
                'ent_1': '',
                'ent_2': data_2.loc[index].to_dict(),
                'rel_name': '<TAG>' + '-' + data_2.loc[index]['entity_type']
            })
        for index in range(len(data_1_temp)):
            temp_list[index]['ent_1'] = data_1_temp.loc[index].to_dict()
            temp_list[index]['rel_name'] = temp_list[index]['rel_name'].replace('<TAG>',data_1_temp.loc[index]['entity_type'])
        return temp_list
    def link_(self,data_1,data_2):
        temp_list = []
        for index_ in range(0, len(data_2), len(data_1)):
            for index in range(len(data_1)):
                temp_list.append({
                    'ent_1': data_1.loc[index].to_dict(),
                    'ent_2': data_2.loc[index_+index].to_dict(),
                    'rel_name': data_1.loc[index]['entity_type'] + '-' + data_2.loc[index_+index]['entity_type']
                })
                # print(i, j + i)
        return temp_list

    def shortest_classifiy(self,data):
        print()
        out_data = []
        pref_data = pd.DataFrame()
        value_data = pd.DataFrame()
        out_data = []

        temp = self.full_connection_classfiy(data[0], data[2])
        temp_1 = pd.DataFrame(temp)
        temp_1['distance'] = 0
        for i,r in temp_1.iterrows():
            r['distance'] = abs(r['ent_1']['entity_token_index'] - r['ent_2']['entity_token_index'])
            print(r)
        out_data_2 = []
        temp_1 = temp_1.sort_values(by='distance',ignore_index=True)
        if len(data[0])<len(data[2]):
            for index in range(len(data[0])):
                out_data_2.append({
                    'ent_1':temp_1.iloc[index]['ent_1'],
                    'ent_2': temp_1.iloc[index]['ent_2'],
                    'rel_name': temp_1.iloc[index]['rel_name'],
                })
        else:
            for index in range(len(data[2])):
                out_data_2.append({
                    'ent_1': temp_1.iloc[index]['ent_1'],
                    'ent_2': temp_1.iloc[index]['ent_2'],
                    'rel_name': temp_1.iloc[index]['rel_name'],
                })
        temp = self.full_connection_classfiy(data[1], data[2])
        out_data_3 = []
        for index in range(len(out_data_2)):
            if temp[index]['ent_2']['entity'] == out_data_2[index]['ent_2']['entity']:
                out_data_3.append(temp[index])
        out_data = []
        temp = self.full_connection_classfiy(data[0], data[1])
        out_data_1 = []
        for index in range(len(out_data_2)):
            if temp[index]['ent_1']['entity'] == out_data_2[index]['ent_1']['entity']:
                out_data_1.append(temp[index])
        for i in out_data_1:
            out_data.append(i)
        for i in out_data_2:
            out_data.append(i)
        for i in out_data_3:
            out_data.append(i)
        return out_data

    def greedy_classifiy(self,data):
        print()
        out_data = []
        out_data_1 = self.cross_(data[0], data[1])
        out_data_2 = self.cross_(data[1], data[2])
        out_data_3 = self.cross_(data[0], data[2])
        for i in out_data_1:
            out_data.append(i)
        for i in out_data_2:
            out_data.append(i)
        for i in out_data_3:
            out_data.append(i)
        return out_data

    def logical_classifiy(self,data):
        pref_data = pd.DataFrame()
        value_data = pd.DataFrame()
        out_data = []
        for i in data:
            # print(i.loc[0])
            if i.loc[0]['entity_type'] == 'Perf':
                pref_data = i
            if i.loc[0]['entity_type'] == 'value':
                value_data = i

        if self.check_pos(pref_data, value_data) == True:
            print('True')
            out_data_1 = self.full_connection_classfiy(data[1], data[0],type=0)
            out_data_2 = self.link_(data[0], data[2])
            out_data_3 = self.cross_(data[1],data[2])
            for i in out_data_1:
                out_data.append(i)
            for i in out_data_2:
                out_data.append(i)
            for i in out_data_3:
                out_data.append(i)
        else:
            out_data_1 = self.full_connection_classfiy(data[0], data[1],type=1)
            out_data_2 = self.cross_(data[0],data[2])
            out_data_3 = self.link_(data[1], data[2])
            for i in out_data_1:
                out_data.append(i)
            for i in out_data_2:
                out_data.append(i)
            for i in out_data_3:
                out_data.append(i)

        return out_data

