import cv2
import sys
import glob
import os
import time
import imutils

from datetime import datetime


#https://pyimagesearch.com/2021/04/19/face-detection-with-dlib-hog-and-cnn/

minPx = 299 # минимальный размер лица в пикселеях по высоте или ширине

#DATASOURCE = "/Applications/MAMP/htdocs/video.proj/data"
DATASOURCE = "/Volumes/Seagate Exp/data/celeb"
DATADEST = "/Volumes/Seagate Exp/data/celeb_face"

DNN = "CAFFE"
if DNN == "CAFFE":
        modelFile = "./res10_300x300_ssd_iter_140000_fp16.caffemodel"
        configFile = "./deploy.prototxt.txt"
        net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
else:
        modelFile = "./opencv_face_detector_uint8.pb"
        configFile = "./opencv_face_detector.pbtxt.txt"
        net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)



start = time.time()


for base, dirs,files in os.walk(DATASOURCE):
    #print('Searching in : ',base)

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
            h, w, c = image.shape
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)



            counter=int(0)


            blob = cv2.dnn.blobFromImage(rgb, 1.0, (300, 300), [104, 117, 123], False, False)

            conf_threshold=0.3
            
            net.setInput(blob)
            
            detections = net.forward()
            
            for i in range(detections.shape[2]):
                    confidence = detections[0, 0, i, 2]
                    if confidence > conf_threshold:
                        x1 = int(detections[0, 0, i, 3] * w)
                        y1 = int(detections[0, 0, i, 4] * h)
                        x2 = int(detections[0, 0, i, 5] * w)
                        y2 = int(detections[0, 0, i, 6] * h)


                        #print(imagePathDest)
                        #print(detections.shape[2])
                        
                        #print(str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2))

                        counter=int(counter)+1
                        #cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        #status = cv2.imwrite(imagePathDest, image)
                        #continue
                        
            
                        x3 = x2 - x1
                        y3 = y2 - y1
                        hX = x3 / 4 #добавление отступов на 1/4 от ширины и высоты
                        hY = y3 / 4 #добавление отступов на 1/4 от ширины и высоты
                        nX1 = x1 - hX
                        nX2 = x2 + hX
                        nY1 = y1 - hY
                        nY2 = y2 + hY

                        if(nX2 > w):
                          nX2 = x2
                        if(nY2 > h):
                          nY2 = y2
                
                        if(nX1 < 0):
                          nX1 = 0                
                        if(nY1 < 0):
                          nY1 = 0

                        sizeH = nY2 - nY1
                        sizeW = nX2 - nX1
              
                        if((sizeH >= minPx) & (sizeW >= minPx)):#если ширина или высота морды с отступом больше лимита minPx

                         scale=1.0
                         if(sizeH > sizeW):
                           scale = sizeH / sizeW
                           nSizeW = int(minPx)
                           nSizeH = int((minPx * scale))
                         elif(sizeW > sizeH):
                           scale = sizeW / sizeH
                           nSizeH = int(minPx)
                           nSizeW = int((minPx * scale))             
                         else:
                           nSizeH = int(minPx)
                           nSizeW = int(minPx)

                         croped=image[int(nY1):int(nY2), int(nX1):int(nX2)]
                         #print("CROPE: X-W " + str(nX1) + " / " + str(nX2) + " Y-H " + str(nY1) + " / " + str(nY2))
                         #print("NSIZE:" + str(nSizeW) + " " + str(nSizeH))
                         try:
                          resized = cv2.resize(croped, (nSizeW, nSizeH), interpolation = cv2.INTER_LINEAR)
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
