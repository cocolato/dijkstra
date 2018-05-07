import requests,re
# dijkstra算法实现，有向图和路由的源点作为函数的输入，最短路径最为输出
def dijkstra(graph,src):
    # 判断图是否为空，如果为空直接退出
    if graph is None:
        return None
    nodes = [i for i in range(len(graph))]  # 获取图中的所有节点
    visited=[]   # 表示已经路由到最短路径的节点集合
    if src in nodes:    #如果该节点未被标记
        visited.append(src)     #标记该节点
        nodes.remove(src)
    else:
        return None
    distance={src:0}  # 记录源节点到各个节点的距离
    for i in nodes:
        distance[i]=graph[src][i]  # 初始化
    path = {src: {src: []}}  # 记录源节点到每个节点的路径
    print(path, distance)
    k=pre=src
    while nodes:
        mid_distance=float('inf')
        for v in visited:
            for d in nodes:
                new_distance = graph[src][v]+graph[v][d]
                if new_distance < mid_distance:
                    mid_distance=new_distance
                    graph[src][d]=new_distance  # 进行距离更新
                    k=d
                    pre=v
        distance[k]=mid_distance  # 最短路径
        path[src][k]=[i for i in path[src][pre]]
        path[src][k].append(k)
        # 更新两个节点集合
        visited.append(k)
        nodes.remove(k)
        print(visited,nodes)  # 输出节点的添加过程
    return distance,path

#创建字典存储点位信息
graph_list=[]
#创建列表存储距离/时间信息
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}

x=input("请输入点位数目:")
x=int(x)
a={}
for i in range(1,x+1):
    m=i
    a[i]=input("请输入点位"+str(m)+":")#循环输入点位


print(a)

for i in range(1,x+1):
    list = []#列表存储中间的距离/时间
    for m in range(1,x+1):
        url1= "http://restapi.amap.com/v3/place/text?key=35fc3e2f362fa1eeec425f4468f2452b&keywords=" + a[i] \
           + "&types=&city=成都&children=1&offset=1&page=1&extensions=all"
        data1 = requests.get(url1, headers=head)
        data1.encoding = 'utf-8'
        data1 = data1.text
        pat1 = 'location":"(.*?),(.*?)",".*?ddress'
        result1 = re.findall(pat1, data1)

        url2 = "http://restapi.amap.com/v3/place/text?key=35fc3e2f362fa1eeec425f4468f2452b&keywords=" + a[m]\
           + "&types=&city=成都&children=1&offset=1&page=1&extensions=all"
        data2 = requests.get(url2, headers=head)
        data2.encoding = 'utf-8'
        data2 = data2.text
        result2 = re.findall(pat1, data2)

        url3 = "http://restapi.amap.com/v3/distance?key=35fc3e2f362fa1eeec425f4468f2452b&origins=" +\
               str(result1[0][0]) + "," + str(result1[0][1]) + "&destination=" + str(result2[0][0]) + "," +\
               str(result2[0][1])+"&type=1"
        #print(url3)
        data3 = requests.get(url3, headers=head)
        data3.encoding = 'utf-8'
        data3 = data3.text
        #print(data3)
        pat2 = "distance\":\"(.*?)\",\"duration\":\"(.*?)\""
        result3 = re.findall(pat2, data3)
        #print(result3[0][0])
        #获得两个节点的距离/时间信息
        list.append(int(result3[0][0]))

    graph_list.append(list)
    #将所有的距离/时间信息存储到列表中

distance,path= dijkstra(graph_list, 0)  # 查找从源点0开始带其他节点的最短路径
print(distance,path)#输出最短距离和行驶路线

time=0
print("最终路径：")  #输出最优的路线内容
for key in path[0]:
    print(a[key+1],end='')
    time+=1
    if time<x:
        print("到",end='')

