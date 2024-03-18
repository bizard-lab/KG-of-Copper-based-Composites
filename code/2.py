class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
def AddRelationShip(root, ans1, ans2):
    if root:
        if root.left and root.val == ans2:
            temp = root.left
            root.left = ans1
            ans1.left = temp
        elif root.right and root.val == ans2:
            temp = root.right
            root.right = ans1
            ans1.right = temp
        AddRelationShip(root.left, ans1, ans2)
        AddRelationShip(root.right, ans1, ans2)
def GetGeneration(root, ans1, ans2, count):
    if root and (root.val == ans1 or root.val == ans2):
        count += 1
        GetGeneration(root.left, ans1, ans2, count)
        GetGeneration(root.right, ans1, ans2, count)
    return count
def GetCousin(root, ans1, ans2, count, count1, count2):
    if root:
        count += 1
        if root.val == ans1:
            count1 = count
        elif root.val == ans2:
            count2 = count
        GetCousin(root.left, ans1, ans2, count, count1, count2)
        GetCousin(root.right, ans1, ans2, count, count1, count2)
    if count == -1:
        return -1
    else:
        return abs(count1-count2)
root = TreeNode()
n = int(input())
str_n = []
for i in range(n):
    ans = input().split(' ')
    str_n.append(ans)
for str1 in str_n:
    if str1[0] == 'AddRelationShip':
        AddRelationShip(root, str1[1], str1[2])

    elif str1[0] == 'GetGeneration':
        res = GetGeneration(root, str1[1], str1[2], -1)
        print(res)
    elif str1[0] == 'GetCousin':
        res = GetCousin(root, str1[1], str1[2], -1, 0, 0)
        print(res)
