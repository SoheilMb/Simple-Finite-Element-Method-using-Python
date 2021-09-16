import CmpElMtx_function as Cmp
import pathlib
import math
import numpy as np
import pandas as pd
import random

#Physical constants
pi=math.pi
mu0=4*pi*1E-7  #Permeability in vacuum
c0= 299792456  #Speed of light in vacuum
eps0 = 1/(mu0*c0*c0) #Permittivity in vacuum

#Voltage between inner and outer conductor
U=1
#Read the grid from the corresponding files
no2xy= pd.read_csv("xy.csv")
el2no= pd.read_csv("Nodenums.csv")


#Get number of nodes

noNum=len(no2xy)

#Get number of elements
elNum=len(el2no)


#Scale the domain to measure 2cm x 2cm.
#The initial mesh fitted the unit square:
# -1 < x < 1 and -1 < y < 1.

#Assemble the matrix A and vector b.
Number_of_nodes=90
A=np.zeros((Number_of_nodes,Number_of_nodes)) 


print(A.shape)
b=(np.array([0 for i in range (noNum)])).reshape(noNum,1)


for elIdx in range(1,elNum):
    #Get the nodes and their coordinates
    #for the element ’elIdx’.
    no=np.array(el2no.loc[elIdx-1])[1:]
    xy=[no2xy.loc[elIdx-1]]
    xy=np.array(xy[0][1:])
    #print(xy.reshape(6,1))
    #Compute the element matrix and add the contribution to the global matrix
    A_el=Cmp.CmpElMtx(xy)
    
    
    #A=add_to_global(A,A_el,no)
    A[np.ix_(no,no)]+=A_el


print(A.shape)

essential_and_natural_no=pd.read_csv("ess_and_nat_nodes.csv")
    

no_nat= essential_and_natural_no["no_nat"]
no_nat=np.asarray(no_nat)

essential_and_natural_no = essential_and_natural_no[essential_and_natural_no.no_ess != 1000]
no_ess= essential_and_natural_no["no_ess"]
no_ess=np.asarray(no_ess)



Int_Ext_no=pd.read_csv("noInt_and _ext.csv")


noExt= Int_Ext_no["noExt"]
noExt=np.asarray(noExt)


Int_Ext_no = Int_Ext_no[Int_Ext_no.noInt != 1000]
noInt= Int_Ext_no["noInt"]
noInt=np.asarray(noInt)


#Pick out the parts of the matrix and the vectors
#needed to solve the problem


'''
A_ess
'''

A_ess=np.matrix([])
A_ess=A[np.ix_(no_nat,no_ess)]




'''
A_nat
'''
A_nat=np.array([])
A_nat=A[np.ix_(no_nat,no_nat)]

'''
Using ix_ one can quickly construct index arrays that will index the cross product. a[np.ix_([1,3],[2,5])] returns
the array [[a[1,2] a[1,5]], [a[3,2] a[3,5]]].
'''


'''
b
'''
b=b[np.ix_(no_nat)]

    



no_all=[i for i in range(0,Number_of_nodes)]
'''
z
'''
z=(np.array([0 for i in range (len(no_all))])).reshape(len(no_all),1)


'''
z(noInt)
'''

z[np.ix_(noInt)]=U*np.ones((len(noInt),1))



'''
z_ess
'''

z_ess=np.array([])
z_ess=z[np.ix_(no_ess)]


'''
Solve the system of linear equations.
"solve the linear system A*x = B (for x)"

Matrix multiply between A_ess and z_ess (np.dot)
'''

inv_A = np.linalg.inv(A_nat)
B=b-((A_ess)@(z_ess))
z_nat=inv_A.dot(B)

print("znat",z_nat ,"len z_nat",len(z_nat) )
'''
# Build up the total solution
'''
z=(np.array([0 for i in range (len(no_all))])).reshape(len(no_all),1)
z=np.asarray(z,dtype=np.float32)
z[np.ix_(no_ess)]=z_ess
z[np.ix_(no_nat)]=z_nat
print("z:",z)

'''
Compute the capacitance.
'''
W=0.5*eps0*(((z.transpose()).dot(A)).dot(z))

print(W)

'''
C = 2*W/U^2;

'''

C=2*W/U**2
print("C per unit length [pF/m]"+str(C/1e-12))



print("z shape",z.shape)

tr=np.array([])

for item in z:
   
    
    tr=np.append(tr,item[0])
    


print("len tr:",len(tr))


print(tr)

import matplotlib.pyplot as plt
import matplotlib.tri as tri

# converts quad elements into tri elements
def quads_to_tris(quads):
    tris = [[None for j in range(3)] for i in range(2*len(quads))]
    for i in range(len(quads)):
        j = 2*i
        n0 = quads[i][0]
        n1 = quads[i][1]
        n2 = quads[i][2]
        n3 = quads[i][3]
        tris[j][0] = n0
        tris[j][1] = n1
        tris[j][2] = n2
        tris[j + 1][0] = n2
        tris[j + 1][1] = n3
        tris[j + 1][2] = n0
    return tris

# plots a finite element mesh
def plot_fem_mesh(nodes_x, nodes_y, elements):
    for element in elements:
        x = [nodes_x[element[i]] for i in range(len(element))]
        y = [nodes_y[element[i]] for i in range(len(element))]
        plt.fill(x, y, edgecolor='black', fill=False)


elements_tris=[]
# FEM data
no2xy2= pd.read_csv("xy2.csv")
el2no2= pd.read_csv("Nodenums.csv")

print(el2no2.head())
for idx in range(len(el2no2)):
    elements_tris.append(list(el2no2.loc[idx])[1:])
    
nodes_x = np.array([no2xy2['x']])[0]
print("len x",len(nodes_x))

nodes_y = np.array([no2xy2['y']])[0]

print(len(nodes_y))
'''
nodal_values = []
for i in range(len(nodes_x)):
        r=random.uniform(0, 1)
        nodal_values.append(r)
'''
nodal_values=[]

nodal_values=tr      
#elements_tris = [[2, 6, 5], [5, 6, 10], [10, 9, 5]]
#elements_quads = [[0, 1, 4, 3], [1, 2, 5, 4], [3, 4, 8, 7], [4, 5, 9, 8]]
elements = elements_tris #+ elements_quads

# convert all elements into triangles
elements_all_tris = elements_tris# + quads_to_tris(elements_quads)

# create an unstructured triangular grid instance
triangulation = tri.Triangulation(nodes_x, nodes_y, elements_all_tris)

# plot the finite element mesh
plot_fem_mesh(nodes_x, nodes_y, elements)

# plot the contours
plt.tricontourf(triangulation, nodal_values,cmap=plt.cm.get_cmap('viridis', 6))#'RdBu',,'Blues'

# show







plt.colorbar(label='φ[V]')
#φ
plt.axis('equal')


plt.show()



from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#plt.trisurf(triangulation, nodal_values,cmap=plt.cm.get_cmap('Blues', 6))#'RdBu',,'Blues'

# show


#surf=ax.plot_trisurf(nodes_x, nodes_y, nodal_values)

surf=ax.plot_trisurf(triangulation, nodal_values,cmap=plt.cm.get_cmap('winter', 6))


fig.colorbar(surf)

'''
ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.zaxis.set_major_locator(MaxNLocator(5))
'''
fig.tight_layout()
plt.show()





