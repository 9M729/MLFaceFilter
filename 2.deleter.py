import sys
import glob
import os
import shutil

"""
 удаляет папки с фотками где фоток меньше лимита
 
"""

DATASOURCE = "/Volumes/Seagate Exp/data/imdb_filtered"
MIN = int(40)
MAX = int(80)



for base, dirs,files in os.walk(DATASOURCE):

 if base == DATASOURCE:
   continue
    
 counter = int(0)
 
     #print(base)
     
 for Files in files:

  if(Files[:1] != "."):
    counter = int(counter) + 1
    if(counter > MAX):
     #print("to delete file " + Files + "count:" + str(counter))  
     os.remove(base + "/" + Files)


 if counter < MIN:
  try:
   #print("to delete dir " + base + "count:" + str(counter))  
   shutil.rmtree(base)
  except OSError as e:
   print("Error: %s - %s." % (e.filename, e.strerror))
 else:
   #print("not delete" + base + "count:" + str(counter))
   op=0

print("END")

