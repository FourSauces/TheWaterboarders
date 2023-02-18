import cv2
import os
import face_recognition

my_path = "/Users/judyliu/Documents/treehacks2023/TheWaterboarders/opencv-webcam"
os.chdir(my_path + "/source_code/")

# Load Camera
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print(ret)

while True:
    try:
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) == 0:
            continue
        middle_point = (frame.shape[1] // 2, frame.shape[0] // 2)
        closest_face_location = min(face_locations, key=lambda loc: (loc[0]+loc[2] - middle_point[0])**2 + (loc[1]+loc[3] - middle_point[1])**2)
        top, right, bottom, left = closest_face_location
        the_center = ((left+right)//2, (top+bottom)//2)
        print(the_center)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = cap.read()
    except Exception as e:
        print(e)
        break

cap.release()
cv2.destroyAllWindows()

