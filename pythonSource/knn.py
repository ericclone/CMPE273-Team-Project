# References:
#   http://stackoverflow.com/questions/24385714/detect-text-region-in-image-using-opencv
#   http://blog.steven5538.tw/2015/06/02/CAPATHA-ocr-using-python-opencv/

import cv2
import numpy as np

def getTextBlocks(file_name ):
    img  = cv2.imread(file_name)
    img_final = cv2.imread(file_name)
    img2gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(img2gray , img2gray , mask =  mask)
    ret, new_img = cv2.threshold(image_final, 180 , 255, cv2.THRESH_BINARY_INV)  # for black text
    
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3 , 3)) # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more 
    dilated = cv2.dilate(new_img,kernel,iterations = 5) # dilate , more the iteration more the dilation

    img2, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # get contours
    
    textRectArr = []
	
    for contour in contours:
        # get rectangle bounding contour
        x,y,w,h = cv2.boundingRect(contour)
		
        if w < 35 and h<35:
            continue

        crop_img = new_img[y:y+h, x:x+w]
        ret,crop_img = cv2.threshold(crop_img, 127, 255, cv2.THRESH_BINARY_INV) #reverse color of foreground and background
        textRectArr.append(crop_img)
        
    return textRectArr

def getLetterImgsOfOneText(textBlockImg):
    im2, contours, hierarchy = cv2.findContours(textBlockImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x:x[1])
    arr = []

    for index, (c, _) in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(c)
        add = True
        for i in range(0, len(arr)):
            if abs(cnts[index][1] - arr[i][0]) <= 3:
                add = False
                break
        if add:
            arr.append((x, y, w, h))
    
    textLetterImgs = []; #ex: ['C','M','P','E'], ['2','0','6']

    for index, (x, y, w, h) in enumerate(arr):
        letterSrcImg = textBlockImg[y: y + h, x: x + w]
        
        if(h < 15 or w < 10 or w > 20):
            continue	
        resized_image = cv2.resize(letterSrcImg, (20, 20))
        textLetterImgs.append(resized_image)
    return textLetterImgs

def testLetterImg(knn, imgTest):
    arrTest = []
    arrTest.append(imgTest)
    testData = np.array(arrTest)
    testData = testData.reshape(-1, 400).astype(np.float32)
    ret,result,neighbours,dist = knn.findNearest(testData,k=1)
    return chr(int(ret))

def getTrainSet(imgPath):

    trainImgs = []
    #according to the sequence of ASCII
	#add "/"
    trainLetterImgPath = imgPath + "slash.png"
    trainLetterImg = cv2.imread(trainLetterImgPath)
    trainLetterImg = cv2.cvtColor(trainLetterImg, cv2.COLOR_BGR2GRAY)
    trainImgs.append(trainLetterImg)
    #add 0-9
    for i in range(10):
        trainDigitImgPath = imgPath + str(i) + ".png"
        trainDigitImg = cv2.imread(trainDigitImgPath)
        trainDigitImg = cv2.cvtColor(trainDigitImg, cv2.COLOR_BGR2GRAY)
        trainImgs.append(trainDigitImg)
    #add ":"
    trainLetterImgPath = imgPath + "colon.png"
    trainLetterImg = cv2.imread(trainLetterImgPath)
    trainLetterImg = cv2.cvtColor(trainLetterImg, cv2.COLOR_BGR2GRAY)
    trainImgs.append(trainLetterImg)
    #add alphabet[a-zA-Z]
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    for letter in alphabet:
        trainLetterImgPath = imgPath + letter + ".png"
        trainLetterImg = cv2.imread(trainLetterImgPath)
        trainLetterImg = cv2.cvtColor(trainLetterImg, cv2.COLOR_BGR2GRAY)
        trainImgs.append(trainLetterImg)

    trainData = np.array(trainImgs)
    trainData = trainData.reshape(-1, 400).astype(np.float32)
    trainLabels = [[47],[48],[49],[50],[51],[52],[53],[54],[55],[56],[57],[58],[65],[66],[67],[68],[69],[70],[71],[72],[73],[74],[75],[76],[77],[78],[79],[80],[81],[82],[83],[84],[85],[86],[87],[88],[89],[90],[97],[98],[99],[100],[101],[102],[103],[104],[105],[106],[107],[108],[109],[110],[111],[112],[113],[114],[115],[116],[117],[118],[119],[120],[121],[122]]
    trainLabels = np.array(trainLabels)

    return trainData, trainLabels

def checkPre(knn, trainSetDir, marksheetImgPath, requiredPre):
    textBlockImgs = getTextBlocks(marksheetImgPath)

    #generate the text in string according to its image
    texts = []
    ######for UT##########################################
    #letterImgsOfOneText = getLetterImgsOfOneText(textBlockImgs[4])
    #text = ""
    #for letterImg in letterImgsOfOneText:
    #    text = text + testLetterImg(letterImg);
    #print text
    #return
    ######################################################

    for textBlockImg in textBlockImgs:
        text = ""
        letterImgsOfOneText = getLetterImgsOfOneText(textBlockImg)
        #test each letter image and then generate the word in string type 
        for letterImg in letterImgsOfOneText:

            text = text + testLetterImg(knn, letterImg);
        texts.append(text)
    #check if required prerequisites has been found in the mark sheet 
    foundPres = []
    for pre in requiredPre:
       if pre in texts:
            foundPres.append(pre)
    return foundPres

def test():
    trainSetDir = "D:\\Study\\python\\opencv\\myChainSet\\20x20\\"
    marksheetImgPath = "D:\\Study\\python\\opencv\\solution1\\img\\marksheet4.png"
    trainData, trainLabels = getTrainSet(trainSetDir)
    #the 2 lines below will be put in init function on server
	knn = cv2.ml.KNearest_create()
    knn.train(trainData, cv2.ml.ROW_SAMPLE, trainLabels)

    requiredPre = ["202", "206", "248"]
    foundPres = checkPre(knn, trainSetDir, marksheetImgPath, requiredPre)
    print foundPres

test()