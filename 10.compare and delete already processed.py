import sys
import glob
import os
import shutil

"""
 удаляет папки из DESTSOURCE если эти папки есть в DATASOURCE
 
"""

DATASOURCE = "/Volumes/Seagate Exp/data/imdb_face"
DESTSOURCE = "/Volumes/Seagate Exp/data/imdb"  #удалят папки отсюда





for base, dirs,files in os.walk(DATASOURCE):
    
 
 if base != DATASOURCE:
     tmp = base.split("/")
     fold = tmp[-1]
     print(fold)
     todel = DESTSOURCE + "/" + str(fold)
     try:
      shutil.rmtree(todel)
     except OSError as e:
      print("Error: %s - %s." % (e.filename, e.strerror))
     
