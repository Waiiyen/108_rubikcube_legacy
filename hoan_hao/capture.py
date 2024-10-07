import cv2
import time
cap =cv2.VideoCapture(0)
img_counter = 0
time_start = time.time()
while True:
    ret, frame = cap.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(10)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        img_name = r"/home/asus/Desktop/image/img{}.png".format(img_counter)
        cv2.imwrite(img_name, frame) 
        print("{} written!".format(img_name))
        img_counter += 1.
        time_start = time.time()

cap.release()

cv2.destroyAllWindows()
