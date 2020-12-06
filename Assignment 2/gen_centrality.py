import snap
from collections import deque

fbgraph=snap.LoadEdgeList(snap.PUNGraph,"facebook_combined.txt", 0, 1)

#Calculating closeness centrality
n=fbgraph.GetNodes()
closenessfile=open("centralities/closeness.txt","a+")

closeness_list=[]

#iterating over all nodes
for node in fbgraph.Nodes():
	farness=0													#First finding the farness of node
	NId=node.GetId()
	ID_shortestdist=snap.TIntH()
	shortpath=snap.GetShortPath(fbgraph,NId,ID_shortestdist)
	for i in ID_shortestdist:
		farness+=ID_shortestdist[i]
	closeness=(n-1)/(farness)									#Normalised closeness
	templist=[]
	templist.append(NId)
	templist.append(closeness)
	closeness_list.append(templist)

closeness_list.sort(key = lambda x: x[1], reverse=True) 		#Sorting by descending closeness score

for i in closeness_list:
	line=str(i[0])+str(" ")+str(round(i[1],6))+"\n"
	closenessfile.write(line)

closenessfile.close()



#Betweeenness Centrality

#Brande's algorithm- gets the Betweenness Centrality measures in a graph


betweennness_list=snap.TIntFltH()


#Initializing betweenness values
for i in range(0,4039):
	betweennness_list[i]=0


#Brandes Algorithm for Betweenness Centrality
#iterating over all nodes
for node in fbgraph.Nodes():
	S=[]
	P=dict((w.GetId(),[]) for w in fbgraph.Nodes())						#Storing shortest paths				
	g=dict((t.GetId(),0) for t in fbgraph.Nodes())				
	g[node.GetId()]=1
	d=dict((t.GetId(),-1) for t in fbgraph.Nodes()) 
	d[node.GetId()]=0
	Q=deque([])
	Q.append(node.GetId())
	while Q:
		v=Q.popleft()
		S.append(v)
		v_iter=fbgraph.GetNI(v)
		for w in v_iter.GetOutEdges():
			if d[w] < 0:
				Q.append(w)
				d[w]=d[v] + 1
			if d[w]==d[v]+1:
				g[w]=g[w]+g[v]
				P[w].append(v)
	e=dict((v.GetId(),0) for v in fbgraph.Nodes())
	while S:
		w= S.pop()
		for v in P[w]:
			e[v] = e[v] + (g[v]/g[w])*(1+e[w])
		if(w!=node.GetId()):
			betweennness_list[w]=betweennness_list[w]+e[w]

#Normalising betweenness values
for i in betweennness_list:
	betweennness_list[i]=(2/((n-1)*(n-2)))*betweennness_list[i]


betweennness_list.SortByDat(False)										#Sorting by value

betweennessfile=open("centralities/betweenness.txt","a+")

for i in betweennness_list:
	line=str(i)+str(" ")+str(round(betweennness_list[i],6))+"\n"
	betweennessfile.write(line)

betweennessfile.close()




#PageRank:

d=[0 for i in range(0,4039)]

x=1/1010															#total number of nodes in biased preference vector
pr=snap.TIntFltH()                                                  #using a hash table to store PageRank values

for node in fbgraph.Nodes():
	NId=node.GetId()
	if(NId%4==0):
		d[NId]=x
		pr[NId]=x
	else:
		d[NId]=0
		pr[NId]=0

for j in range(0,100):
	for node in fbgraph.Nodes():
		t=0
		NId=node.GetId()
		for Id in node.GetOutEdges():
			Id_iter=fbgraph.GetNI(Id)
			t+=pr[Id]/(Id_iter.GetOutDeg())
		pr[NId]=0.8*t+0.2*d[NId]
	sum=0
	for i in pr:
		sum+=pr[i]
	for i in pr:
		pr[i]=pr[i]/sum

pr.SortByDat(False)
pagerankfile=open("centralities/pagerank.txt","a+")
for i in pr:
	line=str(i)+str(" ")+str(round(pr[i],6))+"\n"
	pagerankfile.write(line)

pagerankfile.close()
