import pyvista as pv


NORMAL_OPTIONS = {
    "cell_normals": True,
    "point_normals": True,
    "split_vertices": True,
    "flip_normals": False,
    "consistent_normals": True,
    "auto_orient_normals": False,
    "non_manifold_traversal": True,
    "feature_angle": 30.0,
    "inplace": False,
}


def make_disc(center, inner, outer, normal, r_res, c_res):
    return pv.Disc(
        center=center,
        inner=inner,
        outer=outer,
        normal=normal,
        r_res=r_res,
        c_res=c_res,
    )


def make_polydata(points, faces=None, force_float=False):
    if faces is None:
        return pv.PolyData(points, force_float=force_float)
    return pv.PolyData(points, faces, force_float=force_float)


def read_mesh(path):
    return pv.read(path)


def is_polydata(mesh):
    return isinstance(mesh, pv.core.pointset.PolyData)


def compute_normals(mesh):
    return mesh.compute_normals(**NORMAL_OPTIONS)
