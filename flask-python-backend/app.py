from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
import yaml
import json
import jwt
import datetime
import hashlib, uuid  # for hashing
import random
import ssl
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
import myconfig

# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain('/etc/ssl/certs/nginx-selfsigned.crt', '/etc/ssl/private/nginx-selfsigned.key')
from trycourier import Courier
import os
from flask import flash, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
from os import path

app = Flask(__name__)
app.config['SECRET_KEY'] = myconfig.secretKey
app.config['PROPAGATE_EXCEPTIONS'] = True

config = yaml.safe_load(open('database.yaml'))
client = MongoClient(config['uri'])
# db = client.lin_flask
db = client['knf-dev']
cors = CORS(app)

otpDict = {}

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


errorclient = Courier(auth_token=myconfig.courierAuthToken1)
def sendErrorMessage(msg):
    resp = errorclient.send_message(
            message={
                "to": {
                "email": "ravensenterprises8@gmail.com",
                },
            "content": {
                "title": "Welcome to PharmDifficult!",
                "body": msg,
            },
            "data": {
                "name": "Pharm Difficult",
            },
            "routing": {
                "method": "single",
                "channels": ["email"],
            },
  }
)



def log_backend(message):
    f = open("backend_logs.txt", "a")
    currentTime = datetime.now() + timedelta(hours=5.5)
    f.write(f'{currentTime.strftime("%d/%m/%Y %H:%M:%S")} '+message+'\n')
    f.close()

def hash_file(filename):
    if path.isfile(filename) is False:
        raise Exception("File not found for hash operation")

    h_sha256 = hashlib.sha256()

    with open(filename, 'rb') as file:

        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h_sha256.update(chunk)

    return h_sha256.hexdigest()


UPLOAD_FOLDER = "/home/iiitd/flask-python-backend/allFiles/"
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = Courier(auth_token=myconfig.courierAuthToken2)
@app.route('/api/v1/email', methods=['POST'])
def sendOTP():
    global otpDict
    otp = random.randint(100000, 999999)
    if request.method == 'POST':
        body = request.json
        emailID = body['email']
        print("recieved", emailID)
        message = "Your OTP is "+str(otp)
        print(message)
        otpDict[emailID] = str(otp)

        log_backend("New registration with email ID "+emailID+" and otp sent is "+str(otp))
        resp = client.send_message(
            message={
                "to": {
                "email": emailID,
                },
            "content": {
                "title": "Welcome to PharmDifficult!",
                "body": message,
            },
            "data": {
                "name": "Pharm Difficult",
            },
            "routing": {
                "method": "single",
                "channels": ["email"],
            },
  }
)

    return jsonify({
        'status': "otp has been sent!",
    })


@app.route('/api/v1/3ACE60B0A0C1B6C9345E31494142947AA97D4EF4912E895D8795663393819759')
def secretRestart():
    os.system('sudo /home/iiitd/flask-python-backend/restart.sh')
    return render_template('restart.html', message="Hello!")


@app.route('/api/v1/verifyOtp', methods=['POST'])
def verify():
    global otpDict
    print('inside verify', otpDict)
    if request.method == 'POST':
        body = request.json
        emailID = body['email']
        otp = body['otp']
        print('original', otpDict)
        print("recieved", emailID, otp)
        if emailID in otpDict.keys():
            if otp == otpDict[emailID]:
                log_backend("Registration with email id "+emailID+" entered correct OTP and was registered")
                del otpDict[emailID]
                return jsonify({
                    'verified': 1,
                })
    log_backend("Registration with email id "+emailID+" entered wrong OTP and was not allowed to register")
    return jsonify({
        'verified': 0,
    })

@app.route('/api/v1/users/register', methods=['POST'])
def registerUser():
    print("reached register route")
    
    if request.method == 'POST':
        print(request)
        params = request.json
        print("put params is ", params)
        stakeholder = params['stakeHolder']
        if(stakeholder == "patient"):
            if params['request'] == 'register':
                print('register patient received params', params)
                updatedData = {}
                updatedData['name'] = params['name']
                updatedData['phone'] = params['phoneNo']
                updatedData['email'] = params['email']
                updatedData['wallet_address'] = params['wallet_address']
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Patient data with email ' + params['email'] + ' has been updated!')
                return jsonify({'status': 'Patient data with email ' + params['email'] + ' has been updated!'})

        elif stakeholder == "doctor":
            if params['request'] == 'register':
                print('register doctor received params', params)
                updatedData = {}
                updatedData['name'] = params['name']
                updatedData['phone'] = params['phoneNo']
                updatedData['email'] = params['email']
                updatedData['licenceNo'] = params['licenceNo']
                updatedData['wallet_address'] = params['wallet_address']
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Doctor data with email ' + params['email'] + ' has been updated!')
                return jsonify({'status': 'Doctor data with email ' + params['email'] + ' has been updated!'})
            
        
            else:
                print('\n # Invalid user $ \n')
                # Return some error JSON

        elif stakeholder == "hospital":
            if params['request'] == 'register':
                print('register hospital received params', params)
                updatedData = {}
                updatedData['name'] = params['name']
                updatedData['phone'] = params['phoneNo']
                updatedData['email'] = params['email']
                updatedData['licenceNo'] = params['licenceNo']
                updatedData['wallet_address'] = params['wallet_address']
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Hospital data with email ' + params['email'] + ' has been updated!')
                return jsonify({'status': 'Hospital data with email ' + params['email'] + ' has been updated!'})

        
            else:
                print('\n # Invalid user $ \n')
                # Return some error JSON
        
        elif stakeholder == "insurance":
            if params['request'] == 'register':
                print('register insurance received params', params)
                updatedData = {}
                updatedData['name'] = params['name']
                updatedData['phone'] = params['phoneNo']
                updatedData['email'] = params['email']
                updatedData['licenceNo'] = params['licenceNo']

                updatedData['wallet_address'] = params['wallet_address']
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Insurace data with email ' + params['email'] + ' has been updated!')
                return jsonify({'status': 'Insurace data with email ' + params['email'] + ' has been updated!'})

        
            else:
                print('\n # Invalid user $ \n')
                # Return some error JSON
        
        elif stakeholder == "pharmacy":
            if params['request'] == 'register':
                print('register pharmacy received params', params)
                updatedData = {}
                updatedData['name'] = params['name']
                updatedData['phone'] = params['phoneNo']
                updatedData['email'] = params['email']
                updatedData['licenceNo'] = params['licenceNo']
                updatedData['wallet_address'] = params['wallet_address']
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Pharmacy data with email ' + params['email'] + ' has been updated!')
                return jsonify({'status': 'Patient data with email ' + params['email'] + ' has been updated!'})

            
            else:
                print('\n # Invalid user $ \n')
                log_backend('Invalid user tried updating data')
                return jsonify({'status': 'Error: Invalid user!'})
        else:
            print("Not a valid user!")


