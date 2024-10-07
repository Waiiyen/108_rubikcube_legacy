import time
import os
import requests
import sys

imageByteStream = None
returnCode = os.system('fswebcam -r 1280x720 -S 1 -q color/color.jpg') # Use this line for webcam.