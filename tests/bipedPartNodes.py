import pubs.ui.mainWindow; 
reload(pubs.ui.mainWindow)
import rigrepo.templates.biped.biped as bt
reload(bt)
import rigrepo.libs.attribute
reload(rigrepo.libs.attribute)
graph = bt.Biped("elsa")

pubs.ui.mainWindow.launch(graph=graph)
