#NECESSARY LIBRARIES
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from flask import Flask, Response ,send_file, after_this_request

app = Flask(__name__)


############ FACE RECOGNITION CODE ###############################################################################################################################

path = 'Images'
images = []
studentNames =[]
myList = os.listdir(path)
print(myList)

for FL in myList:
    curImg = cv2.imread(f'{path}/{FL}')
    images.append(curImg)
    studentNames.append(os.path.splitext(FL)[0])

print(studentNames)

#ENCODES THE IMAGES STORED IN THE IMAGES FOLDER
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = None

#CODE TO MARK ATTENDANCE OF THE STUDENT IN THIS FILE
def attendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time_now = datetime.now()
            tStr = time_now.strftime('%H:%M:%S')
            dStr = time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n{name},{dStr},{tStr}')


#Delete Attendance Data


known_face_encodings = findEncodings(images)           

face_locations = []
face_names = []
face_encodings = []
process_this_frame = True
limit = 0



#MAIN CODE STARTS HERE
def frame_gen():
    video_capture = cv2.VideoCapture(0)
    global limit
    while limit<100:
        #IF NO FACES ARE DETECTED, THIS LIMIT WILL INCREMENT TILL IT REACHES IT'S MAX VALUE THEN THE LOOP WILL BE TERMINATED
        limit=limit+1

        #GRABS A SINGLE FRAME FROM THE WEBCAM FEED
        success, frame = video_capture.read()

        if not success :
            video_capture.release()
            break
        
        else :
            #RESIZES THE FRAME TO DETECT FACE BETTER
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            #CONVERTS THE FRAME TO RGB COLOR
            rgb_small_frame = small_frame[:, :, ::-1]

            #STORES ALL FACES AND IT'S ENCODINGS IN THESE GLOBAL LISTS USING THE FACE RECOGNITION LIBRARY FUNCTIONS
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "NOT REGISTERED"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = studentNames[best_match_index]
                    attendance(name)
                    #RESETS THE LIMIT
                    limit=0
                    
                face_names.append(name)


            #CODE DISPLAYS THE RESULT IN A RECTANGLE BOX WITH THE STUDENT'S NAME ON THE BOTTOM            
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                #SCALES THE IMAGES BACK TO ORIGINAL SIZE
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                name = name.upper()

                #DRAW RECTANGLE AROUND THE FACE
                cv2.rectangle(frame, (left-5, top-10), (right+5, bottom+10), (0, 255, 0), 2)

                #LABEL WITH NAME ON IT
                cv2.rectangle(frame, (left-5, bottom - 30), (right+5, bottom+10), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(frame, name, (left + 2, bottom - 2), font, 0.9, (255, 255, 255), 2)

            #DISPLAYS EACH AND EVERY FRAME THE CAMERA CAPTURE
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    limit=0
    video_capture.release()
    return ("ATTENDANCE IS SUCCESSFULLY TAKEN")
#################################################################################################################################################################

#ROUTES OF THE REQUESTS FROM FRONTEND
@app.route('/webcam')
def webcam():
    return Response(frame_gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/download')
def attendance_csv():
    return send_file('Attendance.csv', mimetype='text/csv', attachment_filename='Attendance.csv', as_attachment=True)

if __name__ == '__main__':
   app.run(debug=True)






