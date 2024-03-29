# Automated-Attendance-System-Python

## SOLUTION PROPOSED
The objective of the solution is to reduce proxying, reduce time and effort taken to record the attendance.
The above mentioned objective is achieved by :
<ul>
  <li>Verifying and authenticating the student identity</li>
  <li>Verifyng the current location of the student</li>
</ul>
<b> Verification and authentication of student identity </b> is achieved using the <b> facial recognition </b> of the student along with
their roll number. <br>
<b> Student's current location </b> is verified by collecting their current <b> latitude </b> and <b> longitude </b> coordinates. <br>

## ADVANTAGES
<ul>
  <li>Affordable</li>
  <li>OS Independent and Device Independent (Can be used in any OS as it is hosted in web)</li>
  <li>Students can post attendance from any device even if they forgot their devices at home</li>
</ul>

## FRONTEND

### WORKING
This repo contains the react application that handles the working of frontend in the automated attendance system. Users need to enter
their roll numbers and capture a picture. These details along with location and timestamp is sent to the backend. The details of the
location is fetched using the geolocation api available in react.

### APIs USED
<ul>
  <li>React - Geolocation</li>
  <li>React - Webcam</li>
</ul>

### TOOLS USED
<ul>
  <li>ReactJS</li>
</ul>

## BACKEND

### WORKING
This repo contains the flask application that handles the working of backend in the automated attendance system. <br>

#### API ENDPOINTS
##### /api/attendance (POST) : 
This api endpoint receives the roll number of the student, current latitude and longitude, image of the student and timestamp when the
request was made. With the given timestamp and the roll number of the student, the hall and course code along with the faculty for which attendance needs to be recorded is identified with the help of timetable stored in the database. <br><br>
The <b> facial image </b> received from the frontend is compared with the already recorded facial image of that particular student available in the database in order to <b> verify the identity of the student </b>. <br><br>
The coordinates collected is compared with the already stored four corner coordinates of each hall. If the collected point lies in between the
four coordinates, then it can be confirmed that the student is within the classroom. <br><br>
If the above mentioned verifications are successfully passed then the student is provided attendance for that particular course. <br>

### APIs USED
<ul>
  <li>ImageKit.io</li>
  <li>facepplib</li>
  <li>pymongo</li>
</ul>

### TOOLS USED
<ul>
  <li>Python Flask</li>
  <li>MongoDB</li>
</ul>
