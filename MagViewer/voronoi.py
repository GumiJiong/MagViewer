import numpy as np
from scipy.spatial import ConvexHull, Voronoi


def voronoi_volume(pos):
    lens = len(pos)
    offsets = np.array(np.meshgrid([1, -1, 0], [1, -1, 0], [1, -1, 0])).T.reshape(-1, 3)
    offsets = offsets[np.any(offsets != 0, axis=1)]

    for i in range(lens):
        for offset in offsets:
            pos = np.concatenate((pos, [pos[i] + offset]))

    vor = Voronoi(pos)
    vol = np.zeros(vor.npoints)
    for i, reg_num in enumerate(vor.point_region):
        indices = vor.regions[reg_num]
        if -1 in indices:  # some regions can be opened
            vol[i] = np.inf
        else:
            vol[i] = ConvexHull(vor.vertices[indices]).volume
    return vol[:lens]
