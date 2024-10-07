import cv2 
import numpy as np 

cap = cv2.VideoCapture(0)  # '0' represents the default camera
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# Read and display frames from the camera
while True:
    # Read a frame from the camera

    # Read a frame from the camera
    ret, img = cap.read()
    # cv2.convertScaleAbs(img, 0.1, -0)
    cv2.imshow("Camera Feed", img)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close any open windows
cap.release()
cv2.destroyAllWindows()


