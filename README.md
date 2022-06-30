# Imager-Object-Detection
Object Detection Application with a frontend built using ReactJS, backend built using Flask and Model is based on Tiny-Yolo v3.

The Application has 3 parts:
- client 
- server
- yolo model


## Client
```
cd client
npm install
npm start
```

## Server
```
cd server
```
### virtaul environment
```
pip3 install virtualenv
python -m virtualenv venv 
venv/Scripts/activate
deactivate 
```
### To run Flask server:
```
pip install -r requirements.txt
flask run
$env:FLASK_ENV = "development"
```

## Model
Pull the docker image from [dockerhub](https://hub.docker.com/r/ekansh18/tfs)

create a container: 
```
docker run -p 8501:8501 \
--mount type=bind,source={source path to model},target=/models/yolo
-e MODEL_NAME=yolo -t tensorflow/serving &
```
the model will be running on http://localhost:8501/v1/models/yolo