@app.route('/')
def index():
    return render_template('index2.html', message="Hello!")

@app.route('/api/v1/users', methods=['POST', 'GET'])
def data():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        stakeholder = body['stakeholder']
        allData = db[stakeholder].find()
        for data in allData:
            if data['email'].lower() == body['email'].lower():
                print('email already exists, exiting')
                log_backend("User tried registering with same email id")
                return jsonify({
                'status': 0,
            })
                
        if(stakeholder == "patient"):
            registrationNum = 123456789  # Later, generate a sequential number for every new user
            db[stakeholder].insert_one({
                'registrationNum':body['registrationNum'],
                'name':body['name'],
                'DOB':body['DOB'],
                'gender':body['gender'],
                'email':body['email'].lower(),
                'password': hashlib.sha256(body['password'].encode()).hexdigest(),  # Later, add salt as well
                'phone':body['phone'],
                'joiningDate':body['joiningDate'],
                'pcpID':body['pcpID'],
                'insuranceID':body['insuranceID'],
                'verifiedUser':0,
                'wallet_address': body['wallet_address']
            })
            log_backend('Patient created. Data is posted to MongoDB!')
            return jsonify({
            'status': 'Patient created. Data is posted to MongoDB!',
            })
        elif (stakeholder == "doctor"):
            db[stakeholder].insert_one({
                'licenceNo':body['licenceNo'],
                'name':body['name'],
                'DOB':body['DOB'],
                'gender':body['gender'],
                'email':body['email'],
                'password':hashlib.sha256(body['password'].encode()).hexdigest(),  # Later, add salt as well
                'phone':body['phone'],
                'specialty':body['specialty'],
                'location':body['location'],
                'joiningDate':body['joiningDate'],
                'consultationFee':body['consultationFee'],
                'verifiedUser':0,
                'wallet_address': body['wallet_address']
            })
            log_backend('Doctor created. Data is posted to MongoDB!')
            return jsonify({
            'status': 'Doctor created. Data is posted to MongoDB!',
            })
        elif (stakeholder == "pharmacy"):
            db[stakeholder].insert_one({
                'licenceNo':body['licenceNo'],
                'name':body['name'],
                'email':body['email'],
                'password':hashlib.sha256(body['password'].encode()).hexdigest(),  # Later, add salt as well
                'phone':body['phone'],
                'location':body['location'],
                'image1':body['image1'],
                'image2':body['image2'],                
                'joiningDate':body['joiningDate'],
                'verifiedUser':0,
                'wallet_address': body['wallet_address']
            })
            log_backend('Pharmacy created. Data is posted to MongoDB!')
            return jsonify({
                'status': 'Pharmacy created. Data is posted to MongoDB!',
                })
        elif (stakeholder == "insurance"):
            db[stakeholder].insert_one({
                'licenceNo':body['licenceNo'],
                'name':body['name'],
                'email':body['email'],
                'password':hashlib.sha256(body['password'].encode()).hexdigest(),  # Later, add salt as well
                'phone':body['phone'],
                'location':body['location'],
                'image1':body['image1'],
                'image2':body['image2'],
                'verifiedUser':0, 
                'wallet_address': body['wallet_address']
            })
            log_backend('Insurance created. Data is posted to MongoDB!')
            return jsonify({
            'status': 'Insurance created. Data is posted to MongoDB!',
            })
        elif (stakeholder == "hospital"):
            db[stakeholder].insert_one({
                'name':body['name'],
                'email':body['email'],
                'licenceNo':body['licenceNo'],
                'password':hashlib.sha256(body['password'].encode()).hexdigest(),  # Later, add salt as well
                'phone':body['phone'],
                'specialty':body['specialty'],
                'location':body['location'],
                'image1':body['image1'],
                'image2':body['image2'],
                'verifiedUser':0, 
                'wallet_address': body['wallet_address']
            })
            log_backend('Hospital created. Data is posted to MongoDB!')
            return jsonify({
            'status': 'Hospital created. Data is posted to MongoDB!',
            })
        
        return jsonify({
            'status': 'Failed to create a new user!',
        })
    
    # GET all data from database
    if request.method == 'GET':

        allData = db["pharmacy"].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            name = data['name']
            licenceNo = data['licenceNo']
            email = data['email']
            dataDict = {
                'id': str(id),
                'email': firstName,
                'licenceNo': licenceNo,
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)

