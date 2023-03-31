#pip install googletrans==4.0.0rc1
import googletrans
import cv2
import numpy as np

text1 = "この文は現在翻訳中です"

def translateToImage(text, filename):

    translator = googletrans.Translator()
    textIn = translator.translate(text, dest="en").text

    img = np.ones((296, 607, 3), dtype=np.uint8)
    img = 255 * img

    charList = []
    for character in textIn:
        charList.append(character)

    tempBool = False

    if (len(charList) >= 26):
        # TODO add
        print("Hello")
        counter = 0
        index = 0
        quitLoop = False
        while True:
            tempList = []
            for character in charList[index:]:
                quitLoop = False
                tempList.append(character)
                if character == " ":
                    nextLength = 0
                    for letter in charList[index + 1:]:
                        nextLength += 1
                        if letter == " ":
                            break
                    if len(tempList) + nextLength > 26:
                        quitLoop = True

                index += 1
                if len(tempList) == 26 or index == len(charList) or quitLoop:
                    break
                quitLoop = False

            if tempBool:
                break
            if index == len(charList):
                tempBool = True
            resultText = "".join(tempList)
            cv2.putText(img, resultText, (25, 35 + (counter * 50)), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 4, 2)
            counter += 1


    else:
        diff = (26 - len(charList))
        cv2.putText(img, textIn, (25, int(75 - (diff * 0.5))), cv2.FONT_HERSHEY_SIMPLEX, 1.2 + (diff * 0.08), (0, 0, 0),
                    4, 2)

    # cv2.putText(img, textIn, (25,35), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,0), 2, 2)

    cv2.imshow("Image", img)
    cv2.imwrite(filename, img)
    cv2.waitKey(0)


translateToImage(text1, "resultImage.jpg")
