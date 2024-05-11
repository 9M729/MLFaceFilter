import sys
import glob
import os
import shutil

"""
 копирует файлы и папки согласно лимиту в папку DESTSOURCE
 если в папке меньше лимита то он ее не копирует
 если больше то перестает копировать по достижению лимита
 
"""

DATASOURCE = "/Volumes/Seagate Exp/data/models_filtered"
DATADEST = "/Volumes/Seagate Exp/data/models_files"  
MIN = 12
MAX = 14




for base, dirs,files in os.walk(DATASOURCE):
 co=0
 if base != DATASOURCE:
    if(len(files) >= MIN):
        
     pathParts = base.split("/")
     createFolder=pathParts[(len(pathParts)-1)]
     createFolderFull=DATADEST +"/"+ createFolder
        
     if os.path.exists(createFolderFull) == False:
      os.makedirs(createFolderFull)

     for Files in files:
        co += 1
        if(co > MAX):
         break

        shutil.copyfile(DATASOURCE + "/" + createFolder + "/" + Files, DATADEST + "/" + createFolder + "/" + Files)
        #print(Files)
    
        
     
