str1 = input().split(',')
str1_arr, res_dict = list(), dict()
count, temp = 1,  []
for s in str1:
    if count == 3:
        count = 1
        s = float(s)
        temp.append(s)
        str1_arr.append(temp)
        temp = []
        continue
    temp.append(s)
    count += 1
for arr1 in str1_arr:
    res_dict[arr1[1]] = res_dict.get(arr1[1], 0) + arr1[2]
new_res_dict = sorted(res_dict.items(), key=lambda x: x[1], reverse=True)
print(new_res_dict)
str1_arr.sort(key=lambda x: (x[1], x[2]))
print(str1_arr)

day = 1
while str1_arr and count < len(str1_arr):
    count = 0
    sum1 = 0
    print('Day'+str(day)+':')
    while sum1 <= 8:
        sum1 += str1_arr[count][2]
        res = str1_arr.pop(0)
        print(res)
    day += 1

# 'conference1','A',1.5,'conference'2,''B,1,'conference'3,'A',2.5