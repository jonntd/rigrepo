import pubs.ui.mainWindow
reload(pubs.ui.mainWindow)
# reload parts
import rigrepo.parts.part
reload(rigrepo.parts.part)
import rigrepo.parts.limb
reload(rigrepo.parts.limb)
import rigrepo.parts.arm
reload(rigrepo.parts.arm)
import rigrepo.parts.spine
reload(rigrepo.parts.spine)
import rigrepo.parts.neck
reload(rigrepo.parts.neck)
import rigrepo.parts.blink
reload(rigrepo.parts.blink)
#reload templates
import rigrepo.templates.base.base
reload(rigrepo.templates.base.base)
import rigrepo.templates.biped.biped
reload(rigrepo.templates.biped.biped)
import rigrepo.libs.data.joint_data
import os
import maya.cmds as mc

buildPath = os.path.join(os.path.dirname(biped.__file__),"build")
mc.file(new=True, force=True)
mc.file(os.path.join(buildPath,"skeleton.ma"), i=True,f=True)
mc.file(os.path.join(buildPath,"blink_curves.ma"), i=True,f=True)

data = rigrepo.libs.data.joint_data.JointData()
data.read(os.path.join(buildPath,"joint_positions.data"))
joints = mc.ls(type='joint')
data.applyData(joints)

# the right arm is all messed up and we have to fix it. Also, you can't run nodes more than once
# in the same scene at th moment. We will have to fix this.
matt_graph = rigrepo.templates.biped.biped.Biped('matt')
pubs.ui.mainWindow.launch(graph=matt_graph)
