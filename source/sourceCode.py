import numpy as np
from numpy import sin, cos, pi
from skimage import measure
import trimesh
import os
import pycork

#Double Gyroid Equation
def tpms_equation(x, y, z, a, t):
    # Gyroid surface
    cox=cos(2.0*pi*x/a)
    siy=sin(2.0*pi*y/a)
    coy=cos(2.0*pi*y/a)
    siz=sin(2.0*pi*z/a)
    coz=cos(2.0*pi*z/a)
    six=sin(2.0*pi*x/a)
    return ((six**2)*(coy**2) + (siy**2)*(coz**2) + (siz**2)*(cox**2) + (2*six*coy*siy*coz) + (2*six*coy*siz*cox) + (2*cox*siy*siz*coz)) - (t**2)

path="C:\\Users\\Public\\"  #Working folder
name="3DBenchy.stl"  #STL file located at the working folder

#Gyroid Parameters
a_cell = 1e-2  # [m] Unit cell size
strut_param = 0.7  # "t" value for the gyroid equation. Level-set value for the gyroid surface
res = 20j  # 155j #                          #Resolution of a single unit cell. Number of voxels
reso = res.imag  # Take imaginary part of the "res" variable
#Size correction and number of units
a_cell = 1000 * a_cell  # Factor to get the correct size


#Input geometry
##################################################################################################
#Basic cube (Comment this block if external geometry is to be used)
# total_l = 2.0e-2  # [m] Length of the prism
# total_w = 2.0e-2  # [m] Width of the prism
# total_h = 2.0e-2  # [m] Height of the prism
#
# #Size and unit corrections
# total_l = 1000 * total_l  # Factor to get the correct size
# total_w = 1000 * total_w  # Factor to get the correct size
# total_h = 1000 * total_h  # Factor to get the correct size
# meshg=trimesh.primitives.Box(extents=([total_l,total_w,total_h]))
#
# total_l = meshg.extents[0]*1.5
# total_w = meshg.extents[1]*1.5
# total_h = meshg.extents[2]*1.5

##################################################################################################
#External geometry (Comment this block if basic cube is to be generated)
meshg=trimesh.load_mesh(path+name)

xmax=meshg.bounds[:,0][1]
xmin=meshg.bounds[:,0][0]
ymax=meshg.bounds[:,1][1]
ymin=meshg.bounds[:,1][0]
zmax=meshg.bounds[:,2][1]
zmin=meshg.bounds[:,2][0]

cenx = (xmax + xmin) / 2
ceny = (ymax + ymin) / 2
cenz = (zmax + zmin) / 2
centro = np.array([cenx, ceny, cenz])

meshg.vertices -= centro

total_l = (xmax-xmin)+1.2
total_w = (ymax-ymin)+1.2
total_h = (zmax-zmin)+1.2

##################################################################################################

geotry=trimesh.exchange.off.export_off(meshg, digits=3)
with open(path+"geotry.off", "w") as text_file:
    text_file.write("%s" % geotry)

nx = total_l / a_cell  
ny = total_w / a_cell 
nz = total_h / a_cell 
  
#Gyroid creation with marching cubes
xi, yi, zi = np.mgrid[0:total_l:res * nx, 0:total_w:res * ny, 0:total_h:res * nz]
vol = tpms_equation(xi, yi, zi, a_cell, strut_param)
verts, faces, normals, values = measure.marching_cubes(vol,0, spacing=(total_l / (int(nx * reso)-1 ), total_w / (int(ny * reso)-1 ), total_h / (int(nz * reso)-1 )))  # 
meshf = trimesh.Trimesh(vertices=verts[:], faces=faces[:], vertex_normals=normals[:])
meshf.vertices -= meshf.centroid        
meshoff=trimesh.exchange.off.export_off(meshf, digits=3)
with open(path+"tpms.off", "w") as text_file:
    text_file.write("%s" % meshoff)


#Boolean intersection with pycork
meshA = trimesh.load_mesh(path+"geotry.off", process=False)
meshB = trimesh.load_mesh(path+"tpms.off", process=False)
vertsA = meshA.vertices
trisA = meshA.faces
vertsB = meshB.vertices
trisB = meshB.faces
vertsD, trisD = pycork.intersection(vertsA, trisA,vertsB, trisB)
meshC = trimesh.Trimesh(vertices=vertsD, faces=trisD, process=False)
meshC.export(path+"resultado.stl")
os.remove(path+"geotry.off")
os.remove(path+"tpms.off")

#Gyroid properties
area=round((meshC.area),4) #[mm^2] Total surface 
vol=round((meshC.volume),4) #[mm^2] Total volume 
RD=meshC.volume/meshA.volume #[%] Volume fraction 
RD=RD*100
RD=round(RD,4)

print("Total surface [mm^2]: ",area)
print("Total volume [mm^2]: ",vol)
print("Volume fraction (%): ",RD)


