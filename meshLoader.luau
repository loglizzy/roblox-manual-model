local MeshLoader = {}

function MeshLoader.LoadTextSubMesh(subMesh: ModuleScript)
    local meshValues = require(subMesh):split(" ")
    local vertices = {}
    local verticeCount = meshValues[1]
    for i = 3, verticeCount, 3 do
        table.insert(vertices, Vector2.new(
            meshValues[i],
            meshValues[i + 1],
            meshValues[i + 2]
        ))
    end
    
    local triangles = {}
    local triangleCount = meshValues[2]
    for i = 3 + verticeCount, 3 + triangleCount, 3 do
        table.insert(triangles, {
            meshValues[i],
            meshValues[i + 1],
            meshValues[i + 2]
        })
    end

    return {
        vertices = vertices,
        triangles = triangles
    }
end

function MeshLoader.LoadTextModel(textModelSplit: Folder)
    local meshes = {}
    for i, meshFolder: Folder in textModelSplit:GetChildren() do
        local subMeshes = {}
        for i, subMeshModule in meshFolder:GetChildren() do
            subMeshes[i] = MeshLoader.LoadTextSubMesh(subMeshModule)
        end

        meshes[i] = subMeshes
    end

    return meshes
end

local AssetService = game:GetService("AssetService")
function MeshLoader.CreateTextModelMeshParts(textModel: {})
    local meshParts = {}

    for i, mesh in textModel do
        meshParts[i] = {}

        for s, subMesh in mesh do
            local editableMesh = AssetService:CreateEditableImage()
            local meshVertexesBaseId
    	    for i, v in mesh.vertices do
    	    	local vertexId = editableMesh:AddVertex(v)
    	    	if not meshVertexesBaseId then
    	    		meshVertexesBaseId = vertexId
    	    	end
    	    end

    	    for i, v in mesh.faces do
    	    	editableMesh:AddTriangle(
    	    		meshVertexesBaseId + v[1],
    	    		meshVertexesBaseId + v[2],
    	    		meshVertexesBaseId + v[3]
    	    	)
    	    end

            local meshPart = AssetService:CreateMeshPartAsync(Content.fromObject(editableMesh), {
                CollisionFidelity = Enum.CollisionFidelity.Box,
                RenderFidelity = Enum.RenderFidelity.Precise
            })

            meshParts[i][s] = meshPart
        end
    end

    return meshParts
end

return MeshLoader