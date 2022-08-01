from __future__ import print_function, unicode_literals
import time
import os
import base64
from datetime import datetime
from pymongo import MongoClient
from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from facepplib import FacePP, exceptions
from imagekitio import ImageKit

face_detection = ""
faceset_initialize = ""
face_search = ""
face_landmarks = ""
dense_facial_landmarks = ""
face_attributes = ""
beauty_score_and_emotion_recognition = ""

imagekit = ImageKit(
    private_key = 'private_WrxZPJhyTPfaW7fg+vVhdYcA+xM=',
    public_key = 'public_zskDEmBVQzt/Rz7rdX3lwqNwm60=',
    url_endpoint = 'https://ik.imagekit.io/rf39vtebd')

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r'/api/*': {'origin': 'http://127.0.0.1:3000'}})

cluster = MongoClient("mongodb+srv://aas:hackathon@aas.2kkkz.mongodb.net/SAS?retryWrites=true&w=majority")
db = cluster["SAS"]

student = db["Student"]
faculty = db["Faculty"]
hall = db["Hall"]
timetable = db["Timetable"]
timing = db["Timing"]

def face_comparing(app, Image1, Image2):
    cmp_ = app.compare.get(image_url1=Image1, image_url2=Image2)

    if cmp_.confidence > 70:
        print('BOTH FACES ARE SAME ...')
        return True
    else:
        print('BOTH FACES ARE NOT SAME ...')
        return False

def checkFace(link1, link2):
    api_key = 'xQLsTmMyqp1L2MIt7M3l0h-cQiy0Dwhl'
    api_secret = 'TyBSGw8NBEP9Tbhv_JbQM18mIlorY6-D'

    try:
        app_ = FacePP(api_key=api_key, api_secret=api_secret)
        
        funcs = [
            face_detection,
            faceset_initialize,
            face_search,
            face_landmarks,
            dense_facial_landmarks,
            face_attributes,
            beauty_score_and_emotion_recognition
        ]

        image1 = link1
        image2 = link2
        
        return face_comparing(app_, image1, image2)
    
    except exceptions.BaseFacePPError as e:
        print('ERROR :', e)

def checkCoordinate(latitude, longitude, hall_id):
    hall_details = hall.find_one({"Hall_id": hall_id})

    x = [0 for _ in range(4)]
    y = [0 for _ in range(4)]

    c = 0
    for i in hall_details['Corners']:
        x[c] = float(hall_details['Corners']['C' + str(c + 1)]['Latitude'])
        y[c] = float(hall_details['Corners']['C' + str(c + 1)]['Longitude'])
        c = c + 1

    xmin = min(x)
    xmax = max(x)

    ymin = min(y)
    ymax = max(y)

    if latitude >= xmin and latitude <= xmax:
        if longitude >= ymin and longitude <= ymax:
            return True
        return False

    return False

class Attendance(Resource):
    def get(self):
        return {"Message": "Hello, World"}

    @cross_origin(supports_credentials=True)
    def post(self):
        rollno = request.form["rollno"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        image = request.form['image']

        rollno = rollno.upper()
        
        print("---------------------------SAVING IMAGE-------------------------------------")

        imgstr = image[image.index(",")+1: ]
        
        upload = imagekit.upload(
            file = imgstr,
            file_name = rollno + "_temp.jpg",
            options={},
        )

        image2 = upload['response']['url']

        print("---------------------------IMAGE SAVED-------------------------------------")

        student_details = student.find_one({"Rollno": rollno})

        t = str(time.strftime("%H:%M"))
        current_hour = int("09")#int(t[:t.index(":")])
        current_minutes = int("20")#int(t[t.index(":") + 1:])

        student_class = timetable.find_one({"Class": rollno[0:4]})
        current_day = str(datetime.today().strftime('%A'))

        class_timing = timing.find_one()
        for i in class_timing.keys():
            if(i != "_id"):
                start = class_timing[i]["Start"]
                end = class_timing[i]["End"]

                hour = int(start[ : start.index(":")])
                minutes = int(start[start.index(":") + 1 : ])

                if((hour == current_hour) and (minutes + 10 >= current_minutes) and (current_minutes >= minutes)):
                    current_course = student_class['Schedule'][str(current_day)][i]['Course_id']
                    current_hall = student_class['Schedule'][str(current_day)][i]['Hall_id']

                    print(i, "PRESENT")
                    print(current_course)
                    print(current_hall)

                    image1 = student.find_one({"Rollno": rollno})["image_url"]

                    if(checkFace(image1, image2)):
                        if(checkCoordinate(float(latitude), float(longitude), "SCL")):
                            student.find_one_and_update(
                                {"Rollno": rollno},
                                {"$set":
                                    {"Courses." + current_course: student_details['Courses'][current_course] + 1}
                                }, upsert=True
                            )
                            return {"message": "Attendance Recorded"}
                        else:
                            return {"message": "Out of Class Room"}   
                    else:
                        return {"message": "Face Authentication Failed"}

        return {"message": "Late to Class"}

@app.route("/")
def index():
    return "Welcome Back!"

api.add_resource(Attendance, "/api/attendance")

if __name__ == "__main__":
    app.run(debug=True)