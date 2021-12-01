import cv2 

from deepface import DeepFace

img = cv2.imread('happyjun.jpg')

print((img))
#img = cv2.resize(img, dsize=(545,720), interpolation=cv2.INTER_AREA)




# predictions = DeepFace.analyze(img)
# print(predictions)
# print(predictions['dominant_emotion'])
# img1 = cv2.imread('angry_boy.jpg')
# cv2.imshow('image1',img1)
# predictions1 = DeepFace.analyze(img1)
# print(predictions1)
# print(predictions1['dominant_emotion'])