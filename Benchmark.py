

import bpy
import sys
from mathutils import Vector
from mathutils import Euler
import math
import random




def object_setter(size, type, amount):
    print(type)
    n=0
    margin=size*2
    side = math.ceil(math.sqrt(amount))
    str = ("bpy.ops.mesh.primitive_"+type+"_add")
    if type == 'monkey' or 'cube':
        for i in range(side):
            for j in range(side):
                if (n<amount):
                    n+=1
                    eval(str)(size=size, enter_editmode=False, location=(j*margin, i*margin, 0))
                else: break;
    else:
        for i in range(side):
            for j in range(side):
                if (n<amount):
                    n+=1
                    eval(str)(radius=size, enter_editmode=False, location=(j*margin, i*margin, 0))
                else: break;

def camera_setter(size, amount):
    koef = 1.5 #camera length and width
    line = math.ceil(math.sqrt(amount))
    x = (line-1)*size
    y = -(line-1)*size*2-koef
    z = (line-1)*size*2+koef
    bpy.data.objects["Camera"].location = Vector((x, y, z))
    bpy.data.objects["Camera"].rotation_euler = Euler((0.9, 0, 0))

def material_maker(count):
    for i in range(count):
        matName = 'Material_'+ str(i)
        mat_ball = bpy.data.materials.new(name=matName)
        bpy.data.materials[matName].use_nodes = True
        bpy.data.materials[matName].node_tree.nodes.new("RPRShaderNodeUber")
        bpy.data.materials[matName].node_tree.links.clear()
        bpy.data.materials[matName].node_tree.links.new(bpy.data.materials[matName].node_tree.nodes["RPR Uber"].outputs["Shader"],
        bpy.data.materials[matName].node_tree.nodes["Material Output"].inputs["Surface"])
        bpy.data.materials[matName].node_tree.nodes["RPR Uber"].inputs[1].default_value = (random.random(), random.random(), random.random(), 1)

def apply_materials():
    counter = len(bpy.data.materials)-1
    print(counter)
    for object in bpy.data.objects:
        if (object.type == 'MESH'):
            object.data.materials.append(bpy.data.materials[random.randint(0,counter)])  
            
def light_maker(amount, type, size, amount_obj):
    line = math.ceil(math.sqrt(amount_obj))
    x = (line-1)*size*2
    if type == 'IES':
        file = bpy.ops.image.open(filepath="/home/kirill/Documents/ies-lights-pack/star.ies", directory="/home/kirill/Documents/ies-lights-pack", files=[{"name":"star.ies", "name":"star.ies"}], show_multiview=False)   
        light_data = bpy.data.lights.new(name="mylight", type='POINT' )
        light_data.rpr.ies_file = bpy.data.images.get("star.ies")
        
        for i in range(amount):
            light_data.energy = 5
            light_object = bpy.data.objects.new(name="mylight_"+str(i), object_data=light_data)
            bpy.context.collection.objects.link(light_object)
            light_object.location = (random.randint(-1, x),random.randint(-1, x), x)
        
    else:
        light_data = bpy.data.lights.new(name="mylight", type=type)
        for i in range(amount):
            light_data.energy = 1000
            light_object = bpy.data.objects.new(name="mylight_"+str(i), object_data=light_data)
            bpy.context.collection.objects.link(light_object)
            light_object.location = (random.randint(-1, x),random.randint(-1, x), x)
        
def set_env(samples, threshold, IBL):

    objs = [ob for ob in bpy.context.scene.objects if ob.type in ('LIGHT', 'MESH')]
    bpy.ops.object.delete({"selected_objects": objs})

    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)
	
    bpy.context.scene.render.engine = 'RPR'
    bpy.context.scene.world.rpr.enabled = IBL #boolean
    bpy.context.scene.rpr.limits.max_samples = samples
    bpy.context.scene.rpr.limits.noise_threshold = threshold

     
argv = sys.argv
argv = argv[argv.index("--") +1:]
s = " ".join(argv)[1:-1]
d = {i.split(':')[0]: i.split(':')[1] for i in s.split(', ')}

TypeOfLight = d['TypeOfLight']
MaxSamples = int(d['MaxSamples'])
Threshold = float(d['Threshold'])
TypeOfObject = d['TypeOfObject']
CountOfObjects = int(d['CountOfObjects'])
CountOfLights = int(d['CountOfLights'])
CountOfMaterials = int(d['CountOfMaterials'])
Size = int(d['ObjectSize'])

if d['UseIBL'] == 'false':
    UseIBL = False
else:
    UseIBL = True


        
set_env(MaxSamples,Threshold, UseIBL) 
object_setter(Size, TypeOfObject, CountOfObjects);
camera_setter(Size, CountOfObjects);
material_maker(CountOfMaterials);
apply_materials();
light_maker(CountOfLights, TypeOfLight, Size, CountOfObjects)

bpy.context.scene.render.filepath = "//Benchmark.png"
bpy.ops.render.render(write_still = True)

