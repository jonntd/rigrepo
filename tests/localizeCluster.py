import rigrepo.libs.cluster
reload(rigrepo.libs.cluster)

def localizeCluster():
    cluster = 'cluster1'
    transform = 'rig'
    modelTransform = 'model'

    rigrepo.libs.cluster.localize(cluster, transform, modelTransform)
