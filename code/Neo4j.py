import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher
import pymysql
import csv

connect = pymysql.connect(host="127.0.0.1",  
                              user="root",
                              password="123456",
                              db="test",
                              charset='utf8')  
cursor = connect.cursor()

sql1 = "select * from literature_entity"
sql2 = "select * from entity_relationship"

cursor.execute(sql1)
entity = cursor.fetchall()
cursor.execute(sql2)
relation = cursor.fetchall()
# print(relation)
connect.commit()  

#  ---------------------
cursor.close()  
connect.close() 

def write_data():

    storage_entity = []

    for i in entity:
        storage_entity.append({
            'id':i[0],
            'ent_name':i[2],
            'ent_type':i[3],

        })
   
    storage_entity = pd.DataFrame(storage_entity)
    return storage_entity
de = write_data() 

data1 = de[['id','ent_name']][de['ent_type'] == '材料实体']
data1.columns = ['ent_id','mat_name']
data1.shape
print(data1.shape)
mat_name = []
for i in range(0, len(data1)):
    mat_name.append(data1.iloc[i,1])
    mat_name = list(set(mat_name)) 
print(mat_name)

data2 = de[['id','ent_name']][de['ent_type'] == '性能']
data2.columns = ['ent_id','perf_name']
perf_name = []
for i in range(0, len(data2)):
    perf_name.append(data2.iloc[i,1])
    perf_name = list(set(perf_name))  
print(perf_name)

data3 = de[['id','ent_name']][de['ent_type'] == '性能值']
data3.columns = ['ent_id','perf_value']
perf_value = []
for i in range(0, len(data3)):
    perf_value.append(data3.iloc[i,1])
    perf_value = list(set(perf_value))  
print(perf_value)


graph = Graph("http://localhost:7474/", username="neo4j", password="123456", run="sub")

graph.delete_all()

graph.begin()

label_1 = '材料实体'
label_2 = '性能'
label_3 = '性能值'

def create_node(mat_name, perf_name,perf_value):
    for name in mat_name:
        node_1 = Node(label_1, name=name)
        graph.create(node_1)
    for name in perf_name:
        node_2 = Node(label_2, name=name)
        graph.create(node_2)
    for name in perf_value:
        node_3 = Node(label_3, name=name)
        graph.create(node_3)
create_node(mat_name, perf_name,perf_value)


def write_relation():

    storage_relation = []

    for i in relation:
        storage_relation.append({
            'relation_id':i[0],
            'ent_name_1':i[2],
            'ent_name_2':i[13],
            'relation_name': i[23],

        })
    
    storage_relation = pd.DataFrame(storage_relation)
    print(storage_relation)
    return storage_relation


dr = write_relation()


name1_list = []
name2_list = []
rel_list = []

for i in range(0, len(dr)):
    name1_list.append(dr.iloc[i, 1])  # 第一类label属性的节点
    rel_list.append(dr.iloc[i,3]) # 关系
    name2_list.append(dr.iloc[i, 2])



tuple_total = list(zip(name1_list,rel_list,name2_list))
tuple_total = list(set(tuple_total))
print(tuple_total)
matcher = NodeMatcher(graph)
for i in range(0, len(tuple_total)):
    name_1 = matcher.match(name=tuple_total[i][0]).first()
    rel = tuple_total[i][1]
    name_2 = matcher.match(name=tuple_total[i][2]).first()
    relationship = Relationship(name_1, rel, name_2)
    graph.create(relationship)


