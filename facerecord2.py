import cv2
import os
import face_recognition
import threading
import time

class WebcamRecorder:    
    def __init__(self, filename):
        self.filename = filename
        self.frame = None
        self.centerFace = (-1, -1)
        self.isRecording = False
        self.frames = []
        self.prevFaces = []
        self.fps = 60
        self.stop_event = threading.Event()
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        t = threading.Thread(target=self.updateFrameLoop)
        t.start()
        g = threading.Thread(target=self.updatePositionsLoop)
        g.start()

    def get_face_center(self, frame):
        try:
            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            if not face_locations:
                print("No face detected")
                return (-1, -1)

            middle_point = (frame.shape[1] // 2, frame.shape[0] // 2)
            closest_face_location = min(face_locations, key=lambda loc: (loc[0]+loc[2] - middle_point[0])**2 + (loc[1]+loc[3] - middle_point[1])**2)
            top, right, bottom, left = closest_face_location
            return ((left+right)//2, (top+bottom)//2)
        except:
            return (-1, -1)
    
    def updateFrame(self):
        ret, frame = self.cap.read()

        if ret:
            self.frame = frame
            if self.isRecording:
                self.frames.append(frame)

    def updateFrameLoop(self):
        while not self.stop_event.is_set():
            self.updateFrame()
    
    def updatePositionsLoop(self):
        while not self.stop_event.is_set():
            self.centerFace = self.get_face_center(self.frame)
            print("Center of face", self.centerFace)
            self.prevFaces.append(self.centerFace)
            if len(self.prevFaces) > 2:
                self.prevFaces.pop(0)

    def save(self):
        self.isRecording = False
        if not self.frames:
            return

        height, width, channels = self.frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.filename, fourcc, self.fps/6, (width, height))
        for frame in self.frames:
            out.write(frame)
            time.sleep(1/self.fps)
        out.release()
        self.frames = []

    def stop(self):
        self.stop_event.set()

if __name__ == "__main__":
    recorder = WebcamRecorder("output.mp4")
    print("Recorder initialized")
    recorder.start()
    print("Recording started")
    recorder.isRecording = True
    time.sleep(5)
    print("About to save")
    try:
        os.remove(os.path.join(os.getcwd(), "output.mp4"))
    except FileNotFoundError:
        print("File does not exist")
    recorder.save()
    print("Saved")
    recorder.stop()
