import snap


fbgraph=snap.LoadEdgeList(snap.PUNGraph,"facebook_combined.txt", 0, 1)
n=fbgraph.GetNodes()


close_list=[]
for node in fbgraph.Nodes():
	NId=node.GetId()
	closeness_snap=snap.GetClosenessCentr(fbgraph,NId,True,False)        		#Standard function for closeness centrality
	templist=[]
	templist.append(NId)
	templist.append(closeness_snap)
	close_list.append(templist)

close_list.sort(key = lambda x: x[1], reverse=True)

closeness_overlap=0

closenessfile=open("centralities/closeness.txt","r")

for i in range(0,100):
	line=closenessfile.readline()
	for j in range(0,len(line)):
		if line[j]==' ':
			val=line[:j]
			break
	#Checking for overlaps
	for k in range(0,100):
		if(int(close_list[k][0])==int(val)):
			closeness_overlap+=1
			break

closenessfile.close()

#Check Betweenness overlap

NodeC = snap.TIntFltH()
EdgeC = snap.TIntPrFltH()
snap.GetBetweennessCentr(fbgraph, NodeC, EdgeC, 0.8, False)						#Standard function for betweenness
NodeC.SortByDat(False)


BHash_top=snap.TIntH()


i=0
b_overlap=0
betweennessfile=open("centralities/betweenness.txt","r")

for j in NodeC:
	BHash_top[i]=j
	i+=1
	if(i==100):
		break

#Extracting top100 NodeIds in a separate hash table
for i in range(0,100):
	line=betweennessfile.readline()
	for j in range(0,len(line)):
		if line[j]==' ':
			val=line[:j]
			break
	for i in BHash_top:
		if(int(val)==BHash_top[i]):
			b_overlap+=1

betweennessfile.close()


#Check PageRankOverlap


PRHash=snap.TIntFltH()
PRHash_top=snap.TIntH()
snap.GetPageRank(fbgraph,PRHash,0.8)							#Standard function for PageRank
PRHash.SortByDat(False)
i=0
pr_overlap=0
pagerankfile=open("centralities/pagerank.txt","r")

#Extracting top100 NodeIds in a separate hash table
for j in PRHash:
	PRHash_top[i]=j
	i+=1
	if(i==100):
		break

#Checking for overlaps
for i in range(0,100):
	line=pagerankfile.readline()
	for j in range(0,len(line)):
		if line[j]==' ':
			val=line[:j]
			break
	for i in PRHash_top:
		if(int(val)==PRHash_top[i]):
			pr_overlap+=1

pagerankfile.close()

print("#overlaps for Closeness Centrality:",closeness_overlap)
print("#overlaps for Betweenness Centrality:",b_overlap)
print("#overlaps for PageRank Centrality:",pr_overlap)