# WARNING
That project is in totally start right now, very shallow in features.

Things i plan adding over time:
* Vertex color support(already coded but not active)
* Texture color support
* Better mesh splitting method

# Instructions:
1. place your 3D model inside "models" folder
2. run `python meshExtractor`
3. check "output" folder for the results
4. load inside roblox using "meshLoader.luau"
example:
```luau
local MeshLoader = require(pathToMeshLoader)
local sampleTextModel = require(pathToThePythonGeneratedModel)
MeshLoader.CreateTextModelMeshParts(MeshLoader.LoadTextModel(sampleTextModel)
```