@app.route('/api/v1/users/fetch', methods=['POST'])
def fetchUser():
    print("reached fetch route")
    params = request.json
    print('fetch request is: ', params)
    # GET a specific data by id
    if request.method == 'POST':
        print("fetch Params from back", params)
        # params = json.loads(params)
        stakeholder = params["stakeholder"]
        del params["stakeholder"]
        if 'password' in params.keys():
            inp = params['password']
            inp = hashlib.sha256(inp.encode()).hexdigest()
            params['password'] = inp
        uploader = ""
        if stakeholder == 'files':
            uploader = params['uploader']
            params = {}             
        print('GET user params', params)
        filter = {}
        for i in params.keys():
            if(not(params[i].lower() == 'none')):
                filter[i] = params[i]
        print(filter)
        dataJson = []
        allData = db[stakeholder].find(filter)

        print("stakeholder is", stakeholder)
        if stakeholder == 'doctor':
            for data in allData:
                id = data['_id']
                name = data['name']
                email = data['email']
                licence = data['licenceNo']
                # TODO: for nxt deadline remove this
                password = data['password']
                DOB = data['DOB']
                specialty = data['specialty']
                location = data['location']
                consultationFee = data['consultationFee']
                joiningDate = data['joiningDate']
                gender = data['gender']
                phone = data['phone']
                wallet_address = data['wallet_address']
                dataDict = {
                    'id': str(id),
                    'name' : name,
                    'email': email,
                    'licenceNo': licence, 
                    # TODO: for nxt deadline remove this
                    'DOB' : DOB,
                    'specialty' : specialty,
                    'location' : location,
                    'consultationFee' : consultationFee,
                    'joiningDate' : joiningDate,
                    'gender' : gender,
                    'phone' : phone,
                    'wallet_address': wallet_address
                }
                dataJson.append(dataDict)
                log_backend("fetch attempt by doctor email id "+email + 'successful!')

        elif stakeholder == 'pharmacy':
            print("stakeholder is pharmacy")
            for data in allData:
                id = data['_id']
                name = data['name']
                email = data['email']
                licence = data['licenceNo']
                # TODO: for nxt deadline remove this
                password = data['password']
                image1 = data['image1']
                image2 = data['image2']
                location = data['location']
                phone = data['phone']
                wallet_address = data['wallet_address']
                dataDict = {
                    'id': str(id),
                    'name' : name,
                    'email': email,
                    'licenceNo': licence, 
                    'image1':image1,
                    'image2':image2,
                    'location' : location,
                    'phoneNo' : phone,
                    'wallet_address': wallet_address
                }
                dataJson.append(dataDict)
                log_backend("fetch attempt by pharmacy email id "+email + 'successful!')

        elif stakeholder == 'insurance':
            print("stakeholder is insurance")
            for data in allData:
                print(data)
                id = data['_id']
                name = data['name']
                email = data['email']
                if('licenceNo' in data.keys()):

                    licence = data['licenceNo']
                else:
                    licence = data['licenceNo']
                # TODO: for nxt deadline remove this
                password = data['password']
                image1 = data['image1']
                image2 = data['image2']
                location = data['location']
                phone = data['phone']
                wallet_address = data['wallet_address']

                dataDict = {
                    'id': str(id),
                    'name' : name,
                    'email': email,
                    'licenceNo': licence, 
                    'image1':image1,
                    'image2':image2,
                    'location' : location,
                    'phoneNo' : phone,
                    'wallet_address': data['wallet_address']
                }
                dataJson.append(dataDict)
                log_backend("fetch attempt by insurance email id "+email + 'successful!')
                
        elif stakeholder == 'hospital':
            print('stakeholder is hospital')
            for data in allData:
                id = data['_id']
                name = data['name']
                email = data['email']
                licence = data['licenceNo']
                # TODO: for nxt deadline remove this
                password = data['password']
                specialty = data['specialty']
                image1 = data['image1']
                image2 = data['image2']
                location = data['location']
                phone = data['phone']
                wallet_address = data['wallet_address']

                dataDict = {
                    'id': str(id),
                    'name' : name,
                    'email': email,
                    # TODO: some values do not have licence number saved
                    # 'licenceNo': licence, 
                    'image1':image1,
                    'image2':image2,
                    'specialty' : specialty,
                    'location' : location,
                    'phoneNo' : phone,
                    'wallet_address': data['wallet_address']
                }
                dataJson.append(dataDict)
                log_backend("fetch attempt by hospital email id "+email + 'successful!')
        
        elif stakeholder == 'patient':
            for data in allData:
                id = data['_id']
                name = data['name']
                DOB = data['DOB']
                gender = data['gender']
                email = data['email']
                # TODO: for nxt deadline remove this
                password = data['password']
                phone = data['phone']
                joiningDate = data['joiningDate']
                pcpID = data['pcpID']
                insuranceID = data['insuranceID']
                wallet_address = data['wallet_address']

                dataDict = {
                    'id': str(id),
                    'name' : name,
                    'DOB' : DOB,
                    'gender' : gender,
                    'email': email,
                    'phoneNo' : phone,
                    'joiningDate' :joiningDate,
                    'pcpID' :pcpID,
                    'insuranceID': insuranceID,
                    'wallet_address': data['wallet_address']
                    
                }
                dataJson.append(dataDict)
                log_backend("fetch attempt by patient email id "+email + 'successful!')


        elif stakeholder == 'patient':
            for data in allData:
                id = data['_id']
                name = data['name']
                DOB = data['DOB']
                gender = data['gender']
                email = data['email']
                # TODO: for nxt deadline remove this
                password = data['password']
                phone = data['phone']
                joiningDate = data['joiningDate']
                pcpID = data['pcpID']
                insuranceID = data['insuranceID']
                wallet_address = data['wallet_address']

                dataDict = {
                    'id': str(id),
                    'name' : name,
                    'DOB' : DOB,
                    'gender' : gender,
                    'email': email,
                    'phoneNo' : phone,
                    'joiningDate' :joiningDate,
                    'pcpID' :pcpID,
                    'insuranceID': insuranceID,
                    'wallet_address': data['wallet_address']
                    
                }
                dataJson.append(dataDict)
                log_backend("fetch attempt by patient email id "+email + 'successful!')
    
        elif stakeholder == 'files':
            for data in allData:
                id = data['_id']
                fetchedUploader = data['uploader']
                accessList = data['access']
                if not ((fetchedUploader == uploader) or (uploader in accessList)):
                    continue
                originalFileName = data['originalFileName']
                stakeholderForFile = data['stakeholder']

                dataDict = {
                    'id': str(id),
                    'uploader': fetchedUploader,
                    'access': accessList,
                    'originalFileName': originalFileName,
                    'stakeholder': stakeholderForFile,
                }
                dataJson.append(dataDict)
                log_backend("Request for all files of a user made")

        return jsonify(dataJson)


