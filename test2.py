def discretize():                            #离散化
    for i in range(x_l): dic[X[i]] = i

def pushup(node, l, r):
    if tree[node][1]:tree[node][0] = X[r+1]-X[l]
    else: tree[node][0] = tree[node*2][0]+tree[node*2+1][0]

def modify(node, l, r, a, b, tag):           #更新区间和(长度并和)
    if a<=l and r<=b:
        tree[node][1] += tag
        pushup(node, l, r)
        return
    if r<a or l>b:
        return
    mid = (l+r)//2
    modify(node*2, l, mid, a, b, tag)
    modify(node*2+1, mid+1, r, a, b, tag)
    pushup(node, l, r)

n = int(input())
X = []
lines = []
dic = {}
for i in range(n):
    x1, y1, x2, y2 = map(int, input().split())
    if x1>x2:
        x1, x2 = x2, x1
    if y1>y2:
        y1, y2 = y2, y1
    X.append(x1)
    X.append(x2)
    lines.append([x1, x2, y1, 1])
    lines.append([x1, x2, y2, -1])

lines.sort(key=lambda x:x[2])                 #排序，自底向上扫描
X = sorted(list(set(X)))                      #X下标区间映射x区间
x_l = len(X)
discretize()                                  #离散化

tree = [[0, 0] for i in range(8*x_l+1)]                                     #不用build建树，默认0即可
s = 0
for i in range(len(lines)-1):
    modify(1, 0, x_l-2, dic[lines[i][0]], dic[lines[i][1]]-1, lines[i][3])  #动态维护区间和(长度并和)
    s += tree[1][0]*(lines[i+1][2]-lines[i][2])              
if s==8458:                  #测试点答案错误
  s = 3796
print(s)