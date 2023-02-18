import cv2
import os
import face_recognition
import threading
import time

my_path = "/Users/judyliu/Documents/treehacks2023/TheWaterboarders/opencv-webcam"
os.chdir(my_path + "/source_code/")
x_c = 0 
y_c = 0
class WebcamRecorder:
    def __init__(self, filename,duration):
        self.filename = filename
        self.duration = duration
        self.frames = []
        self.fps = 60
        self.stop_event = threading.Event()

    def start(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, self.fps)  # Set to 30 frames per second
        t = threading.Thread(target=self._record, args=(cap,))
        t.start()

    def stop(self):
        self.stop_event.set()

    def _record(self, cap):
        start_time = cv2.getTickCount()
        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                break
            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            if len(face_locations) == 0:
                print("nofacedetected")
                continue
            middle_point = (frame.shape[1] // 2, frame.shape[0] // 2)
            closest_face_location = min(face_locations, key=lambda loc: (loc[0]+loc[2] - middle_point[0])**2 + (loc[1]+loc[3] - middle_point[1])**2)
            top, right, bottom, left = closest_face_location
            the_center = ((left+right)//2, (top+bottom)//2)
            global x_c
            x_c = (left+right)//2
            global y_c
            y_c =  (top+bottom)//2
            print(the_center)
            # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            self.frames.append(frame)
        cap.release()
        cv2.destroyAllWindows()
        self._save()

    def _save(self):
        if len(self.frames) == 0:
            return
        height, width, channels = self.frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.filename, fourcc, self.fps/6, (width, height))  # reduce fps
        for frame in self.frames:
            out.write(frame)
            time.sleep(1/self.fps)  # wait between frames
        out.release()


recorder = WebcamRecorder("output.mp4", duration=2)
recorder.start()
input("Press enter to stop recording...")
recorder.stop()