@app.route('/api/v1/users/login', methods=['GET', 'DELETE', 'PUT', 'POST'])
def onedata():
    print("reached login route")
    params = request.json
    print('print request is: ', params)

    # GET a specific data by id
    if request.method == 'POST':
        print("Params from back", params)
        # params = json.loads(params)
        stakeholder = params["stakeholder"]
        del params["stakeholder"]
        if 'password' in params.keys():
            inp = params['password']
            inp = hashlib.sha256(inp.encode()).hexdigest()
            params['password'] = inp
        uploader = ""
        if stakeholder == 'files':
            uploader = params['uploader']
            params = {}             
        print('GET user params', params)
        filter = {}
        for i in params.keys():
            if(not(params[i].lower() == 'none')):
                filter[i] = params[i]
        print(filter)
        dataJson = []
        allData = db[stakeholder].find(filter)

        print("stakeholder is", stakeholder)
        if stakeholder == 'doctor':
            for data in allData:
                if data['verifiedUser']:
                    id = data['_id']
                    name = data['name']
                    email = data['email']
                    licence = data['licenceNo']
                    # TODO: for nxt deadline remove this
                    password = data['password']
                    DOB = data['DOB']
                    specialty = data['specialty']
                    location = data['location']
                    consultationFee = data['consultationFee']
                    joiningDate = data['joiningDate']
                    gender = data['gender']
                    phone = data['phone']
                    wallet_address = data['wallet_address']
                    dataDict = {
                        'id': str(id),
                        'name' : name,
                        'email': email,
                        'licenceNo': licence, 
                        # TODO: for nxt deadline remove this
                        'DOB' : DOB,
                        'specialty' : specialty,
                        'location' : location,
                        'consultationFee' : consultationFee,
                        'joiningDate' : joiningDate,
                        'gender' : gender,
                        'phone' : phone,
                        'wallet_address': wallet_address
                    }
                    dataJson.append(dataDict)
                    log_backend("Login attempt by doctor email id "+email + 'successful!')
                else:
                    log_backend("Login attempt by doctor email id "+data['email'] + 'unsuccessful. Admin approval required!')
                    return jsonify({'verifiedUser': 0})

        elif stakeholder == 'pharmacy':
            print("stakeholder is pharmacy")
            for data in allData:
                if data['verifiedUser']:
                    id = data['_id']
                    name = data['name']
                    email = data['email']
                    licence = data['licenceNo']
                    # TODO: for nxt deadline remove this
                    password = data['password']
                    image1 = data['image1']
                    image2 = data['image2']
                    location = data['location']
                    phone = data['phone']
                    wallet_address = data['wallet_address']
                    dataDict = {
                        'id': str(id),
                        'name' : name,
                        'email': email,
                        'licenceNo': licence, 
                        'image1':image1,
                        'image2':image2,
                        'location' : location,
                        'phoneNo' : phone,
                        'wallet_address': wallet_address
                    }
                    dataJson.append(dataDict)
                    log_backend("Login attempt by pharmacy email id "+email + 'successful!')
                else:
                    log_backend("Login attempt by pharmacy email id "+data['email'] + 'unsuccessful. Admin approval required!')
                    return jsonify({'verifiedUser': 0})
        elif stakeholder == 'insurance':
            print("stakeholder is insurance")
            for data in allData:
                if data['verifiedUser']:
                    print(data)
                    id = data['_id']
                    name = data['name']
                    email = data['email']
                    if('licenceNo' in data.keys()):

                        licence = data['licenceNo']
                    else:
                        licence = data['licenceNo']
                    # TODO: for nxt deadline remove this
                    password = data['password']
                    image1 = data['image1']
                    image2 = data['image2']
                    location = data['location']
                    phone = data['phone']
                    wallet_address = data['wallet_address']

                    dataDict = {
                        'id': str(id),
                        'name' : name,
                        'email': email,
                        'licenceNo': licence, 
                        'image1':image1,
                        'image2':image2,
                        'location' : location,
                        'phoneNo' : phone,
                        'wallet_address': data['wallet_address']
                    }
                    dataJson.append(dataDict)
                    log_backend("Login attempt by insurance email id "+email + 'successful!')
                else:
                    log_backend("Login attempt by insurance email id "+data['email'] + 'unsuccessful. Admin approval required!')
                    return jsonify({'verifiedUser': 0})
                
        elif stakeholder == 'hospital':
            print('stakeholder is hospital')
            for data in allData:
                if data['verifiedUser']:
                    id = data['_id']
                    name = data['name']
                    email = data['email']
                    licence = data['licenceNo']
                    # TODO: for nxt deadline remove this
                    password = data['password']
                    specialty = data['specialty']
                    image1 = data['image1']
                    image2 = data['image2']
                    location = data['location']
                    phone = data['phone']
                    wallet_address = data['wallet_address']

                    dataDict = {
                        'id': str(id),
                        'name' : name,
                        'email': email,
                        # TODO: some values do not have licence number saved
                        # 'licenceNo': licence, 
                        'image1':image1,
                        'image2':image2,
                        'specialty' : specialty,
                        'location' : location,
                        'phoneNo' : phone,
                        'wallet_address': data['wallet_address']
                    }
                    dataJson.append(dataDict)
                    log_backend("Login attempt by hospital email id "+email + 'successful!')
                else:
                    log_backend("Login attempt by hospital email id "+data['email'] + 'unsuccessful. Admin approval required!')
                    return jsonify({'verifiedUser': 0})
        
        elif stakeholder == 'patient':
            for data in allData:
                if data['verifiedUser']:
                    id = data['_id']
                    name = data['name']
                    DOB = data['DOB']
                    gender = data['gender']
                    email = data['email']
                    # TODO: for nxt deadline remove this
                    password = data['password']
                    phone = data['phone']
                    joiningDate = data['joiningDate']
                    pcpID = data['pcpID']
                    insuranceID = data['insuranceID']
                    wallet_address = data['wallet_address']

                    dataDict = {
                        'id': str(id),
                        'name' : name,
                        'DOB' : DOB,
                        'gender' : gender,
                        'email': email,
                        'phoneNo' : phone,
                        'joiningDate' :joiningDate,
                        'pcpID' :pcpID,
                        'insuranceID': insuranceID,
                        'wallet_address': data['wallet_address']
                        
                    }
                    dataJson.append(dataDict)
                    log_backend("Login attempt by patient email id "+email + 'successful!')
                else:
                    log_backend("Login attempt by patient email id "+data['email'] + 'unsuccessful. Admin approval required!')
                    return jsonify({'verifiedUser': 0})
        # adda
        elif stakeholder == 'files':
            for data in allData:
                id = data['_id']
                fetchedUploader = data['uploader']
                accessList = data['access']
                if not ((fetchedUploader == uploader) or (uploader in accessList)):
                    continue
                originalFileName = data['originalFileName']
                stakeholderForFile = data['stakeholder']

                dataDict = {
                    'id': str(id),
                    'uploader': fetchedUploader,
                    'access': accessList,
                    'originalFileName': originalFileName,
                    'stakeholder': stakeholderForFile,
                }
                dataJson.append(dataDict)
                log_backend("Request for all files of a user made")

        elif stakeholder == "verify":
            print(params)
            allData = db['files'].find(filter)
            # Should have sent uploader and originalFileName as well
            print("Daata is ",allData)
            for data in allData:
                print(data)
                id = data['_id']
                fetchedUploader = data['uploader']
                accessList = data['access']
                originalFileName = data['originalFileName']
                hashedFile = data['hashedFile']
                pathStored = data['pathStored']
                URL = data['URL']
       
                newHash = hash_file(pathStored)
                log_backend("Request for file verification made")
                print(newHash, "newHash")
                print(hashedFile, "oLDHash")
                if newHash == hashedFile:
                    log_backend( URL+ " Verified file!")
                    dataJson.append({"URL": URL, "verified":True})
                    break
                else:
                    log_backend(URL+" Unverified file!")
                    dataJson.append({"URL": '', "verified": False})
                    break
            return jsonify(dataJson)

        if stakeholder == "admin":
            print('admin All data', allData)
            for data in allData:
                id = data['_id']

                dataDict = {
                    'id': str(id),     
                    'verifiedUser': data['verifiedUser'],
                    'stakeholder': 'admin'               
                }
                dataJson.append(dataDict)
            return jsonify(dataJson)

        print('Attempted to login, sending response', dataJson)
        if stakeholder in ['doctor', 'hospital', 'insurance', 'patient', 'pharmacy']:
            if allData and dataJson:  # Generate JWT
                token = jwt.encode({
                    'user': params['email'],
                    'expiration': str(datetime.now() + timedelta(seconds=120))
                }, app.config['SECRET_KEY'])
                dataJson[0]['token'] = token.decode('utf-8')
                return jsonify(dataJson)
            else:
                log_backend("Login denied")
                return jsonify({'status': 'No matching user found. Unable to send valid response.'})
        return jsonify({'status': 'Verify called'})

        
    # DELETE a data
    if request.method == 'DELETE':
        db['users'].deleteMany({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        # params = json.loads(params)
        # del params["stakeholder"]
        print("put params is ", params)
        stakeholder = params['stakeHolder']
        allData = db[stakeholder].find()
        if(stakeholder == "patient"):
            if params['request'] == 'register':
                print('register patient received params', params)
                updatedData = {}
                updatedData['name'] = params['name']
                updatedData['phone'] = params['phoneNo']
                updatedData['email'] = params['email']
                updatedData['wallet_address'] = params['wallet_address']
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Patient data with email ' + params['email'] + ' has been updated!')
                return jsonify({'status': 'Patient data with email ' + params['email'] + ' has been updated!'})

            elif params['request'] == 'update':
                name = params['name']
                email = params['email']
                DOB = params['DOB'].replace("-", "/")
                phone = params['phone']
                currentPassword = params['currentPassword']
                newPassword = params['newPassword']
                newPasswordRepeat = params['newPasswordRepeat']
                updatedData = {}
                if name:
                    updatedData['name'] = name
                if phone:
                    updatedData['phone'] = phone
                if DOB:
                    updatedData['DOB'] = DOB
                if currentPassword:
                    # Check if current password matches the one in the database first. 
                    if newPassword and newPasswordRepeat:
                        if newPassword == newPasswordRepeat:
                            updatedData['password'] = hashlib.sha256(newPassword.encode()).hexdigest()  # Later, add salt as well
                        else:
                            log_backend("A request for update was made but password did not match")
                            return jsonify({'error': 101, 'status': 'Couldn\'t update profile. Passwords don\'t match!'})
                if email:
                    print('updatedData', updatedData)
                    db[stakeholder].update_one(
                        {'email': email},  # retrieving the user using email ID
                        {
                            "$set": updatedData
                        }
                    )
                    print('\n # Update successful # \n')
                    log_backend("Pateint with email ID "+email + " was updated")
                    return jsonify({'status': 'Patient data with email ' + email + ' has been updated!'})
                else:
                    print('\n # Invalid user $ \n')
                    # Return some error JSON

        elif stakeholder == "doctor":
            if params['request'] == 'register':
                print('register doctor received params', params)
                updatedData = {}
                updatedData['name'] = params['name']
                updatedData['phone'] = params['phoneNo']
                updatedData['email'] = params['email']
                updatedData['licenceNo'] = params['licenceNo']
                updatedData['wallet_address'] = params['wallet_address']
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend( 'Doctor data with email ' + params['email'] + ' has been updated!')
                return jsonify({'status': 'Doctor data with email ' + params['email'] + ' has been updated!'})
            
            elif params['request'] == 'update':
                name = params['name']
                email = params['email']
                DOB = params['DOB'].replace("-", "/")
                phone = params['phone']
                specialty = params['specialty']
                licenceNo = params['licenceNo']
                fee = params['fee']
                location = params['location']
                currentPassword = params['currentPassword']
                newPassword = params['newPassword']
                newPasswordRepeat = params['newPasswordRepeat']
                updatedData = {}
                if name:
                    updatedData['name'] = name
                if phone:
                    updatedData['phone'] = phone
                if DOB:
                    updatedData['DOB'] = DOB
                if specialty:
                    updatedData['specialty'] = specialty
                if licenceNo:
                    updatedData['licenceNo'] = licenceNo
                if fee:
                    updatedData['consultationFee'] = fee
                if location:
                    updatedData['location'] = location
                if currentPassword:
                    # Check if current password matches the one in the database first. 
                    if newPassword and newPasswordRepeat:
                        if newPassword == newPasswordRepeat:
                            updatedData['password'] = hashlib.sha256(newPassword.encode()).hexdigest()  # Later, add salt as well
                        else:
                            log_backend("Did not update as password incorrect")
                            return jsonify({'error': 101, 'status': 'Couldn\'t update profile. Passwords don\'t match!'})
                if email:
                    print('updatedData', updatedData)
                    db[stakeholder].update_one(
                        {'email': email},  # retrieving the user using email ID
                        {
                            "$set": updatedData
                        }
                    )
                    print('\n # Update successful # \n')
                    
                    return jsonify({'status': 'Doctor data with email ' + email + ' has been updated!'})
            else:
                print('\n # Invalid user $ \n')
                # Return some error JSON

        elif stakeholder == "hospital":
            if params['request'] == 'register':
                print('register hospital received params', params)
                updatedData = {}
                updatedData['name'] = params['name']
                updatedData['phone'] = params['phoneNo']
                updatedData['email'] = params['email']
                updatedData['licenceNo'] = params['licenceNo']
                updatedData['wallet_address'] = params['wallet_address']
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Hospital data with email ' + params['email'] + ' has been updated!')
                return jsonify({'status': 'Hospital data with email ' + params['email'] + ' has been updated!'})

            elif params['request'] == 'update':
                name = params['name']
                email = params['email']
                DOB = params['DOB'].replace("-", "/")
                phone = params['phone']
                specialty = params['specialty']
                licenceNo = params['licenceNo']
                fee = params['fee']
                location = params['location']
                currentPassword = params['currentPassword']
                newPassword = params['newPassword']
                newPasswordRepeat = params['newPasswordRepeat']
                updatedData = {}
                if name:
                    updatedData['name'] = name
                if phone:
                    updatedData['phone'] = phone
                if DOB:
                    updatedData['DOB'] = DOB
                if specialty:
                    updatedData['specialty'] = specialty
                if licenceNo:
                    updatedData['licenceNo'] = licenceNo
                if fee:
                    updatedData['consultationFee'] = fee
                if location:
                    updatedData['location'] = location
                if currentPassword:
                    # Check if current password matches the one in the database first. 
                    if newPassword and newPasswordRepeat:
                        if newPassword == newPasswordRepeat:
                            updatedData['password'] = hashlib.sha256(newPassword.encode()).hexdigest()  # Later, add salt as well
                        else:
                            log_backend('Couldn\'t update profile. Passwords don\'t match!')
                            return jsonify({'error': 101, 'status': 'Couldn\'t update profile. Passwords don\'t match!'})
                if email:
                    print('updatedData', updatedData)
                    db[stakeholder].update_one(
                        {'email': email},  # retrieving the user using email ID
                        {
                            "$set": updatedData
                        }
                    )
                    print('\n # Update successful # \n')
                    log_backend('Hospital data with email ' + email + ' has been updated!')
                    return jsonify({'status': 'Hospital data with email ' + email + ' has been updated!'})
            else:
                print('\n # Invalid user $ \n')
                # Return some error JSON
        
        elif stakeholder == "insurance":
            if params['request'] == 'register':
                print('register insurance received params', params)
                updatedData = {}
                updatedData['name'] = params['name']
                updatedData['phone'] = params['phoneNo']
                updatedData['email'] = params['email']
                updatedData['licenceNo'] = params['licenceNo']

                updatedData['wallet_address'] = params['wallet_address']
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Insurance data with email ' + params['email'] + ' has been updated!')
                return jsonify({'status': 'Insurance data with email ' + params['email'] + ' has been updated!'})

            elif params['request'] == 'update':
                name = params['name']
                email = params['email']
                DOB = params['DOB'].replace("-", "/")
                phone = params['phone']
                specialty = params['specialty']
                licenceNo = params['licenceNo']
                fee = params['fee']
                location = params['location']
                currentPassword = params['currentPassword']
                newPassword = params['newPassword']
                newPasswordRepeat = params['newPasswordRepeat']
                updatedData = {}
                if name:
                    updatedData['name'] = name
                if phone:
                    updatedData['phone'] = phone
                if DOB:
                    updatedData['DOB'] = DOB
                if specialty:
                    updatedData['specialty'] = specialty
                if licenceNo:
                    updatedData['licenceNo'] = licenceNo
                if fee:
                    updatedData['consultationFee'] = fee
                if location:
                    updatedData['location'] = location
                if currentPassword:
                    # Check if current password matches the one in the database first. 
                    if newPassword and newPasswordRepeat:
                        if newPassword == newPasswordRepeat:
                            updatedData['password'] = hashlib.sha256(newPassword.encode()).hexdigest()  # Later, add salt as well
                        else:
                            return jsonify({'error': 101, 'status': 'Couldn\'t update profile. Passwords don\'t match!'})
                if email:
                    print('updatedData', updatedData)
                    db[stakeholder].update_one(
                        {'email': email},  # retrieving the user using email ID
                        {
                            "$set": updatedData
                        }
                    )
                    print('\n # Update successful # \n')
                    log_backend('Insurance data with email ' + email + ' has been updated!')
                    return jsonify({'status': 'Insurance data with email ' + email + ' has been updated!'})
                else:
                    print('\n # Invalid user $ \n')
                    # Return some error JSON
        
        elif stakeholder == "pharmacy":
            if params['request'] == 'register':
                print('register pharmacy received params', params)
                updatedData = {}
                updatedData['name'] = params['name']
                updatedData['phone'] = params['phoneNo']
                updatedData['email'] = params['email']
                updatedData['licenceNo'] = params['licenceNo']
                updatedData['wallet_address'] = params['wallet_address']
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('pharmacy data with email ' + params['email'] + ' has been updated!')
                return jsonify({'status': 'pharmacy data with email ' + params['email'] + ' has been updated!'})

            elif params['request'] == 'update':
                name = params['name']
                email = params['email']
                DOB = params['DOB'].replace("-", "/")
                phone = params['phone']
                specialty = params['specialty']
                licenceNo = params['licenceNo']
                fee = params['fee']
                location = params['location']
                currentPassword = params['currentPassword']
                newPassword = params['newPassword']
                newPasswordRepeat = params['newPasswordRepeat']
                updatedData = {}
                if name:
                    updatedData['name'] = name
                if phone:
                    updatedData['phone'] = phone
                if DOB:
                    updatedData['DOB'] = DOB
                if specialty:
                    updatedData['specialty'] = specialty
                if licenceNo:
                    updatedData['licenceNo'] = licenceNo
                if fee:
                    updatedData['consultationFee'] = fee
                if location:
                    updatedData['location'] = location
                if currentPassword:
                    # Check if current password matches the one in the database first. 
                    if newPassword and newPasswordRepeat:
                        if newPassword == newPasswordRepeat:
                            updatedData['password'] = hashlib.sha256(newPassword.encode()).hexdigest()  # Later, add salt as well
                        else:
                            return jsonify({'error': 101, 'status': 'Couldn\'t update profile. Passwords don\'t match!'})
                if email:
                    print('updatedData', updatedData)
                    db[stakeholder].update_one(
                        {'email': email},  # retrieving the user using email ID
                        {
                            "$set": updatedData
                        }
                    )
                    print('\n # Update successful # \n')
                    return jsonify({'status': 'Pharmacy data with email ' + email + ' has been updated!'})
                else:
                    print('\n # Invalid user $ \n')
                    return jsonify({'status': 'Error: Invalid user!'})
        else:
            log_backend("Invalid user tried to update")
            print("Not a valid user!")

@app.route('/api/v1/users/verifyUserFile', methods=['POST'])
def verifyUserFile():  # Function for Naman to add blockchain file verification 
    pass

@app.route('/api/v1/users/approveUser', methods=['POST'])
def approveUser():  # Approve the user and give approval accordingly (change the boolean value)
    if request.method == 'POST':
        print(request)
        params = request.json
        print("put params is ", params)
        stakeholder = params['stakeholder']
        verifiedFile = params['verifiedFile']
        if(stakeholder == "patient"):
            if verifiedFile:
                print('register patient received params', params)
                updatedData = {}
                updatedData['verifiedUser'] = 1
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Patient with email ' + params['email'] + ' has been approved!')
                return jsonify({'status': 'Patient with email ' + params['email'] + ' has been approved!'})
            else:
                log_backend('Couldn\'t approve patient with email ' + params['email'] + '. Couldn\'t verify !')
                return jsonify({'status': 'Couldn\'t approve patient with email ' + params['email'] + '. Couldn\'t verify !'})
 

        elif stakeholder == "doctor":
            if verifiedFile:
                print('register doctor received params', params)
                updatedData = {}
                updatedData['verifiedUser'] = 1
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Doctor with email ' + params['email'] + ' has been approved!')
                return jsonify({'status': 'Doctor with email ' + params['email'] + ' has been approved!'})
            else:
                log_backend('Couldn\'t approve doctor with email ' + params['email'] + '. Couldn\'t verify document!')
                return jsonify({'status': 'Couldn\'t approve doctor with email ' + params['email'] + '. Couldn\'t verify document!'})

        elif stakeholder == "hospital":
            if verifiedFile:
                print('register hospital received params', params)
                updatedData = {}
                updatedData['verifiedUser'] = 1
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Hospital with email ' + params['email'] + ' has been approved!')
                return jsonify({'status': 'Hospital with email ' + params['email'] + ' has been approved!'})
            else:
                log_backend('Couldn\'t approve hospital with email ' + params['email'] + '. Couldn\'t verify document!')
                return jsonify({'status': 'Couldn\'t approve hospital with email ' + params['email'] + '. Couldn\'t verify document!'})
        
        elif stakeholder == "insurance":
            if verifiedFile:
                print('register insurance received params', params)
                updatedData = {}
                updatedData['verifiedUser'] = 1
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Insurance with email ' + params['email'] + ' has been approved!')
                return jsonify({'status': 'Insurance with email ' + params['email'] + ' has been approved!'})
            else:
                log_backend('Couldn\'t approve insurance firm with email ' + params['email'] + '. Couldn\'t verify document!')
                return jsonify({'status': 'Couldn\'t approve insurance firm with email ' + params['email'] + '. Couldn\'t verify document!'})
        
        elif stakeholder == "pharmacy":
            if verifiedFile:
                print('register pharmacy received params', params)
                updatedData = {}
                updatedData['verifiedUser'] = 1
                print('adding to DB', updatedData)

                db[stakeholder].update_one(
                    {
                        'email': params['email']  # retrieving the user using email ID
                    },  
                    {
                        "$set": updatedData
                    }
                )
                log_backend('Pharmacy with email ' + params['email'] + ' has been approved!')
                return jsonify({'status': 'Pharmacy with email ' + params['email'] + ' has been approved!'})
            else:
                log_backend('Couldn\'t approve Pharmacy with email ' + params['email'] + '. Couldn\'t verify document!')
                return jsonify({'status': 'Couldn\'t approve Pharmacy with email ' + params['email'] + '. Couldn\'t verify document!'})
        else:
            log_backend('Bad user data recieved')
            return jsonify({'status': 'Invalid user!'})
    else:
        log_backend('Bad request recieved')
        return jsonify({'status': 'Invalid request!'})
            

@app.route('/api/v1/users/denyUser', methods=['POST'])
def denyUser():  # deny the user from access (delete from the database)
    print("Deny User RECEIVED")
    if request.method == 'POST':
        print("POST request")
        params = request.json
        print("put params is ", params)
        db[params['stakeholder']].delete_one({'email': params['email']})
        log_backend('Denied user with email ' + params['email'])
        return jsonify({'status': 'Denied user with email ' + params['email']})
    else:
        log_backend('Couldn\'t deny user with email ' + params['email'] + '. Couldn\'t verify document!')
        return jsonify({'status': 'Couldn\'t deny user with email ' + params['email'] + '. Couldn\'t verify document!'})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<stakeholder>/<name>')
def download_file(stakeholder, name):
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER+"/"+stakeholder+'/'
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/uploadFile', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print("reached this route")
        print(request.files)
        file = request.files['image']
        print(file)
        print(request.form)
        stakeHolder = request.form['stakeholder']
        fileType = request.form['type']
        print("VENS8")
        print("Stakeholder is", stakeHolder)
        uploader = request.form['uploader']
        access = request.form['access'].split(',')
        print("Uploader is", uploader)
        print("access is", access, type(access))
        pathToFolder = UPLOAD_FOLDER+'/'+stakeHolder+'/'
        app.config['UPLOAD_FOLDER'] = pathToFolder
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("File name is ", filename)
            fileExtension = filename.split('.')[1]
            hashedFileName = hashlib.sha256(filename.encode()).hexdigest()
            print("HashedFileName", hashedFileName)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], hashedFileName+"."+fileExtension))
            message = hash_file(pathToFolder+"/"+hashedFileName+"."+fileExtension)
            folder = pathToFolder+"/"+hashedFileName+"."+fileExtension
            print("Path to folder is", folder)
            print("Hash of the file is", message)
            hashedURL = "https://192.168.2.251:5000/uploads/"+stakeHolder+"/"+hashedFileName+'.'+fileExtension
            print("URL to access file", hashedURL )


            db["files"].insert_one({
                    "originalFileName": filename,
                    "hashedFileName":hashedFileName,
                    "hashedFile" : message,
                    "URL":hashedURL,
                    "pathStored":folder,
                    "access": access,
                    "uploader":uploader,
                    "stakeholder":stakeHolder,
                    "type":fileType,
                })
            log_backend("File "+filename+" has been added to the backend db")
            return {"hash":message}
    log_backend("File could not be uploaded")
    return {"hash":"error"}

