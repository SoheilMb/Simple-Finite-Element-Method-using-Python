import numpy as np



def Area_OK(x1,x2,x3,y1,y2,y3):
    if 0.5*(((x2-x1)*(y3-y1))-((x3-x1)*(y2-y1)))>0:
        return True
    else: return False
    
def CmpElMtx(xy):
    '''
xy= the coordinates of the nodes of the triangle in a fashion like:
[x1,y1,x2,y2,x3,y3]
    x1, y1, x2, y2, x3, y3 = tri[0][0], tri[0][1], tri[1][0], tri[1][1], tri[2][0], tri[2][1]
    s1=[(x3-x2),(y3-y2)]
    s2=[(x1-x3),(y1-y3)]
    s3=[(x2-x1),(y2-y1)]
    

    Atot=(0.5 * (((x1-x3)*(y2-y1))-((y1-y3)*(x2-x1))))
    '''
    x1,y1,x2,y2,x3,y3=xy[0],xy[1],xy[2],xy[3],xy[4],xy[5]
    #print(xy)
    Ae=np.zeros((3,3))
   
    Atot=(0.5 * (((x1-x3)*(y2-y1))-((y1-y3)*(x2-x1))))
    # The function Area_OK checks if the area is negative
    if Area_OK (x1,x2,x3,y1,y2,y3) is False:
        x3,y3,x2,y2,x1,y1=xy[0],xy[1],xy[2],xy[3],xy[4],xy[5]
        if Area_OK (x1,x2,x3,y1,y2,y3) is False:
            print('The nodes of the element given in wrong order')
        else:
            Atot=(0.5 * (((x1-x3)*(y2-y1))-((y1-y3)*(x2-x1))))

    #Compute the gradient of the vectors
            
    grad_phi1e=np.array([-(y3-y2),(x3-x2)])/(2*Atot)
    grad_phi2e=np.array([-(y1-y3),(x1-x3)])/(2*Atot)
    grad_phi3e=np.array([-(y2-y1),(x2-x1)])/(2*Atot)

    grad_phi=[grad_phi1e,grad_phi2e,grad_phi3e]
    # Compute all the integrals for this particular element
    for iIdx in range(0,3):
        for jIdx in range(0,3):
            # example:
            #Ae[0,0]=grad_phi[0]*grad_phi[0]*Atot
            #Ae[0,0]=[(-(y3-y2))*(-(y3-y2))+(x3-x2)*(x3-x2)]*Atot
            step1=grad_phi[iIdx]*grad_phi[jIdx]
            
            Ae[iIdx][jIdx]=(step1[0]+step1[1])*Atot

    return Ae


'''            
         
grad_phi1e=np.array([-(5-3),(2-2)])/(2*1)
grad_phi2e=np.array([-(6-3),(4-2)])/(2*1)
grad_phi3e=np.array([-(8-4),(2-0)])/(2*1)
grad_phi=[grad_phi1e,grad_phi2e,grad_phi3e]
#print(grad_phi[1])


grad_phi=np.array([[-0.8333,0.8333],[-0.1389,-1.5278],[0.9722,0.6944]])
step1=(grad_phi[1]*grad_phi[1])
#print(step1)
step2=step1[0]+step1[1]
print(step2)

'''
xy=[1,4,3,6,5,5]
#print(CmpElMtx(xy).reshape((1,9))[0])
