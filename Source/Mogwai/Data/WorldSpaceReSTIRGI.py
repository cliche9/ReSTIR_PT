from falcor import *
import os


def render_graph_WorldSpaceReSTIRGI():
    g = RenderGraph("WorldSpaceReSTIRGIPass")
    loadRenderPassLibrary("AccumulatePass.dll")
    loadRenderPassLibrary("GBuffer.dll")
    loadRenderPassLibrary("WorldSpaceReSTIRGIPass.dll")
    loadRenderPassLibrary("ToneMapper.dll")
    loadRenderPassLibrary("ScreenSpaceReSTIRPass.dll")
    loadRenderPassLibrary("ErrorMeasurePass.dll")
    loadRenderPassLibrary("ImageLoader.dll")

    WorldSpaceReSTIRGIPass = createPass("WorldSpaceReSTIRGIPass", {'samplesPerPixel': 1})
    g.addPass(WorldSpaceReSTIRGIPass, "WorldSpaceReSTIRGIPass")
    GBufferRT = createPass("GBufferRT", {'samplePattern': SamplePattern.Center, 'sampleCount': 1, 'texLOD': TexLODMode.Mip0, 'useAlphaTest': True})
    g.addPass(GBufferRT, "GBufferRT")
    AccumulatePass = createPass("AccumulatePass", {'enableAccumulation': False, 'precisionMode': AccumulatePrecision.Double})
    g.addPass(AccumulatePass, "AccumulatePass")
    ToneMapper = createPass("ToneMapper", {'autoExposure': False, 'exposureCompensation': 0.0, 'operator': ToneMapOp.Linear})
    g.addPass(ToneMapper, "ToneMapper")
    ScreenSpaceReSTIRPass = createPass("ScreenSpaceReSTIRPass")    
    g.addPass(ScreenSpaceReSTIRPass, "ScreenSpaceReSTIRPass")
    
    g.addEdge("GBufferRT.vbuffer", "WorldSpaceReSTIRGIPass.vbuffer")   
    g.addEdge("GBufferRT.depth", "WorldSpaceReSTIRGIPass.vDepth")
    g.addEdge("GBufferRT.faceNormalW", "WorldSpaceReSTIRGIPass.vNormW")
    
    g.addEdge("GBufferRT.vbuffer", "ScreenSpaceReSTIRPass.vbuffer")   
    g.addEdge("GBufferRT.mvec", "ScreenSpaceReSTIRPass.motionVectors")    
    # g.addEdge("ScreenSpaceReSTIRPass.color", "WorldSpaceReSTIRGIPass.directLighting")    
    
    g.addEdge("WorldSpaceReSTIRGIPass.outputColor", "AccumulatePass.input")
    g.addEdge("AccumulatePass.output", "ToneMapper.src")
    
    g.markOutput("ToneMapper.dst")
    g.markOutput("AccumulatePass.output")  

    return g

graph_WorldSpaceReSTIRGI = render_graph_WorldSpaceReSTIRGI()

m.addGraph(graph_WorldSpaceReSTIRGI)
# m.loadScene('VeachAjar/VeachAjar.pyscene')