# import pubs
import pubs.pObject
reload(pubs.pObject)
import pubs.pAttribute
reload(pubs.pAttribute)
import pubs.pNode
reload(pubs.pNode)
import pubs.pDict
reload(pubs.pDict)
import pubs.pGraph
reload(pubs.pGraph)

#import pubs UI
import pubs.ui.fields
reload(pubs.ui.fields)
import pubs.ui.models
reload(pubs.ui.models)
import pubs.ui.widgets
reload(pubs.ui.widgets)
#import pubs.ui.browser
#reload(pubs.ui.browser)
import pubs.ui.centralWidget
reload(pubs.ui.centralWidget)
import pubs.ui.mainWindow
reload(pubs.ui.mainWindow)

#reload libs
import rigrepo.libs.data.abstract_data
reload(rigrepo.libs.data.abstract_data)
import rigrepo.libs.data.node_data
reload(rigrepo.libs.data.node_data)
import rigrepo.libs.data.joint_data
reload(rigrepo.libs.data.joint_data)
import rigrepo.libs.data.curve_data
reload(rigrepo.libs.data.curve_data)
import rigrepo.libs.common
reload(rigrepo.libs.common)
import rigrepo.libs.transform
reload(rigrepo.libs.transform)
import rigrepo.libs.attribute
reload(rigrepo.libs.attribute)
import rigrepo.libs.ikfk
reload(rigrepo.libs.ikfk)
import rigrepo.libs.spline
reload(rigrepo.libs.spline)
import rigrepo.libs.skinCluster
reload(rigrepo.libs.skinCluster)
import rigrepo.libs.curve
reload(rigrepo.libs.curve)
import rigrepo.libs.joint
reload(rigrepo.libs.joint)
import rigrepo.libs.shape
reload(rigrepo.libs.shape)


#reload nodes
import rigrepo.nodes.commandNode
reload(rigrepo.nodes.commandNode)
import rigrepo.nodes.newSceneNode
reload(rigrepo.nodes.newSceneNode)
import rigrepo.nodes.loadFileNode
reload(rigrepo.nodes.loadFileNode)

# reload parts
import rigrepo.parts.part
reload(rigrepo.parts.part)
import rigrepo.parts.limb
reload(rigrepo.parts.limb)
import rigrepo.parts.arm
reload(rigrepo.parts.arm)
import rigrepo.parts.leg
reload(rigrepo.parts.leg)
import rigrepo.parts.spine
reload(rigrepo.parts.spine)
import rigrepo.parts.neck
reload(rigrepo.parts.neck)
import rigrepo.parts.blink
reload(rigrepo.parts.blink)
import rigrepo.parts.hand
reload(rigrepo.parts.hand)

#reload templates
import rigrepo.templates.archetype.rig.build.archetypeRig
reload(rigrepo.templates.archetype.rig.build.archetypeRig)
import rigrepo.templates.biped.rig.build.bipedRig
reload(rigrepo.templates.biped.rig.build.bipedRig)

#regular imports
import os
import maya.cmds as mc

buildPath = os.path.join(os.path.dirname(rigrepo.templates.biped.rig.build.bipedRig.__file__),"base")
mc.file(new=True, force=True)
mc.file(os.path.join(buildPath,"skeleton.ma"), i=True,f=True)
mc.file(os.path.join(buildPath,"blink_curves.ma"), i=True,f=True)

data = rigrepo.libs.data.joint_data.JointData()
data.read(os.path.join(buildPath,"joint_positions.data"))
joints = mc.ls(type='joint')
data.applyData(joints)

# the right arm is all messed up and we have to fix it. Also, you can't run nodes more than once
# in the same scene at th moment. We will have to fix this.
matt_graph = rigrepo.templates.biped.rig.build.bipedRig.BipedRig('matt')
pubs.ui.mainWindow.launch(graph=matt_graph)