app.add_url_rule(
    "/uploads/<stakeholder>/<name>", endpoint="download_file", build_only=True
)

@app.route('/api/v1/unverifiedUsers', methods=['GET'])
def unverifiedUsers():
    # GET all data from database
    if request.method == 'GET':
        log_backend("Admin requested for all unverified users")
        doctor = db["doctor"].find()
        hospital = db["hospital"].find()
        insurance = db["insurance"].find()
        patient = db["patient"].find()
        pharmacy = db["pharmacy"].find()
        files = db["files"].find()
        print('files', files)
        allData = []
        filesData = []
        for data in files:
            print('file stakeholder',data['stakeholder'])
            if data['type'] == 'poi':
                dataDict = {
                    'file_id': str(data['_id']),
                    'originalFileName': data['originalFileName'],
                    'hashedFileName': data['hashedFileName'],
                    'hashedFile': data['hashedFile'],
                    'URL': data['URL'],
                    'uploader': data['uploader'],
                    'stakeholder': data['stakeholder'],
                    'type': data['type']
                }
                print('filesData', filesData)
                filesData.append(dataDict)

        # Get doctor data
        doctorData = []
        for data in doctor:
            if 'verifiedUser' in data.keys():
                if not data['verifiedUser']:
                    id = data['_id']
                    name = data['name']
                    email = data['email']
                    wallet_address = data['wallet_address']
                    dataDict = {
                        'id': str(id),
                        'name': name,
                        'email': email,
                        'wallet_address': wallet_address,
                        'stakeholder': 'doctor'
                    }
                    for fil in filesData:
                        if fil['uploader'] == data['email'] and fil['stakeholder'] == "doctor":
                            z = {**dataDict, **fil}
                            dataDict = z
                    print('doctor merged data', dataDict)
                    doctorData.append(dataDict)
        # print(doctorData)
        allData.append(doctorData)

        hospitalData = []
        for data in hospital:
            if not data['verifiedUser']:
                id = data['_id']
                name = data['name']
                licenceNo = data['licenceNo']
                email = data['email']
                dataDict = {
                    'id': str(id),
                    'email': email,
                    'licenceNo': licenceNo,
                    'wallet_address': data['wallet_address'],
                    'stakeholder': 'hospital'

                }
                for fil in filesData:
                    if fil['uploader'] == data['email'] and fil['stakeholder'] == "hospital":
                        z = {**dataDict, **fil}
                        dataDict = z
                # print('doctor merged data', dataDict)
                hospitalData.append(dataDict)
        # print(hospitalData)
        allData.append(hospitalData)

        insuranceData = []
        for data in insurance:
            if not data['verifiedUser']:
                id = data['_id']
                name = data['name']
                licenceNo = data['licenceNo']
                email = data['email']
                dataDict = {
                    'id': str(id),
                    'email': email,
                    'licenceNo': licenceNo,
                    'wallet_address': data['wallet_address'],
                    'stakeholder': 'insurance'

                }
                for fil in filesData:
                    if fil['uploader'] == data['email'] and fil['stakeholder'] == "insurance":
                        z = {**dataDict, **fil}
                        dataDict = z
                # print('insurance merged data', dataDict)
                insuranceData.append(dataDict)
        # print(insuranceData)
        allData.append(insuranceData)


        patientData = []
        for data in patient:
            if not data['verifiedUser']:
                id = data['_id']
                name = data['name']
                email = data['email']
                dataDict = {
                    'id': str(id),
                    'email': email,
                    'wallet_address': data['wallet_address'],
                    'stakeholder': 'patient'

                }
                for fil in filesData:
                    if fil['uploader'] == data['email'] and fil['stakeholder'] == "patient":
                        z = {**dataDict, **fil}
                        dataDict = z
                # print('patient merged data', dataDict)
                patientData.append(dataDict)
        # print(patientData)
        allData.append(patientData)

        pharmacyData = []
        for data in pharmacy:
            if not data['verifiedUser']:
                id = data['_id']
                name = data['name']
                licenceNo = data['licenceNo']
                email = data['email']
                dataDict = {
                    'id': str(id),
                    'email': email,
                    'licenceNo': licenceNo,
                    'wallet_address': data['wallet_address'],
                    'stakeholder': 'pharmacy'

                }
                for fil in filesData:
                    if fil['uploader'] == data['email'] and fil['stakeholder'] == "pharmacy":
                        z = {**dataDict, **fil}
                        dataDict = z
                # print('pharmacy merged data', dataDict)
                pharmacyData.append(dataDict)
        # print(pharmacyData)
        allData.append(pharmacyData)
        print('all data json', allData)
        return jsonify(allData)


