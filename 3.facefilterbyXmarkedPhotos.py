import cv2
import sys
import glob
import os
import time
import imutils
import numpy as np
import face_recognition

"""
 Отобраные фото лица должны начинаться с x.
"""

DATASOURCE = "/Volumes/Seagate Exp/data/imdb_test"
DATADEST = "/Volumes/Seagate Exp/data/imdb_filtered"




start = time.time()


for base, dirs,files in os.walk(DATASOURCE):
    #print('Searching in : ',base)


    known_face_encodings = []
    known_face_names = []

    for Files in files:
         
        
        if(Files[:2] == "x."):
            print(base+"/"+Files);

            imagePath=base+"/"+Files
            #print(base)


            
            if Files[0:2] == "x.":
             print("-->" + Files)

             fr = face_recognition.face_encodings(face_recognition.load_image_file(imagePath))
             
             if len(fr) > 0:
               print("add")
               known_face_encodings.append(fr[0])
               known_face_names.append(Files)

    if(len(known_face_names) == 0):
        print("Skip not found x. files in " + base)
        continue #Skip if not found x. files and face array empty
    
    for Files in files:

      if(Files[:1] != "."):
        imagePath=base+"/"+Files
        print(len(known_face_encodings))
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
            print(face_distances)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

###########################
        for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                #cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                #font = cv2.FONT_HERSHEY_DUPLEX
                #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 255), 1)
                print("NAME: " + name)


                pathParts = base.split("/")
                createFolder=pathParts[(len(pathParts)-1)]
                createFolderFull=DATADEST +"/"+ createFolder
                if os.path.exists(createFolderFull) == False:
                    os.makedirs(createFolderFull)


                if name != "Unknown":
                  cv2.imwrite(createFolderFull + "/" + "" + Files, frame)
                #else:
                  #cv2.imwrite(createFolderFull + "/" + "U." + Files, frame)

"""
            pathParts = base.split("/")
            createFolder=pathParts[(len(pathParts)-1)]
            createFolderFull=DATADEST +"/"+ createFolder
            imagePathDest=createFolderFull + "/" + Files
        
            if os.path.exists(createFolderFull) == False:
                    os.makedirs(createFolderFull)

        

            image = cv2.imread(imagePath)
            #h, w, c = image.shape
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)



            #cv2.imwrite(imagePathDest, resized)
"""
                    


        
        
            


    
#print(totalDir)
end = time.time()
print("[INFO] face detection took {:.4f} seconds".format(end - start))
