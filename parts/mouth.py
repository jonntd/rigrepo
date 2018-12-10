'''
This is the base module for all of your parts.
'''
import numpy
import os
import maya.cmds as mc
import rigrepo.libs.attribute as attribute
import rigrepo.libs.bindmesh as bindmesh
import rigrepo.libs.control as control
import rigrepo.libs.common as common
import rigrepo.parts.part as part
import rigrepo.libs.data.node_data as node_data
import rigrepo.libs.weights 

class Mouth(part.Part):
    '''
    '''
    def __init__(self, name, lipMainCurve="lip_main_curve", lipCurve="lip_curve", dataObj=None):
        '''
        This is the constructor for the base part
        :param name: Name of the part you are creating.
        :type name: str

        :param jointList: Name of the part you are creating.
        :type jointList: str

        :param name: Name of the part you are creating.
        :type name: str
        '''
        super(Mouth, self).__init__(name, dataObj=dataObj)

        self.addAttribute("lipMainCurve", lipMainCurve, attrType=str) 
        self.addAttribute("lipCurve", lipCurve, attrType=str)
        self.addAttribute("systemParent", self.name, attrType=str)      
        self.addAttribute("geometry", "body_geo", attrType=str)
        self.addAttribute("headPin", "face_mid_bind", attrType=str)
        self.addAttribute("jawPin", "jaw_bind", attrType=str)
        self.addAttribute("orientFile", "", attrType=str)

    def build(self):
        '''
        This will build the rig.
        '''
        super(Mouth, self).build()
        lipMainCurve = self.getAttributeByName('lipMainCurve').getValue()
        lipCurve = self.getAttributeByName('lipCurve').getValue()
        parentGroup = self.getAttributeByName('systemParent').getValue()
        geometry = self.getAttributeByName('geometry').getValue()
        headPinTrs = self.getAttributeByName('headPin').getValue()
        jawPinTrs = self.getAttributeByName('jawPin').getValue()
        orientFile = self.getAttributeByName('orientFile').getValue()
        
        bindmeshGeometry, follicleList, lipMainControlHieracrchyList, jointList = self.__buildCurveRig(lipMainCurve, "lip_main" , parentGroup)
        # delete the controls, tparent joint to the node above the control
        mainBaseCurveJointList = list()
        for jnt, lipMainControlList in zip(jointList, lipMainControlHieracrchyList):
            # create the joint that we will use later to deform the base wire.
            baseCurveJoint = mc.joint(name=jnt.replace("_jnt","_baseCurve_jnt"))
            mainBaseCurveJointList.append(baseCurveJoint)
            # hide the base curve joint. Then parent it under the null node
            mc.setAttr("{}.v".format(baseCurveJoint), 0)
            mc.parent(baseCurveJoint, lipMainControlList[1])
            mc.setAttr("{}.t".format(baseCurveJoint), 0, 0, 0)
            mc.parent(jnt,lipMainControlList[-2])
            mc.delete(lipMainControlList.pop(-1))

        # create a bindMesh for mouth corner controls.
        jointListPos = [mc.xform(joint, q=True, ws=True, t=True) for joint in jointList]
        jointListPosX = [round(pos[0], 3) for pos in jointListPos]
        cornerPos = [jointListPos[jointListPosX.index(max(jointListPosX))],
                     jointListPos[jointListPosX.index(min(jointListPosX))]]

        # create the bindmesh 
        bindmeshGeometry, follicleList = bindmesh.create("{}_corner".format(self.name), cornerPos)
        # set the visibility of the bindmesh
        mc.setAttr("{}.v".format(bindmeshGeometry), 0 )
        mouthCorner_l_follicle = mc.rename(follicleList[0], follicleList[0].replace('_0_','_l_'))
        mouthCorner_r_follicle = mc.rename(follicleList[1], follicleList[1].replace('_1_','_r_'))
        mc.parent([mouthCorner_l_follicle, mouthCorner_r_follicle, bindmeshGeometry], self.name)

        controlPrefix = "lip_main"
        # get the position of the controls for lip tweakers
        upperLeft = list()
        upperLeftPosXList = list()
        upperRight = list()
        upperRightPosXList = list()
        lowerLeft = list()
        lowerLeftPosXList = list()
        lowerRight = list()
        lowerRightPosXList = list()
        mouthCornerLeftPosY = round(mc.xform(mouthCorner_l_follicle, q=True, ws=True, t=True)[1], 3)
        mouthCornerRightPosY = round(mc.xform(mouthCorner_r_follicle, q=True, ws=True, t=True)[1], 3)
        for controlHieracrchy in lipMainControlHieracrchyList:
            #position of control
            controlPosition = mc.xform(controlHieracrchy[0], q=True, ws=True, t=True)
            posX = round(controlPosition[0], 3)
            posY = round(controlPosition[1], 3)
            if posX > .001:
                if round(abs(posY-mouthCornerLeftPosY),3) <.003:
                    lipMainControlHieracrchyList[lipMainControlHieracrchyList.index(controlHieracrchy)] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lipMain_corner_l")) for ctrl in controlHieracrchy]
                elif posY > mouthCornerLeftPosY:
                    upperLeft.append(controlHieracrchy)
                    upperLeftPosXList.append(posY)
                elif posY < mouthCornerLeftPosY:
                    lowerLeft.append(controlHieracrchy)
                    lowerLeftPosXList.append(posY)

            elif posX < -.001:
                if round(abs(posY-mouthCornerLeftPosY),3) <.003:
                    lipMainControlHieracrchyList[lipMainControlHieracrchyList.index(controlHieracrchy)] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lipMain_corner_r")) for ctrl in controlHieracrchy]
                elif posY > mouthCornerRightPosY:
                    upperRight.append(controlHieracrchy)
                    upperRightPosXList.append(posY)
                elif posY < mouthCornerRightPosY:
                    lowerRight.append(controlHieracrchy)
                    lowerRightPosXList.append(posY)
            else:
                if posY > mouthCornerLeftPosY:
                    lipMainControlHieracrchyList[lipMainControlHieracrchyList.index(controlHieracrchy)] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lipMain_center_up")) for ctrl in controlHieracrchy]
                elif posY < mouthCornerLeftPosY:
                    lipMainControlHieracrchyList[lipMainControlHieracrchyList.index(controlHieracrchy)] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lipMain_center_low")) for ctrl in controlHieracrchy]
        # reorder controls
        upperLeftPosXListCopy = list(upperLeftPosXList)
        upperLeftPosXList.sort()
        # rename the controls for left and right.
        for i, pos in enumerate(upperLeftPosXListCopy):
            # rename the center controls.
            lipMainControlHieracrchyList[lipMainControlHieracrchyList.index(upperLeft[i])] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lipMain_up_{}_l".format(upperLeftPosXList.index(pos)))) for ctrl in upperLeft[i]]

        # reorder controls
        upperRightPosXListCopy = list(upperRightPosXList)
        upperRightPosXList.sort()
        # rename the controls for left and right.
        for i, pos in enumerate(upperRightPosXListCopy):
            # rename the center controls.
           lipMainControlHieracrchyList[lipMainControlHieracrchyList.index(upperRight[i])] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lipMain_up_{}_r".format(upperRightPosXList.index(pos)))) for ctrl in upperRight[i]]

        # reorder controls
        lowerLeftPosXListCopy = list(lowerLeftPosXList)
        lowerLeftPosXList.sort()
        lowerLeftPosXList.reverse()
        # rename the controls for left and right.
        for i, pos in enumerate(lowerLeftPosXListCopy):
            # rename the center controls.
            lipMainControlHieracrchyList[lipMainControlHieracrchyList.index(lowerLeft[i])] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lipMain_low_{}_l".format(lowerLeftPosXList.index(pos)))) for ctrl in lowerLeft[i]]

        # reorder controls
        lowerRightPosXListCopy = list(lowerRightPosXList)
        lowerRightPosXList.sort()
        lowerRightPosXList.reverse()
        # rename the controls for left and right.
        for i, pos in enumerate(lowerRightPosXListCopy):
            # rename the center controls.
            lipMainControlHieracrchyList[lipMainControlHieracrchyList.index(lowerRight[i])] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lipMain_low_{}_r".format(lowerRightPosXList.index(pos)))) for ctrl in lowerRight[i]]


        # create the controls
        # If there is a hierarchy argument passed in. We will loop through and create the hiearchy.
        # move the orients
        nodeDataObj = None
        if os.path.isfile(orientFile):
            nodeDataObj = node_data.NodeData()
            nodeDataObj.read(orientFile)

        for follicle in (mouthCorner_l_follicle, mouthCorner_r_follicle):
            parent = follicle
            controlName = follicle.split("_follicle")[0]
            # create the control with a large enough hierarchy to create proper SDK's
            ctrlHierarchy = control.create(name=controlName, 
                controlType="square", 
                hierarchy=['nul','ort', 'auto'], 
                color=common.BLACK,
                parent=parent)
            driverMouthCorner = mc.createNode("joint", name="{}_driver".format(controlName))
            # mover the driver to the orient and parent it under the orient
            mc.parent(driverMouthCorner, ctrlHierarchy[1])
            #mc.xform(driverMouthCorner, ws=True, matrix=mc.xform(ctrlHierarchy[1], q=True, ws=True, matrix=True))
            
            # turn off the visibility of the driver
            mc.setAttr("{}.drawStyle".format(driverMouthCorner), 2)
            # turn on the handle for the mouth corner control and move it 
            mc.setAttr("{}.displayHandle".format(ctrlHierarchy[-1]), 1)
            mc.setAttr("{}.selectHandleX".format(ctrlHierarchy[-1]) ,0.2)
            # zero out the mouth corner hierarchy so it's in the correct position.
            mc.setAttr("{}.translate".format(ctrlHierarchy[0]), 0,0,0)
            #mc.setAttr("{}.rotate".format(ctrlHierarchy[0]), 0,0,0)
            mc.delete(mc.listRelatives(ctrlHierarchy[-1], c=True, shapes=True)[0])

            # create the drivers for the lip_L/R
            neutral = mc.createNode("transform", name="{}_neutral".format(controlName))
            headPin = mc.createNode("transform", name="{}_headPin".format(controlName))
            jawPin = mc.createNode("transform", name="{}_jawPin".format(controlName))

            for pinGrp in [neutral, headPin, jawPin]:
                mc.xform(pinGrp, ws=True, matrix=mc.xform(ctrlHierarchy[1], q=True, ws=True, matrix=True))
                mc.parent(pinGrp, ctrlHierarchy[1])
                cst = mc.parentConstraint(pinGrp, ctrlHierarchy[2])[0]

            # constrain the driver to the control
            mc.pointConstraint(ctrlHierarchy[-1], driverMouthCorner, mo=True)

            if nodeDataObj:
                nodeDataObj.applyData([ctrlHierarchy[1]])

            # constrain the head and jaw pinning.
            mc.parentConstraint(jawPinTrs, jawPin, mo=True)
            mc.parentConstraint(headPinTrs, headPin, mo=True)

            # create the head and jaw pinning.
            mc.addAttr(controlName, ln="pinning", nn="----------", at="enum", enumName="Pinning", keyable=True)
            attribute.lock(controlName, "pinning")
            mc.addAttr(controlName, ln="pin", at="double", min=-10, max=10, dv=0, keyable=True)
            mc.setDrivenKeyframe("{}.{}W0".format(cst,neutral), 
                cd="{}.pin".format(controlName), v=1, dv=0)
            mc.setDrivenKeyframe("{}.{}W1".format(cst,headPin), 
                cd="{}.pin".format(controlName), v=0, dv=0)
            mc.setDrivenKeyframe("{}.{}W2".format(cst,jawPin), 
                cd="{}.pin".format(controlName), v=0, dv=0)
            mc.setDrivenKeyframe("{}.{}W0".format(cst,neutral), 
                cd="{}.pin".format(controlName), v=0, dv=-10)
            mc.setDrivenKeyframe("{}.{}W1".format(cst,headPin), 
                cd="{}.pin".format(controlName), v=0, dv=-10)
            mc.setDrivenKeyframe("{}.{}W2".format(cst,jawPin), 
                cd="{}.pin".format(controlName), v=1, dv=-10)
            mc.setDrivenKeyframe("{}.{}W0".format(cst,neutral), 
                cd="{}.pin".format(controlName), v=0, dv=10)
            mc.setDrivenKeyframe("{}.{}W1".format(cst,headPin), 
                cd="{}.pin".format(controlName), v=1, dv=10)
            mc.setDrivenKeyframe("{}.{}W2".format(cst,jawPin), 
                cd="{}.pin".format(controlName), v=0, dv=10)

            # create the set driven keyframes
            for attr in ['x','y','z']:
                for lipMainControl in lipMainControlHieracrchyList:
                    if "_l_" in lipMainControl[3] and follicle == mouthCorner_l_follicle:
                        mc.setDrivenKeyframe("{}.t{}".format(lipMainControl[3],attr), 
                            cd="{}.t{}".format(driverMouthCorner,attr), v=0, dv=0)
                        mc.setDrivenKeyframe("{}.t{}".format(lipMainControl[3],attr), 
                            cd="{}.t{}".format(driverMouthCorner,attr), v=1, dv=1)
                        mc.setDrivenKeyframe("{}.t{}".format(lipMainControl[3],attr), 
                            cd="{}.t{}".format(driverMouthCorner,attr), v=-1, dv=-1)
                        if attr == "x":
                            mc.setDrivenKeyframe("{}.ry".format(lipMainControl[2]), 
                                cd="{}.t{}".format(driverMouthCorner,attr), v=0, dv=0)
                            mc.setDrivenKeyframe("{}.ry".format(lipMainControl[2]), 
                                cd="{}.t{}".format(driverMouthCorner,attr), v=10, dv=1)
                            mc.setDrivenKeyframe("{}.ry".format(lipMainControl[2]), 
                                cd="{}.t{}".format(driverMouthCorner,attr), v=-10, dv=-1)
                    elif  "_r_" in lipMainControl[3] and follicle == mouthCorner_r_follicle:
                        mc.setDrivenKeyframe("{}.t{}".format(lipMainControl[3],attr), 
                            cd="{}.t{}".format(driverMouthCorner,attr), v=0, dv=0)
                        mc.setDrivenKeyframe("{}.t{}".format(lipMainControl[3],attr), 
                            cd="{}.t{}".format(driverMouthCorner,attr), v=1, dv=1)
                        mc.setDrivenKeyframe("{}.t{}".format(lipMainControl[3],attr), 
                            cd="{}.t{}".format(driverMouthCorner,attr), v=-1, dv=-1)
                        if attr == "x":
                            mc.setDrivenKeyframe("{}.ry".format(lipMainControl[2]), 
                                cd="{}.t{}".format(driverMouthCorner,attr), v=0, dv=0)
                            mc.setDrivenKeyframe("{}.ry".format(lipMainControl[2]), 
                                cd="{}.t{}".format(driverMouthCorner,attr), v=10, dv=1)
                            mc.setDrivenKeyframe("{}.ry".format(lipMainControl[2]), 
                                cd="{}.t{}".format(driverMouthCorner,attr), v=-10, dv=-1)

        # control prefix for the lips
        controlPrefix = "lip"
        bindmeshGeometry, follicleList, controlHieracrchyList, jointList = self.__buildCurveRig(lipCurve, controlPrefix , parentGroup)

        # get the position of the controls for lip tweakers
        upperLeft = list()
        upperLeftPosXList = list()
        upperRight = list()
        upperRightPosXList = list()
        lowerLeft = list()
        lowerLeftPosXList = list()
        lowerRight = list()
        lowerRightPosXList = list()
        mouthCornerLeftPosY = round(mc.xform(mouthCorner_l_follicle, q=True, ws=True, t=True)[1], 3)
        mouthCornerRightPosY = round(mc.xform(mouthCorner_r_follicle, q=True, ws=True, t=True)[1], 3)
        for controlHieracrchy in controlHieracrchyList:
            # create the joint that we will use later to deform the base wire.
            baseCurveJoint = mc.joint(name=jointList[controlHieracrchyList.index(controlHieracrchy)].replace("_jnt","_baseCurve_jnt"))
            # hide the base curve joint. Then parent it under the null node
            mc.setAttr("{}.v".format(baseCurveJoint), 0)
            mc.parent(baseCurveJoint, controlHieracrchy[0])
            #position of control
            controlPosition = mc.xform(controlHieracrchy[0], q=True, ws=True, t=True)
            posX = round(controlPosition[0], 3)
            posY = round(controlPosition[1], 3)
            if posX > .001:
                if round(abs(posY-mouthCornerLeftPosY),3) <.003:
                    controlHieracrchyList[controlHieracrchyList.index(controlHieracrchy)] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lip_corner_l")) for ctrl in controlHieracrchy]
                elif posY > mouthCornerLeftPosY:
                    upperLeft.append(controlHieracrchy)
                    upperLeftPosXList.append(posY)
                elif posY < mouthCornerLeftPosY:
                    lowerLeft.append(controlHieracrchy)
                    lowerLeftPosXList.append(posY)

            elif posX < -.001:
                if round(abs(posY-mouthCornerLeftPosY),3) <.003:
                    controlHieracrchyList[controlHieracrchyList.index(controlHieracrchy)] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lip_corner_r")) for ctrl in controlHieracrchy]
                elif posY > mouthCornerRightPosY:
                    upperRight.append(controlHieracrchy)
                    upperRightPosXList.append(posY)
                elif posY < mouthCornerRightPosY:
                    lowerRight.append(controlHieracrchy)
                    lowerRightPosXList.append(posY)
            else:
                if posY > mouthCornerLeftPosY:
                    controlHieracrchyList[controlHieracrchyList.index(controlHieracrchy)] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lip_center_up")) for ctrl in controlHieracrchy]
                elif posY < mouthCornerLeftPosY:
                    controlHieracrchyList[controlHieracrchyList.index(controlHieracrchy)] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lip_center_low")) for ctrl in controlHieracrchy]
        # reorder controls
        upperLeftPosXListCopy = list(upperLeftPosXList)
        upperLeftPosXList.sort()
        # rename the controls for left and right.
        for i, pos in enumerate(upperLeftPosXListCopy):
            # rename the center controls.
            controlHieracrchyList[controlHieracrchyList.index(upperLeft[i])] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lip_up_{}_l".format(upperLeftPosXList.index(pos)))) for ctrl in upperLeft[i]]

        # reorder controls
        upperRightPosXListCopy = list(upperRightPosXList)
        upperRightPosXList.sort()
        # rename the controls for left and right.
        for i, pos in enumerate(upperRightPosXListCopy):
            # rename the center controls.
           controlHieracrchyList[controlHieracrchyList.index(upperRight[i])] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lip_up_{}_r".format(upperRightPosXList.index(pos)))) for ctrl in upperRight[i]]

        # reorder controls
        lowerLeftPosXListCopy = list(lowerLeftPosXList)
        lowerLeftPosXList.sort()
        lowerLeftPosXList.reverse()
        # rename the controls for left and right.
        for i, pos in enumerate(lowerLeftPosXListCopy):
            # rename the center controls.
            controlHieracrchyList[controlHieracrchyList.index(lowerLeft[i])] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lip_low_{}_l".format(lowerLeftPosXList.index(pos)))) for ctrl in lowerLeft[i]]

        # reorder controls
        lowerRightPosXListCopy = list(lowerRightPosXList)
        lowerRightPosXList.sort()
        lowerRightPosXList.reverse()
        # rename the controls for left and right.
        for i, pos in enumerate(lowerRightPosXListCopy):
            # rename the center controls.
            controlHieracrchyList[controlHieracrchyList.index(lowerRight[i])] = [mc.rename(ctrl, "_".join([name for name in ctrl.split("_") if not name.isdigit()]).replace(controlPrefix, "lip_low_{}_r".format(lowerRightPosXList.index(pos)))) for ctrl in lowerRight[i]]


        # parent the curves to their respective systems
        mc.parent(lipMainCurve, "lip_main")
        mc.parent(lipCurve, "lip")

        #deform the lip bindmesh with the lip_main curve using a wire deformer.
        wireDeformer = mc.wire(bindmeshGeometry, gw=False, en=1.00, ce=0.00, li=0.00, 
                w=lipMainCurve, name="{}_wire".format(lipMainCurve))[0]
        # set the default values for the wire deformer
        mc.setAttr("{}.rotation".format(wireDeformer), 0)
        mc.setAttr("{}.dropoffDistance[0]".format(wireDeformer), 100)

        # create skinCluster for the base wire
        baseCurve = "{}BaseWire".format(lipMainCurve)
        lipMainBaseCurveSkin = mc.skinCluster(*mainBaseCurveJointList+mc.ls(baseCurve), 
                                    n="{}_skinCluster".format(baseCurve),
                                    tsb=True)[0]
        # set the weights to have proper weighting
        wtObj = rigrepo.libs.weights.getWeights(lipMainBaseCurveSkin)
        weightList = list()
        for i, inf in enumerate(wtObj):
            array = numpy.zeros_like(wtObj.getWeights(inf))[0]
            array[i] = 1
            weightList.append(array)
        wtObj.setWeights(weightList)
        rigrepo.libs.weights.setWeights(lipMainBaseCurveSkin, wtObj)

        # create all of the lip clusters
        lipControls = mc.ls("lip_*.__control__", o=True)
        for node in lipControls:
            rigrepo.libs.cluster.create(geometry, 
                                        "{}_cluster".format(node), 
                                        contraintTypes=["orient","scale"], 
                                        parent="{}_def_auto".format(node), 
                                        parallel=False)
            nul = "{}_cluster_nul".format(node)
            mc.xform(nul, ws=True, matrix=mc.xform(node, q=True, ws=True, matrix=True))
            mc.connectAttr("{}.t".format(node), "{}_cluster_auto.t".format(node), f=True)
            mc.connectAttr("{}.r".format(node), "{}_cluster_ctrl.r".format(node), f=True)
            mc.connectAttr("{}.s".format(node), "{}_cluster_ctrl.s".format(node), f=True)

    def __buildCurveRig(self, curve, name='lip', parent=None):
        '''
        This will build a rig setup based on the curve that is passed in.

        :param curve: NurbsCurve name you want to build the rig on.
        :type curve: str

        :param name: This will be used to name the control hierachy and joints in the rig.
        :type name: str

        :return: This method will return the data needed to make adjustments to rig.
        :rtype: tuple
        '''
        # Do some check
        if not mc.objExists(curve):
            raise RuntimeError("{} doesn't exist in the current Maya session.".format(curve))
        # If the name passed in doesn't exist, we will create a transform as the parent group
        # for the rig.
        if not mc.objExists(name):
            mc.createNode("transform", n=name)
        # create the bindmesh 
        #
        # follicleList = (follicle transform, follicle shape) 
        # bindmeshGeometry = geometry name of bindmesh
        #
        bindmeshGeometry, follicleList = bindmesh.createFromCurve(name, curve)
        # emptry list to append controls to in the loop
        controlHieracrchyList = list()
        jointList = list()

        # loop through and create controls on the follicles so we have controls to deform the wire.
        for follicle in follicleList:
            # get the follicle transform so we can use it to parent the control to it.
            follicleIndex = follicleList.index(follicle)
            # create the control with a large enough hierarchy to create proper SDK's
            ctrlHierarchy = control.create(name="{}_{}".format(name, follicleIndex), 
                controlType="square", 
                hierarchy=['nul','ort','rot_def_auto','def_auto'], 
                parent=follicle)

            # create the joint that will drive the curve.
            jnt = mc.joint(n="{}_{}_jnt".format(name, follicleIndex))
            # make sure the joint is in the correct space
            mc.setAttr("{}.translate".format(jnt), 0,0,0)
            mc.setAttr("{}.rotate".format(jnt), 0,0,0)
            mc.setAttr("{}.drawStyle".format(jnt),2)
            mc.setAttr("{}.displayHandle".format(ctrlHierarchy[-1]), 1)
            mc.delete(mc.listRelatives(ctrlHierarchy[-1], c=True, shapes=True)[0])

            # zero out the nul for the control hierarchy so it's in the correct position.
            mc.setAttr("{}.translate".format(ctrlHierarchy[0]), 0,0,0)
            #mc.setAttr("{}.rotate".format(ctrlHierarchy[0]), 0,0,0)
            # set the visibility of the shape node for the follicle to be off.
            # append the control and the follicle transform to their lists
            controlHieracrchyList.append(ctrlHierarchy)
            jointList.append(jnt)

        # This will parent all of the data for the rig to the system group "name"
        for data in (bindmeshGeometry, follicleList):
            mc.parent(data, name)

        # If parent the parent is passed in we will parent the system to the parent.
        if parent:
            if not mc.objExists(parent):
                mc.warning('Created the system but the current parent "{}" does not exist in the \
                    current Maya session.'.format(parent))
            else:
                mc.parent(name, parent)

        # create the skinCluster for the lipMainCurve
        mc.skinCluster(*jointList + [curve], tsb=True, name="{}_skinCluster".format(curve))

        # set the visibility of the bindmesh.
        mc.setAttr("{}.v".format(bindmeshGeometry), 0 )
        mc.setAttr("{}.v".format(curve), 0 )
        return bindmeshGeometry, follicleList, controlHieracrchyList, jointList
