#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image 

Shaders = {}
Lights = []
Spheres = []

class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float64)
    def __add__(self, b):
        ret = np.array([0,0,0]).astype(np.float64)
        ret = ret + self.color
        ret = ret + b.color
        return Color(ret[0],ret[1],ret[2])


    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)

class Camera:
    def __init__(self, c):
        self.viewpoint =  np.fromstring(c.findtext('viewPoint'),dtype = np.float64, sep = ' ') if c.findtext('viewPoint') else np.array([0,0,0]).astype(np.float64)
        self.viewDir=np.fromstring(c.findtext('viewDir'),dtype = np.float64, sep = ' ')if c.findtext('viewDir') else np.array([0,0,-1]).astype(np.float64)
        self.viewProjNormal=np.fromstring(c.findtext('projNormal'),dtype = np.float64, sep = ' ')  if c.findtext('projNormal') else -1*self.viewDir 
        self.viewUp=np.fromstring(c.findtext('viewUp'),dtype = np.float64, sep = ' ') if c.findtext('viewUp') else np.array([0,1,0]).astype(np.float64)
        self.projDistance=np.fromstring(c.findtext('projDistance'),dtype = np.float64, sep = ' ') if c.findtext('projDistance') else 1.0
        self.viewWidth=np.fromstring(c.findtext('viewWidth'),dtype = np.float64, sep = ' ') if c.findtext('viewWidth') else 1.0
        self.viewHeight=np.fromstring(c.findtext('viewHeight'),dtype = np.float64, sep = ' ') if c.findtext('viewHeight') else 1.0

class Sphere:
    def __init__(self, sp):
        self.rad = np.float64(sp.findtext('radius'))
        self.cent = np.fromstring(sp.findtext('center'),dtype = np.float64, sep = ' ')
        self.shadername = sp.find('shader').get('ref')
        self.shader = Shaders[self.shadername]
    
    def normal(self,p):
        q = p-self.cent
        if np.linalg.norm(q) != 0:
            return q/np.linalg.norm(q)
        return np.array([0,0,0])

    def hit(self, vp, ray):
        p = np.dot(self.cent-vp,ray)
        q = np.dot(self.cent-vp,self.cent-vp)
        ac = p**2-q+self.rad**2
        if ac<=0.005:
            return np.inf
        if p-np.sqrt(ac) >= 0 :
            return p-np.sqrt(ac)
        if p+np.sqrt(ac) >= 0 :
            return p+np.sqrt(ac)
        return np.inf
    
        

class Shader:
    def __init__(self,type):
        self.tp = type

class PhongShader(Shader):
    def __init__(self,ps):
        super().__init__(ps.get('type'))
        self.d = np.fromstring(ps.findtext('diffuseColor'),dtype = np.float64, sep = ' ')
        self.s = np.fromstring(ps.findtext('specularColor'),dtype = np.float64, sep = ' ')
        self.e = np.float64(ps.findtext('exponent'))
    def Ph_getColor(self,vp, nor, hp):
        clr = Color(0,0,0)
        for lgt in Lights:
            dir = hp-lgt.pos
            if np.linalg.norm(dir) != 0 :
                dir = dir/np.linalg.norm(dir) 
            if np.linalg.norm(vp) != 0 :
                vd = vp/np.linalg.norm(vp)     
            hv = vd + dir
            if np.linalg.norm(hv) != 0 :
                hv = hv/np.linalg.norm(hv) 
            nl = np.dot(nor, -hv) 
            dn = np.dot(-dir,nor)
            tmp=0 
            if(Spheres):
                for c in Spheres:
                    a=c.hit(hp,-dir)
                    if(tmp<a and a!=np.inf): 
                        tmp=a
            if(tmp<0.003):            
                clr = clr + Color(self.d[0]*lgt.itn[0] * max(0,dn) ,self.d[1]*lgt.itn[1] * max(0,dn),self.d[2]*lgt.itn[2] * max(0,dn))
                ex = np.power(max(0,nl), self.e)
                clr = clr + Color(self.s[0]*ex,self.s[1]*ex,self.s[2]*ex)
                clr.gammaCorrect(2.2)
            else:
                clr = Color(0,0,0) 
        return clr.toUINT8()
       
