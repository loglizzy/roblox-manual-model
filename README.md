Instructions:
1. place your 3D model inside "models" folder
2. run `python meshExtractor`
3. check "meshes" folder for the results
4. load inside roblox using "meshLoader.luau"
example:
```luau
local MeshLoader = require(pathToMeshLoader)
local sampleTextModel = require(pathToThePythonGeneratedModel)
MeshLoader.CreateTextModelMeshParts(MeshLoader.LoadTextModel(sampleTextModel)
```