@app.route('/api/v1/verifiedUsers', methods=['GET'])
def verifiedUsers():
    # GET all data from database
    
    if request.method == 'GET':
        log_backend("Admin requested list of all verified users")
        doctor = db["doctor"].find()
        hospital = db["hospital"].find()
        insurance = db["insurance"].find()
        patient = db["patient"].find()
        pharmacy = db["pharmacy"].find()
        files = db["files"].find()
        print('files', files)
        allData = []
        filesData = []
        for data in files:
            print('file stakeholder',data['stakeholder'])
            if data['type'] == 'poi':
                dataDict = {
                    'file_id': str(data['_id']),
                    'originalFileName': data['originalFileName'],
                    'hashedFileName': data['hashedFileName'],
                    'hashedFile': data['hashedFile'],
                    'URL': data['URL'],
                    'uploader': data['uploader'],
                    'stakeholder': data['stakeholder'],
                    'type': data['type']
                }
                print('filesData', filesData)
                filesData.append(dataDict)

        # Get doctor data
        doctorData = []
        for data in doctor:
            if 'verifiedUser' in data.keys():
                if data['verifiedUser']:
                    id = data['_id']
                    name = data['name']
                    email = data['email']
                    wallet_address = data['wallet_address']
                    dataDict = {
                        'id': str(id),
                        'name': name,
                        'email': email,
                        'wallet_address': data['wallet_address']
                    }
                    for fil in filesData:
                        if fil['uploader'] == data['email'] and fil['stakeholder'] == "doctor":
                            z = {**dataDict, **fil}
                            dataDict = z
                    print('doctor merged data', dataDict)
                    doctorData.append(dataDict)
        # print(doctorData)
        allData.append(doctorData)

        hospitalData = []
        for data in hospital:
            if data['verifiedUser']:
                id = data['_id']
                name = data['name']
                licenceNo = data['licenceNo']
                email = data['email']
                dataDict = {
                    'id': str(id),
                    'email': email,
                    'licenceNo': licenceNo,
                    'wallet_address': data['wallet_address']
                }
                for fil in filesData:
                    if fil['uploader'] == data['email'] and fil['stakeholder'] == "hospital":
                        z = {**dataDict, **fil}
                        dataDict = z
                # print('doctor merged data', dataDict)
                hospitalData.append(dataDict)
        # print(hospitalData)
        allData.append(hospitalData)

        insuranceData = []
        for data in insurance:
            if data['verifiedUser']:
                id = data['_id']
                name = data['name']
                licenceNo = data['licenceNo']
                email = data['email']
                dataDict = {
                    'id': str(id),
                    'email': email,
                    'licenceNo': licenceNo,
                    'wallet_address': data['wallet_address']
                }
                for fil in filesData:
                    if fil['uploader'] == data['email'] and fil['stakeholder'] == "insurance":
                        z = {**dataDict, **fil}
                        dataDict = z
                # print('insurance merged data', dataDict)
                insuranceData.append(dataDict)
        # print(insuranceData)
        allData.append(insuranceData)


        patientData = []
        for data in patient:
            if data['verifiedUser']:
                id = data['_id']
                name = data['name']
                email = data['email']
                dataDict = {
                    'id': str(id),
                    'email': email,
                    'licenceNo': licenceNo,
                    'wallet_address': data['wallet_address']
                }
                for fil in filesData:
                    if fil['uploader'] == data['email'] and fil['stakeholder'] == "patient":
                        z = {**dataDict, **fil}
                        dataDict = z
                # print('patient merged data', dataDict)
                patientData.append(dataDict)
        # print(patientData)
        allData.append(patientData)

        pharmacyData = []
        for data in pharmacy:
            if data['verifiedUser']:
                id = data['_id']
                name = data['name']
                licenceNo = data['licenceNo']
                email = data['email']
                dataDict = {
                    'id': str(id),
                    'email': email,
                    'licenceNo': licenceNo,
                    'wallet_address': data['wallet_address']
                }
                for fil in filesData:
                    if fil['uploader'] == data['email'] and fil['stakeholder'] == "pharmacy":
                        z = {**dataDict, **fil}
                        dataDict = z
                # print('pharmacy merged data', dataDict)
                pharmacyData.append(dataDict)
        # print(pharmacyData)
        allData.append(pharmacyData)
        print('all data json', allData)
        return jsonify(allData)




# allowed = ['192.168.2.251']  # nginx

# @app.before_request
# def limit_remote_addr():
#     if request.remote_addr not in allowed:
#         abort(404) 
    

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print("Error occured:", e)
        log_backend(f"Error: {e}")
        app.sendErrorMessage(e)