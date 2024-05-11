import cv2
import sys
import glob
import os
import time
import imutils
import numpy as np
import shutil
import face_recognition

"""
 анализирует лица в папке DATASOURCE сравнивая их друг с другом в одной папке, затем сортирует по большему колличеству одного лица в папке и копирует в папку с отобранным лицом в папку DATADEST
"""

DATASOURCE = "/Volumes/Seagate Exp/data/models_face"
DATADEST = "/Volumes/Seagate Exp/data/models_filtered"




start = time.time()


for base, dirs,files in os.walk(DATASOURCE):
    #print('Searching in : ',base)

   
   face = {}
   skipList = []
   
   
   for f in files:

    if(f[:1] == "."):
        continue

    if f in skipList:
       print("Skip already compared file loop 1 " + f)
       continue
    
    imagePath=base+"/"+f
    
    print("File testing: " + imagePath)

    known_face_encodings = []
    known_face_names = []
    face[str(f)] = []

   

    fr = face_recognition.face_encodings(face_recognition.load_image_file(imagePath))
             
    if len(fr) > 0:
     known_face_encodings.append(fr[0])
     known_face_names.append(f)

    if(len(known_face_names) == 0):
        print("Not found face in " + f)
        continue #Skip if not found face
    
    for Files in files:

      if Files in skipList:
       #print("Skip already compared file loop 2 " + Files)
       continue


      if(Files[:1] != "."):
        imagePath=base+"/"+Files
        #print(len(known_face_encodings))
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        
        frame = cv2.imread(imagePath)
        rgb_small_frame = frame[:, :, ::-1]
        #print(frame)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            #print(face_distances)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

###########################
        for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                #top *= 4
                #right *= 4
                #bottom *= 4
                #left *= 4

                # Draw a box around the face
                #cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                #font = cv2.FONT_HERSHEY_DUPLEX
                #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 255), 1)





                if name != "Unknown":
                  #print("f=" + f + " name=" + Files)
                  if str(Files) not in skipList:# добавляет распознаный файл в скиплист чтобы пропустить повторяющийся анализ схожести
                     skipList.append(Files)
                  if str(f) != str(Files):
                   face[str(f)].append(str(Files))
                   #print("NAME: " + Files)



   #print("---------------------------------")
   #print(face)
   #print("---------------------------------")
   
   for k in sorted(face, key=lambda k: len(face[k]), reverse=True):
      
      pathParts = base.split("/")
      createFolder=pathParts[(len(pathParts)-1)]
      createFolderFull=DATADEST +"/"+ createFolder
      if os.path.exists(createFolderFull) == False:
       os.makedirs(createFolderFull)

      print("Copy File: " + k)
      shutil.copyfile(base + "/" + str(k), createFolderFull + "/" + str(k))
      for cfile in face[k]:
       print("Copy File: " + cfile)
       shutil.copyfile(base + "/" + str(cfile), createFolderFull + "/" + str(cfile))
      break #break loop after first element


        
        
            


    
#print(totalDir)
end = time.time()
print("[INFO] face detection took {:.4f} seconds".format(end - start))

