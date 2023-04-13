import cv2

img= cv2.imread(r'C:\Users\Michael\Desktop\2.jpg')
filename = r'C:\Users\Michael\Desktop\captions\sdf.jpg'
cv2.imwrite(filename, img)