class LambertianShader(Shader):
    def __init__(self,ls):
        super().__init__(ls.get('type'))
        self.d = np.fromstring(ls.findtext('diffuseColor'),dtype = np.float64, sep = ' ')
    def Lam_getColor(self, nor, hp):
        clr = Color(0,0,0)
        for lgt in Lights:
            dir = hp-lgt.pos #to light from hitpoint 
            if np.linalg.norm(dir) != 0 :
                dir = dir/np.linalg.norm(dir) 
            nl = np.dot(-dir,nor)
            tmp=0 
            if(Spheres):
                for c in Spheres:
                    a=c.hit(hp,-dir)
                    if(tmp<a and a!=np.inf): 
                        tmp=a
        clr = clr+Color(self.d[0]*lgt.itn[0] * max(0,nl) ,self.d[1]*lgt.itn[1] * max(0,nl),self.d[2]*lgt.itn[2] * max(0,nl)) if tmp<0.003 else Color(0,0,0) 
        clr.gammaCorrect(2.2)
        return clr.toUINT8()   
            

class Light:
    def __init__(self,lgt):
        self.pos = np.fromstring(lgt.findtext('position'),dtype = np.float64, sep = ' ')
        self.itn = np.fromstring(lgt.findtext('intensity'),dtype = np.float64, sep = ' ')



def main():
    np.seterr(invalid='ignore')
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    imgSize=np.array(root.findtext('image').split()).astype(np.int32)

    for c in root.findall('camera'):
        camera = Camera(c)
    for s in root.findall('shader'):
        type = s.get('type')
        name = s.get('name')
        if (type == 'Phong'):
            Shaders[name] = PhongShader(s)
        if (type == 'Lambertian'):
            Shaders[name] = LambertianShader(s) 
    for c in root.findall('light') :
        Lights.append(Light(c)) 
    for c in root.findall('surface') :
        tp = c.get('type')
        if tp == 'Sphere' :
            Spheres.append(Sphere(c))
              

    #code.interact(local=dict(globals(), **locals()))  

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0
    
    # replace the code block below!
    
    #ray
    u = np.cross(camera.viewDir ,camera.viewUp)
    if np.linalg.norm(u) != 0:    
        u= u/np.linalg.norm(u)  
    v = np.cross(u,camera.viewDir)#image-pixel mapping
    if np.linalg.norm(v) != 0:
        v= v/np.linalg.norm(v)  
    

    origin = camera.viewDir/np.linalg.norm(camera.viewDir) * camera.projDistance + camera.viewHeight/2 * v - camera.viewWidth/2 * u
    for i in np.arange(imgSize[1]): 
        for j in np.arange(imgSize[0]): 
            ray = np.array(origin + camera.viewHeight * -v * (i+0.5) /imgSize[1] + camera.viewWidth * u * (j+0.5) /imgSize[0])
            if np.linalg.norm(ray) != 0:
                ray = ray/np.linalg.norm(ray) 
            tmp=np.inf
            if(Spheres):
                tmp2=Spheres[0]
                for c in Spheres:
                    a=c.hit(camera.viewpoint,ray)
                    if(tmp>a): 
                        tmp=a
                        tmp2=c # last hitted sphere 
            if tmp == np.inf:
                img[i][j] = np.array([0,0,0])
            if(tmp2.shader.tp == 'Lambertian'):
                img[i][j] = tmp2.shader.Lam_getColor(tmp2.normal(camera.viewpoint+ray*tmp),camera.viewpoint+ray*tmp)
            if(tmp2.shader.tp == 'Phong'):
                img[i][j]=tmp2.shader.Ph_getColor(camera.viewDir,tmp2.normal(camera.viewpoint+ray*tmp),camera.viewpoint+ray*tmp)
    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')
    
if __name__=="__main__":
    main()
