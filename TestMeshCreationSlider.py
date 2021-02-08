import bpy
import eos
import numpy as np
import bmesh

baseLocation = "D:/Users/Alex/Documents/Personal/Uni/Diss/WorkFolder/eos/out/install/x86-Debug/"

class ShapeKeeper(): # Create a dictionary with the path to model as key, model and value. check against mysetting property of locations 
    base = ""

aShapeKeeper = ShapeKeeper()

def getCoefficients(o):

    cooCount = o.my_settings.ShapeCount
    colourCount = o.my_settings.ColourCount
    expreCount = o.my_settings.ExpressionCount

    if len(o.sliders.sliderList) < cooCount + colourCount + expreCount : return

    me = [[0.0]* cooCount, [0.0]* colourCount, [0.0]* expreCount]

    for x in range(0,cooCount):            

        me[0][x] =  o.sliders.sliderList[x].value
       # print(me[x])

    for x in range(cooCount,cooCount + colourCount):           

        me[1][x - cooCount] =  o.sliders.sliderList[x].value
        #print(me[x])

    for x in range(cooCount + colourCount,cooCount + colourCount + expreCount):            

        me[2][x - cooCount - colourCount] =  o.sliders.sliderList[x].value
        #print(me[x])

    return me

def refreshModel():

    #if aShapeKeeper.base == "": return

    o = bpy.context.object

    coofficient = getCoefficients(o)

    if not(coofficient) : return

    mesh = o.data

    if not(aShapeKeeper.base):
        LoadFaceModel()
        return

    morphModel = aShapeKeeper.base.draw_sample(coofficient[0],coofficient[2],coofficient[1])

    i = 0

    mesh.clear_geometry()

    verts = morphModel.vertices
    edges = []
    faces = morphModel.tvi

    mesh.from_pydata(verts, edges, faces) 

def resize(self, context):
    refreshModel()
    return


def CreateBlenderMesh(mesh):
    blendObj = bpy.data.meshes.new("aNewMesh")  # add the new mesh    
    obj = bpy.data.objects.new(blendObj.name, blendObj)
    col = bpy.data.collections.get("Collection")
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    verts = mesh.vertices
    edges = []
    faces = mesh.tvi

    blendObj.from_pydata(verts, edges, faces)

    return obj

def LoadFaceModel():

    morphablemodel_with_expressions = ""

    modelPath = "D:/Users/Alex/Documents/Personal/Uni/Diss/Not_OpenSource/4dfm_head_v1.2_with_colour.bin"
    blendshapesPath = ""

    model = eos.morphablemodel.load_model(modelPath)

    #model = eos.morphablemodel.load_model(baseLocation + "share/sfm_shape_3448.bin")
    #morphablemodel_with_expressions = eos.morphablemodel.load_model(baseLocation + "share/sfm_shape_3448.bin")

    #model = eos.morphablemodel.load_model("D:/Users/Alex/Documents/Personal/Uni/Diss/Not_OpenSource/4dfm_head_v1.2_with_colour.bin")

    #model = eos.morphablemodel.load_model("D:/Users/Alex/Documents/Personal/Uni/Diss/Not_OpenSource/LYHM_global.bin")

    #model = eos.morphablemodel.load_model("D:/Users/Alex/Documents/Personal/Uni/Diss/Not_OpenSource/4dfm_head_v1.2_blendshapes_with_colour.bin")

    print("HAS MODEL THING :")
    print(model.get_expression_model_type())

    modelType = model.get_expression_model_type()

    if(modelType == model.ExpressionModelType.Blendshapes):
        pass

    elif(modelType == model.ExpressionModelType.PcaModel):
        pass

    else:
        pass




    #blendshapes = eos.morphablemodel.load_blendshapes(baseLocation + "share/expression_blendshapes_3448.bin")

    #print(blendshapes)
    #print("----------------------------------")
    #blendshapes = eos.morphablemodel.load_model("D:/Users/Alex/Documents/Personal/Uni/Diss/Not_OpenSource/4dfm_head_v1.2_blendshapes_with_colour.bin")
    #print(blendshapes)

    # morphablemodel_with_expressions = eos.morphablemodel.MorphableModel(model.get_shape_model(), blendshapes,
    #                                                                     color_model=eos.morphablemodel.PcaModel(),
    #                                                                     vertex_definitions=None,
    #                                                                     texture_coordinates=model.get_texture_coordinates())

    # morphablemodel_with_expressions = eos.morphablemodel.MorphableModel(model.get_shape_model(), blendshapes.get_expression_model(),
    #                                                                     color_model=eos.morphablemodel.PcaModel(),
    #                                                                     vertex_definitions=None,
    #                                                                     texture_coordinates=model.get_texture_coordinates())

    aShapeKeeper.base = model

    if(morphablemodel_with_expressions != ""):
        aShapeKeeper.base = morphablemodel_with_expressions
    else:
        morphablemodel_with_expressions = model
    
    return morphablemodel_with_expressions




