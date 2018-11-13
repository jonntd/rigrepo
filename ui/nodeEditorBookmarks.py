import maya.cmds as mc
from rigrepo.libs.fileIO import joinPath

def exportBookmark(bookmarkName, path=1):
    bookmark = findBookmarkNode(bookmarkName)
    if not bookmark:
        print(bookMarkName+' does not exist.')
        return False
    connections = mc.listConnections(bookmark+'.ni', p=1, c=1)
    # Disconect for export
    for i in xrange(0, len(connections), 2):
        nodeAttr = connections[i+1]
        bookmarkAttr = connections[i]
        mc.disconnectAttr(nodeAttr, bookmarkAttr)
    mc.select(bookmark)
    filePath = joinPath(path, bookmarkName)
    print('Bookmark export', filePath)
    mc.file(filePath, es=1, force=1, typ='mayaAscii')

    # Reconnect
    for i in xrange(0, len(connections), 2):
        nodeAttr = connections[i+1]
        bookmarkAttr = connections[i]
        mc.connectAttr(nodeAttr, bookmarkAttr)

def findBookmarkNode(bookmark):
    for bookmarkNode in mc.ls(type='nodeGraphEditorBookmarkInfo'):
        name = mc.getAttr(bookmarkNode + '.nm')
        if name == bookmark:
            print('found', bookmark, bookmarkNode)
            return(bookmarkNode)

'''
createNode nodeGraphEditorBookmarkInfo -n "nodeView1";
	rename -uid "8739FEA9-420B-1EE6-EA3E-0381A9E1B7D7";
	setAttr ".nm" -type "string" "mattsBookmark";
	setAttr ".vl" -type "double2" -452.97617247653466 -263.69046571235856 ;
	setAttr ".vh" -type "double2" 453.57141054811996 224.99999105930365 ;
	setAttr -s 2 ".ni";
	setAttr ".ni[0].x" -330.35711669921875;
	setAttr ".ni[0].y" 132.14285278320313;
	setAttr ".ni[0].nvs" 18305;
	setAttr ".ni[1].x" 201.78570556640625;
	setAttr ".ni[1].y" -28.571428298950195;
	setAttr ".ni[1].nvs" 18306;

connectAttr "null2.msg" "nodeView1.ni[0].dn";
connectAttr "null1.msg" "nodeView1.ni[1].dn";
'''

