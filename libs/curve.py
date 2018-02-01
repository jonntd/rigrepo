
import maya.cmds as mc

def createCurveFromPoints(points, degree=3, name='curve'):
        '''
        docstring
        '''
        knotList = [0]
        if degree == 1:
            knotList.extend(range(len(points))[1:])
            print knotList
        elif degree == 2:
            knotList.extend(range(len(points) - 1))
            knotList.append(knotList[-1]) 
            print knotList
        elif degree == 3:
            knotList.append(0) 
            knotList.extend(range(len(points) - 2))
            knotList.extend([knotList[-1],knotList[-1]]) 
        
        curve = mc.curve(name=name, p=points,k=knotList,degree=degree)
        
        return curve