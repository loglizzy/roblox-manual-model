import trimesh
import numpy as np
import os

import trimesh.visual

outputDir = "output"
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

def processVertice(vertice: float, decimals=6):
    return np.round(vertice, decimals)

maxTriangles = 20000

model = "soccer_ball.glb"
modelDir = f"{outputDir}/{model}"
if not os.path.exists(modelDir):
    os.makedirs(modelDir)

scene = trimesh.load(f"models/{model}")
meshes = [geometry for geometry in scene.geometry.values() if isinstance(geometry, trimesh.Trimesh)]
for meshIndex, mesh in enumerate(meshes):
    meshVertexVisual = mesh.visual.kind == 'vertex'
    
    meshSplitDir = f"{modelDir}/mesh_{meshIndex}_split"
    if not os.path.exists(meshSplitDir):
        os.makedirs(meshSplitDir)
    
    for subMeshIndex, subMesh in enumerate(mesh.split(only_watertight=False)):    
        subMesh.merge_vertices()
        subMesh.remove_infinite_values()
        subMesh.update_faces(subMesh.nondegenerate_faces())
        subMesh.update_faces(subMesh.unique_faces())
        subMesh.remove_unreferenced_vertices()

        triangleCount = len(subMesh.triangles)
        if triangleCount > maxTriangles:
            subMesh.simplify_quadric_decimation(face_count=maxTriangles)

        verticeCount = len(subMesh.vertices)
        textMesh = f"{verticeCount} {triangleCount} "
        for vertice in subMesh.vertices:
            x = processVertice(vertice[0])
            y = processVertice(vertice[1])
            z = processVertice(vertice[2])

            textMesh += f" {x} {y} {z}"

        previousFaceC = 0
        for face in subMesh.faces:
            a = face[0]
            a -= previousFaceC

            b = face[1]
            b -= a

            c = face[2]
            previousFaceC = c
            c -= b

            textMesh += f" {a} {b} {c}"
            
        if meshVertexVisual:
            colors = subMesh.visual.vertex_colors
            for color in colors:
                r = color[0]
                g = color[1]
                b = color[2]
                a = color[3]
                textMesh += f" {r} {g} {b} {a}"

        fname = f"{meshSplitDir}/mesh_{subMeshIndex}.luau"
        with open(fname, "wb") as f:
            luauMeshModule = f"return[[{textMesh}]]"
            f.write(luauMeshModule.encode())
        
        print(fname)

print("All meshes saved.")