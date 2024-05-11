import cv2
import sys
import glob
import os
import time
import imutils
import numpy as np
import face_recognition

from datetime import datetime


#https://pyimagesearch.com/2021/04/19/face-detection-with-dlib-hog-and-cnn/

minPx = 299 # минимальный размер лица в пикселеях по высоте или ширине
coef = 1.2 # добавляет отступ от лица /коэфициент от размера лица// не использовать 5 вконце


DATASOURCE = "/Volumes/Seagate Exp/data/models"
DATADEST = "/Volumes/Seagate Exp/data/models_face"




start = time.time()


for base, dirs,files in os.walk(DATASOURCE):
    #print('Searching in : ',base)

    pathParts = base.split("/")
    existsFolder = DATADEST + "/" + pathParts[(len(pathParts)-1)]
    if os.path.exists(existsFolder) != False:#пропускать если папка уже есть в папке назначения 
        continue #хорошо бы удалить последнюю папку если перезапуск скрипта по сбою

    for Files in files:
         
        
        #print(base+"/"+Files);
        if(Files[:1] != "."):
    
            imagePath=base+"/"+Files
            pathParts = base.split("/")
            createFolder=pathParts[(len(pathParts)-1)]
            createFolderFull=DATADEST +"/"+ createFolder
            imagePathDest=createFolderFull + "/" + Files
        
            if os.path.exists(createFolderFull) == False:
                    os.makedirs(createFolderFull)

        

            image = cv2.imread(imagePath)
            
            try:
             rgb_small_frame = image[:, :, ::-1]
            except Exception as e:
                continue
            
            face_locations = face_recognition.face_locations(rgb_small_frame)

            #print(imagePath)
            #print(face_locations)

            

            counter=int(0)


            
            for fa in face_locations:
                counter=int(counter)+1

                x1 = fa[3]
                y1 = fa[0]
                x2 = fa[1]
                y2 = fa[2]
                w = x2 - x1
                h = y2 - y1
                nW = int(w * coef)
                nH = int(h * coef)
                ww = nW - w
                hh = nH - h

                
                
                resW = nW
                resH = nH
                
                if(nW < minPx or nH < minPx):# skip if face to small
                    continue
                print("w: " + str(w) + " h: " + str(h) + " im:" + Files)
                

                #cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                #status = cv2.imwrite(imagePathDest, image)
                #continue
                        
            
                croped=image[int(y1 - (hh / 2)):int(y2 + (hh / 2)), int(x1 - (ww / 2)):int(x2 + (ww / 2))]
                 #croped=image[int(nY1):int(nY2), int(nX1):int(nX2)]
                 #print("CROPE: X-W " + str(nX1) + " / " + str(nX2) + " Y-H " + str(nY1) + " / " + str(nY2))
                 #print("NSIZE:" + str(nSizeW) + " " + str(nSizeH))
                try:
                  resized = cv2.resize(croped, (resW, resH), interpolation = cv2.INTER_LINEAR)

                  nImagePathDest=imagePathDest + "." + str(counter) + ".jpg"                  
                  cv2.imwrite(nImagePathDest, resized)
                          
                except Exception as e:
                          
                  print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Error: path=" + nImagePathDest + " Folder: " + createFolder + str(e))
                  #exit

                    


        
        
            


        #for directories in dirs:
        #    totalDir += 1
        #for Files in files:
        #    totalFiles += 1
    
#print(totalDir)
end = time.time()
print("[INFO] face detection took {:.4f} seconds".format(end - start))
