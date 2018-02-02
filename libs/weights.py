import maya.cmds as mc
def setWeight(node, weight, map=None): 
    '''
    import rigrepo.libs.shape
    import rigrepo.libs.weights
    reload(rigrepo.libs.weights)
    import maya.cmds as mc
    sc = 'skinCluster2'
    
    for joint in mc.ls('joint?'):
        mc.move( 0, 1, 0, joint, r=1) 
        deltas = rigrepo.libs.shape.pointDelta('pCylinder1_noDeformation', 'pCylinder1_wireDeformed')
        mc.move( 0, -1, 0, joint, r=1) 
        rigrepo.libs.weights.setWeight(sc, deltas, map=joint) 
    '''
 
    if mc.nodeType(node) == 'skinCluster': 
        # find the inf index 
        inf = map
        inf_index = str() 
        con = mc.listConnections(inf+'.worldMatrix[0]', p=1, d=1, s=0) 
        for c in con: 
            if node+'.matrix' in c: 
                inf_index = c.split('[')[1][:-1] 
         
        n = 0 
        for w in weight: 
            pnt_index = str(w[0]) 
            val = w[1] 
            mc.setAttr(node+'.wl['+pnt_index+'].w['+inf_index+']', val) 

    if mc.nodeType(node) == 'cluster': 
        for w in weight: 
            pnt_index = w[0] 
            val = w[1] 
            mc.setAttr(node+'.wl[0].w['+pnt_index+']', val) 
 
