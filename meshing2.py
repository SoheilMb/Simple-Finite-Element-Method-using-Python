from __future__ import division
from __future__ import absolute_import

import meshpy.triangle as triangle
import numpy as np
import numpy.linalg as la
from six.moves import range
import matplotlib.pyplot as pt
import pandas as pd

def round_trip_connect(start, end):
    return [(i, i+1) for i in range(start, end)] + [(end, start)]


'''
points = [(100,400),
          (400,400),
          (400,280),
          (320,270), 
          (320,160), 
          (120,160), 
          (120,250), 
          (100,250)]
'''
'''
points = [(0,400),
          (400,400),
          (400,0),
          (200,0),
          #(200,200),
          (190,30),
          (175,60),
          (155,90),
          (135,120),
          (110,150),
          (85,170),
          (60,190),
          (45,195),
          (0,200)
          ]
'''
points = [(0,400),
          (400,400),
          (400,0),
          (200,0),
          #(200,200),
          (195,25),
          (185,50),
          (170,75),
          
          (135,125),
          (110,150),
          (70,175),
        
          (0,200)
          ]


facets = round_trip_connect(0, len(points)-1)

circ_start = len(points)
points.extend(( 3*np.cos(angle), 3 * np.sin(angle)) for angle in np.linspace(0, 2*np.pi, 30, endpoint=False))

facets.extend(round_trip_connect(circ_start, len(points)-1))


def needs_refinement(vertices, area):
    bary = np.sum(np.array(vertices), axis=0)/3
    max_area = 5 + (la.norm(bary, np.inf)-1)*5
    return bool(area > max_area)
    

info = triangle.MeshInfo()
info.set_points(points)
info.set_holes([(0, 0)])
info.set_facets(facets)

mesh = triangle.build(info, refinement_func=needs_refinement)

mesh_points = np.array(mesh.points)
mesh_tris = np.array(mesh.elements)

pt.triplot(mesh_points[:, 0], mesh_points[:, 1], mesh_tris)
print (mesh_points)



print("------------------------------------------")
print(mesh_tris)


pt.show()
'''
with open ("points.txt",'w') as myfile:
    for point in mesh_points:
        myfile.write(str(point)+"\n")
'''

all_elements=np.array([])


for item in mesh_tris:
    elem=np.array([])
    for p in item:
        #print(p)
        #print(mesh_points[int(p)])
        #all_elements=np.append(all_elements,
        elem=np.append(elem,mesh_points[p])
    all_elements=np.append(all_elements,elem)



all_elements=all_elements.reshape(150,6)


print("print(all_elements):\n ",all_elements)
'''
The resulting file will contain the coordinates of all triangles in
such fashion : [x1,y1,x2,y2,x3,y3]
'''
'''
with open ("elements.txt",'w') as myfile:
    for triangle in all_elements:
        myfile.write(str(triangle)+'\n')
    #myfile.write('\n')
        #print(triangle)


all_elements=all_elements.reshape(900,1)
count=0
with open ("elements2.txt",'w') as myfile:
    while count<900:
        for t in range(6) :
            myfile.write(str(all_elements[count]))
            count+=1
        myfile.write('\n')
        #print(triangle)
'''  
  
import pandas as pd

elems=pd.DataFrame(columns=['x1','y1','x2','y2','x3','y3'])

count=0
all_elements=all_elements.reshape(150,6)

for triangle in all_elements:
    #print(triangle)
    elems.loc[count]=triangle
    count+=1
    
elems.to_csv('xy.csv')        

      

xes=np.array([])
yes=np.array([])
elems=pd.DataFrame(columns=['x','y'])
for p in range(len(mesh_points)):
    xes=np.append(xes,mesh_points[p][0])
    yes=np.append(yes,mesh_points[p][1])


print("len yes:",len(yes)," ",yes)
print("len yes:",len(xes)," ", xes)
elems['x']=xes
elems['y']=yes
    
    
elems.to_csv('xy2.csv')   

print(mesh_tris)
tris= pd.DataFrame(columns=['Node1','Node2','Node3'])
count=0
for item in mesh_tris:
    tris.loc[count]=item
    count+=1

tris.to_csv("Nodenums.csv")

#print(len(tris))

#print(tris.shape)



columns=[i for i in range(1,151)]
tris=pd.DataFrame(columns=columns)
count=0
for i in range(len(mesh_tris)):
    tris[i+1]=mesh_tris[i]
    

#tris.to_csv("Nodenumsmatlab.csv")

print(len(tris))

print(tris.shape)



noExtcoor=np.array([])
noExt=np.array([])
noIntcoor=np.array([])
noInt=np.array([])



noExt=set()

noInt=set()

print("----------------Part 2 ---------------")

noExtcoor2=[]

noIntcoor2=[]


for el in mesh_tris:
    for node in el:
        
        if mesh_points[node][0]==0 and list(mesh_points[node]) not in noExtcoor2:
           
           #noExtcoor.update(tuple(mesh_points[node]))
           #print("coors: ", mesh_points[node], "node: ", node)
           noExtcoor2.append(list(mesh_points[node]))
           noExt.add(node)
           noExtcoor=np.append(noExtcoor,mesh_points[node])
        elif mesh_points[node][1]==0 and list(mesh_points[node]) not in noIntcoor2 :
            
            
           # print("coors: ", mesh_points[node], "node: ", node)
            noIntcoor2.append(list(mesh_points[node]))
            noIntcoor=np.append(noIntcoor,mesh_points[node])
            
            noInt.add(node)
            




print("\nnoExtcoor2: ", noExtcoor2)


print("\n noExt: ",noExt)


print("\n noIntcoor: ",noIntcoor)


print("\n noIntcoor2: ",noIntcoor2)


print("\n noInt: ",noInt)


print("len(noIntcoor)",len(noIntcoor))


print(len(noInt))


print(len(noExtcoor))

print(type(noExt))

Int_and_ext_no=pd.DataFrame(columns=["noInt","noExt"])


noInt=list(noInt)
noExt=list(noExt)

      
while len(noInt)<len(noExt):
     noInt.append(1000)

Int_and_ext_no["noInt"]=sorted(list(noInt))

Int_and_ext_no["noExt"]=sorted(list(noExt))


Int_and_ext_no.to_csv("noInt_and _ext.csv")

ess_nodes=[]
to_add=[list(noExt),list(noInt)]
for ls in to_add:
    for node in ls:
        ess_nodes.append(node)

print(ess_nodes)
    
ess_nodes_coords=[]
to_add=[list(noExtcoor2),list(noIntcoor2)]
for ls in to_add:
    for node in ls:
        ess_nodes_coords.append(node)

print(ess_nodes_coords)


essential_and_natural_no=pd.DataFrame(columns=["no_ess","no_nat"])





all_nodes=set()
for el in mesh_tris:
    for node in el:
        all_nodes.add(node)


nat_nodes=set()
for item in sorted(all_nodes):
    if item not in sorted(ess_nodes):
        nat_nodes.add(item)


nat_nodes=list(nat_nodes)
while len(ess_nodes)<len(nat_nodes):
    ess_nodes.append(1000)
essential_and_natural_no["no_nat"]=sorted(list(nat_nodes))


essential_and_natural_no["no_ess"]=sorted(ess_nodes)
        
print(ess_nodes)

print(essential_and_natural_no.head())

essential_and_natural_no.to_csv("ess_and_nat_nodes.csv")

