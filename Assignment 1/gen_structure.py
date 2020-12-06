import snap
import sys

Rnd = snap.TRnd(42)
Rnd.Randomize()


#Please specify file paths for facebook and amazon graphs here
facebookgraph="/home/yash/Programs/socomp2020/facebook_combined.txt"
amazongraph="/home/yash/Programs/socomp2020/com-amazon.ungraph.txt"

NIdV=snap.TIntV();
fbsg=snap.LoadEdgeList(snap.PUNGraph, facebookgraph, 0, 1)
for node in fbsg.Nodes():
	if node.GetId()%5==0:
		NIdV.Add(node.GetId())
snap.DelNodes(fbsg,NIdV)
snap.SaveEdgeList(fbsg,'facebook.elist')

NIdV2=snap.TIntV();
azsg=snap.LoadEdgeList(snap.PUNGraph, amazongraph, 0, 1)
for node in azsg.Nodes():
	if (node.GetId()%4)!=0:
		NIdV2.Add(node.GetId())
snap.DelNodes(azsg,NIdV2)
snap.SaveEdgeList(azsg,'amazon.elist')



subgraph_name=sys.argv[1]

fbsgel=snap.LoadEdgeList(snap.PUNGraph, subgraph_name, 0, 1)
MaxDegVfb=[]
#Q1
#a
fbnn=fbsgel.GetNodes();
print("Number of nodes:",fbnn)
#b
fben=fbsgel.GetEdges();
print("Number of edges:",fben)
#Q2
#a
print("Number of nodes with degree=7:",snap.CntDegNodes(fbsgel,7))
#b
max_deg_fb_id=snap.GetMxDegNId(fbsgel)
NI=fbsgel.GetNI(max_deg_fb_id)
max_deg_fb=NI.GetDeg()
for NI in fbsgel.Nodes():
	if(NI.GetDeg()==max_deg_fb):
		MaxDegVfb.append(NI.GetId())
MaxDegNodeString=','.join(map(str,MaxDegVfb))
print("Node id(s) with highest degree:", MaxDegNodeString)
#c
snap.PlotOutDegDistr(fbsgel, "deg_dist_"+str(subgraph_name), "deg_dist_"+str(subgraph_name))
#Q3
#a
i=10;
average=0.0
variance=0.0
while(i<=1000):
	diam=snap.GetBfsFullDiam(fbsgel, i, False)
	print("Approximate full diameter by sampling",i,"nodes:",round(diam,4))
	i*=10;
	average+=diam
	variance+=(diam*diam)
average/=3
variance=(variance/3)-average*average
print("Approximate full diameter(mean and variance): %0.4f,%0.4f"%(average,variance))
#b
i=10
average=0.0
variance=0.0
while(i<=1000):
	diam=snap.GetBfsEffDiam(fbsgel, i, False)
	print("Approximate effective diameter by sampling",i,"nodes:",round(diam,4))
	i*=10;
	average+=diam
	variance+=(diam*diam)
average/=3
variance=(variance/3)-average*average
print("Approximate effective diameter(mean and variance): %0.4f,%0.4f"%(average,variance))
#c Plot
snap.PlotShortPathDistr(fbsgel, "shortest_path_"+str(subgraph_name), "shortest_path_"+str(subgraph_name))

#Q4
#a
print("Fraction of nodes in largest connected component:",round(snap.GetMxSccSz(fbsgel),4))
#b
EdgeBridgeV=snap.TIntPrV();
snap.GetEdgeBridges(fbsgel,EdgeBridgeV)
print("Number of edge bridges:",len(EdgeBridgeV))
#c
ArtNIdV=snap.TIntV();
snap.GetArtPoints(fbsgel,ArtNIdV);
print("Number of articulation points:",len(ArtNIdV))
#d Plot
snap.PlotSccDistr(fbsgel, "connected_comp_"+str(subgraph_name),"connected_comp_"+str(subgraph_name))

#Q5
#a
print("Average clustering coefficient:",round(snap.GetClustCf(fbsgel,-1),4))
#b
print("Number of triads:",snap.GetTriads(fbsgel,-1))
#c
RnId=fbsgel.GetRndNId(Rnd)
print("Clustering coefficient of random node "+str(RnId)+":",round(snap.GetNodeClustCf(fbsgel, RnId),4))
#d
print("Number of triads random node "+str(RnId)+" participates:",snap.GetNodeTriads(fbsgel, RnId))
#e
print("Number of edges that participate in at least one triad:",snap.GetTriadEdges(fbsgel,-1))
#f Plot
snap.PlotClustCf(fbsgel, "clustering_coeff_"+str(subgraph_name), "clustering_coeff_"+str(subgraph_name))