def CreateBaseShape():
    
    base = LoadFaceModel()

    secondMesh = base.draw_sample([0,0,0],[0,0,0])

    obj = CreateBlenderMesh(secondMesh)

    modelType = base.get_expression_model_type()

    if(modelType == None):
        obj.my_settings.ExpressionCount = 0
        obj.my_settings.ShapeCount = 0
        obj.my_settings.ColourCount = 0

    elif(modelType == base.ExpressionModelType.Blendshapes):
        obj.my_settings.ExpressionCount = len(base.get_expression_model())
        obj.my_settings.ShapeCount = base.get_shape_model().get_num_principal_components()
        obj.my_settings.ColourCount = base.get_color_model().get_num_principal_components()

    else:
        obj.my_settings.ExpressionCount = 0
        obj.my_settings.ShapeCount = base.get_shape_model().get_num_principal_components()
        obj.my_settings.ColourCount = base.get_color_model().get_num_principal_components()

    print(obj.my_settings.ShapeCount)
    print(obj.my_settings.ColourCount)
    print(obj.my_settings.ExpressionCount)

    if not obj.get('_RNA_UI'):
        obj['_RNA_UI'] = {}

    for x in range(0,obj.my_settings.ShapeCount + obj.my_settings.ColourCount + obj.my_settings.ExpressionCount):
        prop = obj.sliders.sliderList.add()
        prop.value = 0

   

    #print(aShapeKeeper.base)

    return base




#base = LoadFaceModel()
# cooCount = base.get_shape_model().get_num_principal_components()
# colourCount = base.get_color_model().get_num_principal_components()

# print("ColourCount : %d", colourCount)
# expreCount = len(base.get_expression_model())

class MySettings(bpy.types.PropertyGroup):
   
    ExpressionCount : bpy.props.IntProperty(name = "ExpressionCount", description = "Number of Expressions",default = 0)
    ColourCount : bpy.props.IntProperty(name = "ColourCount", description = "Number of Colour",default = 0) 
    ShapeCount : bpy.props.IntProperty(name = "ShapeCount", description = "Number of Shapes",default = 0)   

class SliderProp(bpy.types.PropertyGroup):
    value : bpy.props.FloatProperty(name = "Length",min = -3, max = 3, description = "DataLength", default = 0, update = resize, options = {'ANIMATABLE'})

class SliderList(bpy.types.PropertyGroup):
    sliderList : bpy.props.CollectionProperty(type=SliderProp)

class Create_Model(bpy.types.Operator):
    bl_idname = "view3d.create_model"
    bl_label = "Create Model"
    bl_destription = "A button to create a new morphable face"

    def execute(self, context):

        CreateBaseShape()

        return {'FINISHED'}

# class Slider_Menu(bpy.types.Operator):
#     bl_idname = "view3d.add_frame"
#     bl_label = "Moves Page"
#     bl_destription = "Moves page of current sliders"

#     def execute(self, context):

#         CreateBaseShape()

#         return {'FINISHED'}

class TEST_PT_Panel(bpy.types.Panel):
    bl_idname = "TEST_PT_Panel"
    bl_label = "Test Panel"
    bl_category = "Test Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object
        box = layout.box()     

        row = box.row()
        row.operator('view3d.create_model')  
        
        if(obj != None):

            objType = getattr(obj, "type", "")

            if(objType == "MESH"):                             

                ob = context.active_object
                
                row = box.row()
                row.label(text = "Object: " + ob.name)

                cooCount = ob.my_settings.ShapeCount
                colourCount = ob.my_settings.ColourCount
                expreCount = ob.my_settings.ExpressionCount
            

                #row = box.row()
                #row.prop(obj.my_settings, "reverse")

                if(cooCount > 0):

                    row = box.row()
                    row.label(text = "Shape")
                    row = box.row()

                    cf = row.column_flow(columns = 3, align = False)            
                    for x in range(0,cooCount):             

                        k = "line_%d" % x   
                        cf.prop(obj.sliders.sliderList[x], "value")

                if(colourCount > 0):

                    row = box.row()
                    row.label(text = "Colour: ")
                    row = box.row()
                    cf = row.column_flow(columns = 3, align = False)            
                    for x in range(cooCount,colourCount):             

                        k = "line_%d" % x   
                        cf.prop(obj.sliders.sliderList[x], "value")
                
                if(expreCount > 0):

                    row = box.row()
                    row.label(text = "Expression: ")
                    row = box.row()
                    cf = row.column_flow(columns = 3, align = False)            
                    for x in range(cooCount + colourCount, cooCount + colourCount + expreCount):             

                        k = "line_%d" % x   
                        #cf.prop(obj, '["' + k + '"]')
                        cf.prop(obj.sliders.sliderList[x], "value") 

classes = (
    TEST_PT_Panel,
    Create_Model,
    MySettings,
    SliderProp,
    SliderList
        )

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)   

    bpy.types.Object.my_settings = bpy.props.PointerProperty(type=MySettings)
    bpy.types.Object.sliders = bpy.props.PointerProperty(type=SliderList)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)             

if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()

  