# Code written with video tutorial by Idently on YouTube

import face_recognition
import os, sys
import cv2 as cv
import numpy as np
import math

# caluclate accuracy percentage

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_value = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round((linear_value * 100, 2))) + '%'
    else:
        value = (linear_value + ((1.0 - linear_value) + math.pow((linear_value - 0.5) * 2, 0.2))) * 100 - 100
        return str(round(value, 2)) + '%'

class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True # use this to only process every other frame

    def __init__(self):
        self.encode_faces()

    def get_face_names(self):
        return [x.split()[0] for x in self.face_names]

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f'faces/{image}')
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding) # the encoding (128 features) of the first image :) 
            self.known_face_names.append(os.path.splitext(image)[0])
        print(self.known_face_names)

    def run_recognition(self):
        video_capture = cv.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found :(')

        while True:
            ret, frame = video_capture.read()
            
            if self.process_current_frame:
                small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv.cvtColor(small_frame, cv.COLOR_BGR2RGB)


                # Find all faces in current frame
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    # defaults for faces that we detect, but cannot recognize
                    name = 'Unknown'
                    confidence = 'Unknown'

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name} ({confidence})')

            self.process_current_frame = not self.process_current_frame

            # display annotations

            for (top, right, bottom, left), name, in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
                cv.putText(frame, name, (left + 6, bottom - 6), cv.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            cv.imshow('Face Recognition', frame)

            if cv.waitKey(1) == ord('q'):
                break

        video_capture.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
