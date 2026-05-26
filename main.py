# main.py
import os
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from flask_mail import Mail, Message
from camera import VideoCamera
from camera2 import VideoCamera2
from flask import send_file
import datetime
import cv2
import math
import numpy as np
import pandas as pd
import shutil
import datetime
import hashlib
from random import randint
import time
import PIL.Image
from PIL import Image
import piexif
import imagehash
import geocoder
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

import mysql.connector
from werkzeug.utils import secure_filename
from shapely.geometry import Point, Polygon
from tensorflow.keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="phc_doctor"

)
app = Flask(__name__)
app.secret_key = 'abcdef'

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#######
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="phc_doctor",
        autocommit=True
    )
    return conn

@app.route('/')
def index():
    
    
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ph_admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            # Redirect to home page
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/login_doc', methods=['GET', 'POST'])
def login_doc():
    msg=""
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']

        lat=request.form['lat']
        lon=request.form['lon']
        lat1=lat.split(".")
        lon1=lon.split(".")

        lt1=lat1[1]
        lo1=lon1[1]

        lt2=lt1[0:6]
        lo2=lo1[0:6]

        lt3=lat1[0]+"."+lt2
        lo3=lon1[0]+"."+lo2
        loc=lt3+","+lo3
        ff=open("static/gps_loc.txt","w")
        ff.write(loc)
        ff.close()
            
        
        mycursor.execute('SELECT * FROM ph_doctor WHERE uname = %s AND pass = %s', (uname, pwd))
        account = mycursor.fetchone()
        if account:
            session['username'] = uname
            fn=uname+"_cr.txt"
            fn2=uname+"_tm.txt"
            fn3=uname+"_doc.txt"
            fn4=uname+"_fence.txt"

            
            phc_id=account[10]
            stime=str(account[11])+":"+str(account[13])
            etime=str(account[12])+":"+str(account[14])
            ftime=stime+","+etime
            #
            mobile1=""
            email1=""
            mobile2=""
            email2=""
            email3=""
            mycursor.execute("SELECT * FROM ph_ddhs order by id")
            of1 = mycursor.fetchall()
            for of11 in of1:
                email1=of11[3]
                mobile1=str(of11[2])

            mycursor.execute("SELECT * FROM ph_hmo order by id")
            of2 = mycursor.fetchall()
            for of21 in of2:
                email2=of21[3]
                mobile2=str(of21[2])

            mycursor.execute("SELECT * FROM ph_admin")
            of3 = mycursor.fetchall()
            for of31 in of3:
                email3=of31[2]


            doc=account[1]+"|"+account[7]+"|"+mobile1+"|"+email1+"|"+mobile2+"|"+email2+"|"+email3+"|"+phc_id
        
            #GPS 
            mycursor.execute("SELECT * FROM ph_hospital where phc_id=%s",(phc_id,))
            d4 = mycursor.fetchone()
            g1=d4[5]
            g2=g1.split('new google.maps.LatLng(')
            g21=''.join(g2)
            g22=g21.split('), ')
            print(g22)
            glen=len(g22)
            coors=[]
            i=1
            dt=""
            for g3 in g22:
                cr=[]
                if i<glen:
                    g31=g3.split(",")
                    print(g31)
                    clat=g31[0]
                    clon=g31[1]
                    dt+=clat+","+clon+"|"
                    g32=float(g31[0])
                    g33=float(g31[1])
                    cr.append(g32)
                    cr.append(g33)
                    coors.append(cr)
                i+=1


            
            
            ff=open("static/check/"+fn,"w")
            ff.write(dt)
            ff.close()

            ff=open("static/check/"+fn2,"w")
            ff.write(ftime)
            ff.close()

            ff=open("static/check/"+fn3,"w")
            ff.write(doc)
            ff.close()

            path="static/check/"+fn4
            if not os.path.exists(path):
                with open(path, "w") as ff:
                    ff.write("")

            fn5 = uname + "_dt.txt"

            path = "static/check/" + fn5

            # Create file if not exists
            if not os.path.exists(path):
                with open(path, "w") as ff:
                    ff.write("")
            ##
                
            return redirect(url_for('doc_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_doc.html',msg=msg)

@app.route('/login_ddhs', methods=['GET', 'POST'])
def login_ddhs():
    msg=""
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM ph_ddhs WHERE uname = %s AND pass = %s", (uname, pwd))
        account = cursor.fetchone()
        if account:
            
            
            session['username'] = uname
            # Redirect to home page
            return redirect(url_for('ddhs_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_ddhs.html',msg=msg)

@app.route('/login_hmo', methods=['GET', 'POST'])
def login_hmo():
    msg=""
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM ph_hmo WHERE uname = %s AND pass = %s", (uname, pwd))
        account = cursor.fetchone()
        if account:
            
            
            session['username'] = uname
            # Redirect to home page
            return redirect(url_for('hmo_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_hmo.html',msg=msg)

def pad_left(s, length):
    return s.zfill(length)

@app.route('/admin',methods=['POST','GET'])
def admin():
    msg=""
    mess=""
    email=""
    pid=""
    act=request.args.get("act")
    data=[]
    st=""
    mycursor = mydb.cursor()

    if request.method=='POST':
        name=request.form['name']        
        
        area=request.form['area']
        district=request.form['district']
       
        
            
        #mycursor.execute("SELECT count(*) FROM ph_hospital where name=%s",(name,))
        #cnt = mycursor.fetchone()[0]
        #if cnt==0:
            
        mycursor.execute("SELECT max(id)+1 FROM ph_hospital")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        pid=str(pid)

        input_str = str(maxid)
        padded_str = pad_left(input_str, 3)
        phc_id="P"+padded_str

        det="new google.maps.LatLng(10.920405,78.625245), new google.maps.LatLng(10.885006,78.650308), new google.maps.LatLng(10.883658,78.602586), new google.maps.LatLng(10.920405,78.625245), "
        sql = "INSERT INTO ph_hospital(id,name,area,district,phc_id,detail) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (maxid,name,area,district,phc_id,det)
        mycursor.execute(sql, val)
        mydb.commit()
       
        msg="success"
        #else:
        #    msg="fail"


    mycursor.execute("SELECT * FROM ph_hospital order by id desc")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ph_hospital where id=%s",(did,))
        mydb.commit()
        msg="ok"
        return redirect(url_for('admin'))
        
    return render_template('web/admin.html',msg=msg,act=act,data=data,pid=pid)

@app.route('/add_geo',methods=['POST','GET'])
def add_geo():
    msg=""
    act=request.args.get("act")
    pid=request.args.get("pid")
    
    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM ph_hospital where id=%s',(pid,))
    view=mycursor.fetchone()
    
    if request.method=='POST':
        detail=request.form['detail']
        location=request.form['location']

        mycursor.execute("update ph_hospital set area=%s,detail=%s where id=%s",(location,detail,pid))
        mydb.commit()
       
        msg="ok"

    
    
    return render_template('web/add_geo.html',msg=msg,pid=pid,view=view)

@app.route('/map1', methods=['GET', 'POST'])
def map1():
    msg=""
    pid=request.args.get("pid")
    
    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM ph_hospital where id=%s',(pid,))
    view=mycursor.fetchone()
    
    if request.method=='POST':
        detail=request.form['detail']
        location=request.form['location']

        mycursor.execute("update ph_hospital set area=%s,detail=%s where id=%s",(location,detail,pid))
        mydb.commit()
       
        msg="ok"

    
    
    return render_template('web/map1.html',msg=msg,pid=pid,view=view)



@app.route('/add_doctor',methods=['POST','GET'])
def add_doctor():
    msg=""
    mess=""
    email=""
    vid=""
    act=request.args.get("act")
    data=[]
    st=""
    mycursor = mydb.cursor()

    mycursor.execute("SELECT max(id)+1 FROM ph_doctor")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1

    docid="D"+str(maxid)        
    mycursor.execute("SELECT * FROM ph_hospital")
    phos = mycursor.fetchall()
            
    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']  
        mobile=request.form['mobile']
        email=request.form['email']
        district=request.form['district']
        specialized=request.form['specialized']  
        uname=request.form['uname']
        pass1=request.form['pass']
        phc_id=request.form['phc_id']
        stime=request.form['stime']                          
        etime=request.form['etime']
        smin=request.form['smin']
        emin=request.form['emin']

        mycursor.execute("SELECT count(*) FROM ph_doctor where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            

            sql = "INSERT INTO ph_doctor(id,name,gender,mobile,email,district,specialized,uname,pass,phc_id,stime,etime,smin,emin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,gender,mobile,email,district,specialized,uname,pass1,phc_id,stime,etime,smin,emin)
            mycursor.execute(sql, val)
            mydb.commit()
            vid=str(maxid)
            mess="Dear "+name+", Username: "+uname+", Password: "+pass1
            msg="success"
        else:
            msg="fail"


    mycursor.execute("SELECT * FROM ph_doctor order by id desc")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ph_doctor where id=%s",(did,))
        mydb.commit()
        msg="ok"
        return redirect(url_for('add_doctor'))
        
    return render_template('web/add_doctor.html',msg=msg,act=act,data=data,phos=phos,docid=docid,vid=vid)

@app.route('/edit_doctor',methods=['POST','GET'])
def edit_doctor():
    msg=""
    mess=""
    email=""
    vid=""
    act=request.args.get("act")
    rid=request.args.get("rid")
    data=[]
    st=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_doctor where id=%s",(rid,))
    data = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM ph_hospital")
    phos = mycursor.fetchall()
            
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        district=request.form['district']
        specialized=request.form['specialized']  
        stime=request.form['stime']
        etime=request.form['etime']
        smin=request.form['smin']
        emin=request.form['emin']
        phc_id=request.form['phc_id']

      
        mycursor.execute("update ph_doctor set name=%s,mobile=%s,email=%s,district=%s,specialized=%s,phc_id=%s,stime=%s,etime=%s,smin=%s,emin=%s where id=%s",(name,mobile,email,district,specialized,phc_id,stime,etime,smin,emin,rid))
        mydb.commit()
        
        return redirect(url_for('add_doctor'))
       
    return render_template('web/edit_doctor.html',msg=msg,act=act,data=data,phos=phos)


@app.route('/add_ddhs',methods=['POST','GET'])
def add_ddhs():
    msg=""
    mess=""
    email=""
    act=request.args.get("act")
    data=[]
    st=""
    mycursor = mydb.cursor()

    mycursor.execute("SELECT max(id)+1 FROM ph_ddhs")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1

    dhid="DH"+str(maxid)
        
    if request.method=='POST':
        name=request.form['name']        
        mobile=request.form['mobile']
        email=request.form['email']
        district=request.form['district']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute("SELECT count(*) FROM ph_ddhs where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            

            sql = "INSERT INTO ph_ddhs(id,name,mobile,email,district,uname,pass) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,mobile,email,district,uname,pass1)
            mycursor.execute(sql, val)
            mydb.commit()
            mess="Dear "+name+", Username: "+uname+", Password: "+pass1
            msg="success"
        else:
            msg="fail"


    mycursor.execute("SELECT * FROM ph_ddhs order by id desc")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ph_ddhs where id=%s",(did,))
        mydb.commit()
        msg="ok"
        return redirect(url_for('add_ddhs'))
        
    return render_template('web/add_ddhs.html',msg=msg,act=act,data=data,st=st,email=email,mess=mess,dhid=dhid)

@app.route('/add_hmo',methods=['POST','GET'])
def add_hmo():
    msg=""
    mess=""
    email=""
    act=request.args.get("act")
    data=[]
    st=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM ph_hmo")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1

    hmid="HM"+str(maxid)
                

    if request.method=='POST':
        name=request.form['name']        
        mobile=request.form['mobile']
        email=request.form['email']
        district=request.form['district']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute("SELECT count(*) FROM ph_hmo where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            

            sql = "INSERT INTO ph_hmo(id,name,mobile,email,district,uname,pass) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,mobile,email,district,uname,pass1)
            mycursor.execute(sql, val)
            mydb.commit()
            mess="Dear "+name+", Username: "+uname+", Password: "+pass1
            msg="success"
        else:
            msg="fail"


    mycursor.execute("SELECT * FROM ph_hmo order by id desc")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ph_hmo where id=%s",(did,))
        mydb.commit()
        msg="ok"
        return redirect(url_for('add_hmo'))
        
    return render_template('web/add_hmo.html',msg=msg,act=act,data=data,st=st,email=email,mess=mess,hmid=hmid)







def getImagesAndLabels(path):

    
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids


@app.route('/add_photo',methods=['POST','GET'])
def add_photo():
    vid = request.args.get('vid')
    ff1=open("photo.txt","w")
    ff1.write("2")
    ff1.close()

    #ff2=open("mask.txt","w")
    #ff2.write("face")
    #ff2.close()
    act = request.args.get('act')

    cursor = mydb.cursor()
    
    cursor.execute("SELECT * FROM ph_doctor where id=%s",(vid,))
    value = cursor.fetchone()
    name=value[1]
    
    ff=open("user.txt","w")
    ff.write(name)
    ff.close()

    ff=open("user1.txt","w")
    ff.write(vid)
    ff.close()
    

    
    
    if request.method=='POST':
        vid=request.form['vid']
        fimg="v"+vid+".jpg"
        

        cursor.execute('delete from ph_face WHERE vid = %s', (vid, ))
        mydb.commit()

        

        ff=open("det.txt","r")
        v=ff.read()
        ff.close()
        vv=int(v)
        v1=vv-1
        vface1="User."+vid+"."+str(v1)+".jpg"
        i=2
        while i<vv:
            
            cursor.execute("SELECT max(id)+1 FROM ph_face")
            maxid = cursor.fetchone()[0]
            if maxid is None:
                maxid=1
            vface="User."+vid+"."+str(i)+".jpg"
            sql = "INSERT INTO ph_face(id, vid, vface) VALUES (%s, %s, %s)"
            val = (maxid, vid, vface)
            print(val)
            cursor.execute(sql,val)
            mydb.commit()
            i+=1

        
            
        cursor.execute('update ph_doctor set fimg=%s WHERE id = %s', (vface1, vid))
        mydb.commit()
        shutil.copy('static/faces/f1.jpg', 'static/photo/'+vface1)

        
        ##########
        
        ##Training face
        # Path for face image database
        path = 'dataset'

        recognizer = cv2.face.LBPHFaceRecognizer_create()

        # function to get the images and label data
        

        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))






        #################################################
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM ph_face where vid=%s",(vid, ))
        dt = cursor.fetchall()
        for rs in dt:
            ##Preprocess
            path="static/frame/"+rs[2]
            path2="static/process1/"+rs[2]
            mm2 = PIL.Image.open(path).convert('L')
            #rz = mm2.resize((200,200), PIL.Image.ANTIALIAS)
            rz = mm2.resize((200,200), Image.Resampling.LANCZOS)
            rz.save(path2)
            
            '''img = cv2.imread(path2) 
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
            path3="static/process2/"+rs[2]
            cv2.imwrite(path3, dst)'''
            #noice
            img = cv2.imread('static/process1/'+rs[2]) 
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
            fname2='ns_'+rs[2]
            cv2.imwrite("static/process1/"+fname2, dst)
            ######
            ##bin
            image = cv2.imread('static/process1/'+rs[2])
            original = image.copy()
            kmeans = kmeans_color_quantization(image, clusters=4)

            # Convert to grayscale, Gaussian blur, adaptive threshold
            gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3,3), 0)
            thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)
            
            # Draw largest enclosing circle onto a mask
            mask = np.zeros(original.shape[:2], dtype=np.uint8)
            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
            for c in cnts:
                ((x, y), r) = cv2.minEnclosingCircle(c)
                cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
                cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
                break
            
            # Bitwise-and for result
            result = cv2.bitwise_and(original, original, mask=mask)
            result[mask==0] = (0,0,0)

            
            ###cv2.imshow('thresh', thresh)
            ###cv2.imshow('result', result)
            ###cv2.imshow('mask', mask)
            ###cv2.imshow('kmeans', kmeans)
            ###cv2.imshow('image', image)
            ###cv2.waitKey()

            cv2.imwrite("static/process1/bin_"+rs[2], thresh)
            

            ###RPN - Segment
            img = cv2.imread('static/process1/'+rs[2])
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/fg_"+rs[2]
            segment.save(path3)
            ####
            img = cv2.imread('static/process2/fg_'+rs[2])
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/fg_"+rs[2]
            segment.save(path3)

            
            '''
            img = cv2.imread(path2)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # noise removal
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/"+rs[2]
            segment.save(path3)
            '''
            #####
            image = cv2.imread(path2)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 50, 100)
            image = Image.fromarray(image)
            edged = Image.fromarray(edged)
            path4="static/process3/"+rs[2]
            edged.save(path4)
            ##
        
        cursor.execute("SELECT count(*) FROM ph_face where vid=%s",(vid, ))
        cnt = cursor.fetchone()[0]
        
        return redirect(url_for('view_photo',vid=vid,act='success'))
        
    
    cursor.execute("SELECT * FROM ph_doctor")
    data = cursor.fetchall()
    return render_template('web/add_photo.html',data=data, vid=vid)

#Line Segment Detector
def LSD(img):
    img = cv2.imread('static/process2/'+img)
    lsd = cv2.createLineSegmentDetector(refine=cv2.LSD_REFINE_STD)

    # Detect lines
    lines = lsd.detect(gray)[0]  # lines will be a list of segments

    # Draw the lines on the original image
    drawn = lsd.drawSegments(img, lines)
def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))

@app.route('/view_photo',methods=['POST','GET'])
def view_photo():
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM ph_face where vid=%s",(vid, ))
        value = mycursor.fetchall()

    if request.method=='POST':
        print("Training")
        vid=request.form['vid']
        
        #shutil.copy('static/img/11.png', 'static/process4/'+rs[2])
       
        #return redirect(url_for('view_photo1',vid=vid))
        
    return render_template('web/view_photo.html', result=value,vid=vid)



@app.route('/pro1',methods=['POST','GET'])
def pro1():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM ph_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM ph_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('web/pro1.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro2',methods=['POST','GET'])
def pro2():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM ph_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None or act=='0':
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM ph_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('web/pro2.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro3',methods=['POST','GET'])
def pro3():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM ph_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM ph_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('web/pro3.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro4',methods=['POST','GET'])
def pro4():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM ph_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM ph_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('web/pro4.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro5',methods=['POST','GET'])
def pro5():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM ph_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM ph_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('web/pro5.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro6',methods=['POST','GET'])
def pro6():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM ph_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM ph_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('web/pro6.html', value=value,vid=vid, act=act3,s1=s1)

@app.route('/pro7',methods=['POST','GET'])
def pro7():
    s1=""
    vid = request.args.get('vid')
    act = request.args.get('act')
    value=[]
    
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM ph_face where vid=%s",(vid, ))
    cnt = mycursor.fetchone()[0]

    if act is None:
        act=1
        
    act1=int(act)-1
    act2=int(act)+1
    act3=str(act2)
    
    n=10
    if act1<n:
        s1="1"
        mycursor.execute("SELECT * FROM ph_face where vid=%s limit %s,1",(vid, act1))
        value = mycursor.fetchone()
    else:
        s1="2"

    
    return render_template('web/pro7.html', value=value,vid=vid, act=act3,s1=s1)


###Feature extraction & Classification
def CNN_process(self):
        
        train_data_preprocess = ImageDataGenerator(
                rescale = 1./255,
                shear_range = 0.2,
                zoom_range = 0.2,
                horizontal_flip = True)

        test_data_preprocess = (1./255)

        train = train_data_preprocess.flow_from_directory(
                'dataset/training',
                target_size = (128,128),
                batch_size = 32,
                class_mode = 'binary')

        test = train_data_preprocess.flow_from_directory(
                'dataset/test',
                target_size = (128,128),
                batch_size = 32,
                class_mode = 'binary')

        ## Initialize the Convolutional Neural Net

        # Initialising the CNN
        cnn = Sequential()

        # Step 1 - Convolution
        # Step 2 - Pooling
        cnn.add(Conv2D(32, (3, 3), input_shape = (128, 128, 3), activation = 'relu'))
        cnn.add(MaxPooling2D(pool_size = (2, 2)))

        # Adding a second convolutional layer
        cnn.add(Conv2D(32, (3, 3), activation = 'relu'))
        cnn.add(MaxPooling2D(pool_size = (2, 2)))

        # Step 3 - Flattening
        cnn.add(Flatten())

        # Step 4 - Full connection
        cnn.add(Dense(units = 128, activation = 'relu'))
        cnn.add(Dense(units = 1, activation = 'sigmoid'))

        # Compiling the CNN
        cnn.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

        history = cnn.fit_generator(train,
                                 steps_per_epoch = 250,
                                 epochs = 25,
                                 validation_data = test,
                                 validation_steps = 2000)

        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('Model Accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model Loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

        test_image = image.load_img('\\dataset\\', target_size=(128,128))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = cnn.predict(test_image)
        print(result)

        if result[0][0] == 1:
                print('feature extracted and classified')
        else:
                print('none')


def get_gps_and_time(image_path):
    img = Image.open(image_path)
    exif_data = piexif.load(img.info['exif'])

    gps = exif_data.get("GPS")
    if not gps:
        return None, None, None

    # Convert GPS to decimal
    def to_decimal(value, ref):
        d, m, s = [x[0] / x[1] for x in value]
        decimal = d + m / 60 + s / 3600
        return -decimal if ref in ['S', 'W'] else decimal

    lat = to_decimal(gps[piexif.GPSIFD.GPSLatitude], gps[piexif.GPSIFD.GPSLatitudeRef].decode())
    lon = to_decimal(gps[piexif.GPSIFD.GPSLongitude], gps[piexif.GPSIFD.GPSLongitudeRef].decode())

    # Get timestamp from EXIF
    date_time = exif_data["0th"].get(piexif.ImageIFD.DateTime)
    if date_time:
        date_time = date_time.decode()

    return lat, lon, date_time


@app.route('/doc_home',methods=['POST','GET'])
def doc_home():
    msg=""
    act=request.args.get("act")
    data=[]
    st=""
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_doctor where uname=%s",(uname, ))
    data = mycursor.fetchone()

    import datetime
    now1 = datetime.datetime.now()
    rdate=now1.strftime("%d-%m-%Y")
    edate1=now1.strftime("%Y-%m-%d")
    rtime=now1.strftime("%H:%M")

    ee=edate1.split("-")
    mon=ee[1]
    yr=ee[0]
    #print(rtime)
    mycursor.execute("update ph_doctor set smode=0 where uname=%s",(uname,))
    mydb.commit()
    
    mycursor.execute("SELECT * FROM ph_doctor")
    d11 = mycursor.fetchall()
    for d2 in d11:
        mycursor.execute("SELECT count(*) FROM ph_attendance where att_date=%s && docid=%s",(edate1,d2[7]))
        d1 = mycursor.fetchone()[0]
        if d1==0:
            mycursor.execute("SELECT max(id)+1 FROM ph_attendance")
            maxid2 = mycursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql = "INSERT INTO ph_attendance(id,docid,phc_id,att_date,month,year) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (maxid2,d2[7],d2[10],edate1,mon,yr)
            mycursor.execute(sql, val)
            mydb.commit()

        
        
    return render_template('web/doc_home.html', msg=msg,rs=data,rdate=rdate,edate1=edate1,rtime=rtime)

@app.route('/doc_test',methods=['POST','GET'])
def doc_test():
    msg=""
    act=request.args.get("act")
    data=[]
    st=""
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_doctor where uname=%s",(uname, ))
    data = mycursor.fetchone()

    import datetime
    now1 = datetime.datetime.now()
    rdate=now1.strftime("%d-%m-%Y")
    edate1=now1.strftime("%Y-%m-%d")
    rtime=now1.strftime("%H:%M")

    ee=edate1.split("-")
    mon=ee[1]
    yr=ee[0]
    #print(rtime)
    if request.method=='POST':
        smode=request.form['smode']
        mycursor.execute("update ph_doctor set smode=%s where uname=%s",(smode,uname))
        mydb.commit()
        return redirect(url_for('doc_capture'))

    return render_template('web/doc_test.html', msg=msg,rs=data,rdate=rdate,edate1=edate1,rtime=rtime)


@app.route('/setmode',methods=['POST','GET'])
def setmode():
    msg=""
    act=request.args.get("act")
    data=[]
    st=""
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_doctor where uname=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        smode=request.form['smode']
        mycursor.execute("update ph_doctor set smode=%s where uname=%s",(uname,))
        mydb.commit()
        return redirect(url_for('setmode'))
    

    return render_template('web/setmode.html', msg=msg,data=data)

#Geofencing Algorithm (Point-in-Polygon / Radius-based Check)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def is_inside_geofence(curr_lat, curr_lon, center_lat, center_lon, radius):
    distance = haversine(curr_lat, curr_lon, center_lat, center_lon)
    return distance <= radius

@app.route('/doc_capture',methods=['POST','GET'])
def doc_capture():
    msg=""
    act=request.args.get("act")
    data=[]
    st=""
    maxtime=10
    uname=""
    mess=""
    mess1=""
    mess2=""
    mess3=""

    email1=""
    email2=""
    email3=""
    mobile1=""
    mobile2=""
    mobile3=""
    m1=""
    clat=""
    clon=""

    lat=""
    lon=""
    st_alert=""
    
    if 'username' in session:
        uname = session['username']

    import datetime
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    rdate1=now.strftime("%Y-%m-%d")
    rtime=now.strftime("%H:%M")
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_doctor where uname=%s",(uname, ))
    data = mycursor.fetchone()
    phc_id=data[10]
    stime=int(data[11])
    etime=int(data[12])
    smin=int(data[13])
    smode=data[15]

    mycursor.execute("SELECT * FROM ph_ddhs order by id")
    of1 = mycursor.fetchall()
    for of11 in of1:
        email1=of11[3]
        mobile1=str(of11[2])

    mycursor.execute("SELECT * FROM ph_hmo order by id")
    of2 = mycursor.fetchall()
    for of21 in of2:
        email2=of21[3]
        mobile2=str(of21[2])

    mycursor.execute("SELECT * FROM ph_admin")
    of3 = mycursor.fetchall()
    for of31 in of3:
        email3=of31[2]

    

    mycursor.execute("SELECT max(id)+1 FROM ph_attendance")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    dimg=uname+"_"+str(maxid)+".jpg"

    #dimg="D1_2.jpg"
    ff=open("static/loc.txt","r")
    wloc=ff.read()
    ff.close()

    print("################")
    wc=wloc.split("|")    
    wc_len=len(wc)    
    wcn=wc_len-1    
    wn=randint(0,wcn)    
    wloc2=wc[wn]
    print(wloc2)
    wc2=wloc2.split(",")
    wlat=wc2[0]
    wlon=wc2[1]

    if act=="capture":
        image_path = "static/getimg.jpg"  # Change this to your image file
        image = cv2.imread(image_path)

        if image is not None:
            # Get GPS Coordinates and Current Time
            latitude, longitude = get_gps_coordinates()
            #current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_time=rdate+" "+rtime
            gps_text = f"Lat: {latitude:.6f}, Lon: {longitude:.6f}"
            
            ff=open("static/gps_loc.txt","r")
            gloc=ff.read()
            ff.close()
            gloc1=gloc.split(",")
            lat=gloc1[0]
            lon=gloc1[1]
        
            rd=current_time.split(" ")
            cdate=rdate1
            rd1=rd[1].split(":")
            chour=int(rd1[0])
            cmin=int(rd1[1])
            
            lt=gps_text.split(",")           
            lt1=lt[0].split(":")
            lt2=lt[1].split(":")

            print("current gps loc")
            print(gloc)

            #GPS Coordinates Validation [Ray Casting Algorithm]
            mycursor.execute("SELECT * FROM ph_hospital where phc_id=%s",(phc_id,))
            d4 = mycursor.fetchone()
            g1=d4[5]
            g2=g1.split('new google.maps.LatLng(')
            g21=''.join(g2)
            g22=g21.split('), ')
            print(g22)
            glen=len(g22)
            coors=[]
            i=1
            for g3 in g22:
                cr=[]
                if i<glen:
                    g31=g3.split(",")
                    print(g31)
                    clat=g31[0]
                    clon=g31[1]
                    g32=float(g31[0])
                    g33=float(g31[1])
                    cr.append(g32)
                    cr.append(g33)
                    coors.append(cr)
                i+=1


            ##




            if smode==2 or smode==4:
                lat=wlat
                lon=wlon
            elif smode==1 or smode==3:
                lat=clat
                lon=clon
                gps_text="Lat: "+lat+", Lon="+lon
            else:
                #lat=lt1[1].strip()
                #lon=lt2[1].strip()
                lat=gloc1[0]
                lon=gloc1[1]

            
            
            # Convert OpenCV image to PIL format
            img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(img_pil)

            # Define Box Position (Bottom Left)
            img_w, img_h = img_pil.size
            rect_w, rect_h = 350, 80  # Width and Height of GPS Box
            rect_x = 20  # Positioned at the left side
            rect_y = img_h - rect_h - 20  # Positioned near the bottom

            # Create Rounded Rectangle (White Background)
            radius = 20
            rectangle = Image.new("RGB", (rect_w, rect_h), (255, 255, 255))
            mask = Image.new("L", (rect_w, rect_h), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rounded_rectangle((0, 0, rect_w, rect_h), radius, fill=255)

            # Paste Rectangle onto Image
            img_pil.paste(rectangle, (rect_x, rect_y), mask)

            # Load Font and Draw Text
            font = ImageFont.truetype("static/fonts/ARIAL.ttf", 20)
            text_x, text_y = rect_x + 20, rect_y + 10  # Offset from the box
            time_x, time_y = rect_x + 20, rect_y + 40  # Position time below GPS

            draw.text((text_x, text_y), gps_text, font=font, fill=(0, 0, 0))
            draw.text((time_x, time_y), f"Time: {current_time}", font=font, fill=(0, 0, 0))

            # Convert back to OpenCV format
            final_img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

            # Save and Show Image
            output_path = "static/capture/"+dimg
            cv2.imwrite(output_path, final_img)
            print(f"Geo-tagged image saved as: {output_path}")

            ##
            #image_path = "static/capture/"+dimg
            #latitude, longitude, timestamp = get_gps_and_time(image_path)
            #print(f"Latitude: {latitude}\nLongitude: {longitude}\nTime: {timestamp}")
            ##

            
            latitude = float(lat)
            longitude = float(lon)
            point = Point(longitude, latitude)  # Note: shapely uses (x, y) = (lon, lat)

            # Example polygon (list of (longitude, latitude) tuples)
            '''polygon_coords = [
                (10.863341,78.645331),
                (10.865279,78.645578),
                (10.863466,78.651146),
                (10.861823,78.650899)
            ]'''
            polygon_coords = coors

            polygon = Polygon(polygon_coords)

            # Check if the point is inside the polygon
            if polygon.contains(point):
                s=1
                #print("The point is inside the polygon.")
            else:
                s=2
                #print("The point is outside the polygon.")
            ##
            #lat="10.861600"
            #lon="78.647000"
            lat1=lat.split(".")
            lon1=lon.split(".")
            lt1=int(lat1[0])
            lo1=int(lon1[0])

            ltt1=lat1[1]
            ltt2=ltt1[0:4]
            lt2=int(ltt2)
            
                       
            gn=len(g22)-1
            i=0
            geo1=0
            geo2=0
            gloc1=[]
            gloc2=[]
            while i<gn:
                #print(g24[i])
                gg=g22[i].split(',')
                
                l1=gg[0]
                l2=gg[1]

                f1=l1.split('.')
                geo1=int(f1[0])
                f2=f1[1]
                f3=f2[0:4]
                gloc1.append(f3)

                h1=l2.split('.')
                geo2=int(h1[0])
                h2=h1[1]
                h3=h2[0:4]
                gloc2.append(f3)
                
                i+=1

            ##
            gloc1.sort()
            #print(gloc1)
            gn=len(gloc1)-1
            gn1=int(gloc1[0])
            gn2=int(gloc1[gn])

            print(lt1)
            print(lt2)
            print(lo1)
            print(gn1)
            print(gn2)
            status=""
            if lt1==geo1 and lo1==geo2:
                if gn1<=lt2 and lt2<=gn2:
                    status="1"
                    print("geo")
                    #break
                else:
                    status="2"
                    mess2="Incorrect Location"
            else:
                status="2"

            print("geo st")
            print(status)
            #Time Based Validity
            tstatus="2"
            print(stime)
            print(etime)
            print(chour)
            if stime<=chour and chour<=etime:
                gmin=smin+maxtime
                hour1=stime+1
                
                
                if gmin>=60:
                    gmin1=gmin-60
                    if stime==chour:
                        if smin<=cmin and cmin<60:
                            tstatus="1"
                    elif hour1==chour:
                        if cmin>=0 and cmin<=gmin1:
                            tstatus="1"
                        

                elif stime==chour:
                    if smin<=cmin and cmin<=gmin:
                        tstatus="1"
            else:
                tstatus="2"
                mess3="Incorrect Time"
            ######face
            fstatus=""
            ff=open("static/cam1.txt","r")
            fst=ff.read()
            ff.close()

            if uname==fst:
                fstatus="1"
            else:
                fstatus="2"
                mess1="Face Not Matched"

            '''if smode==1 or smode==2:
                fstatus="1"

            elif smode==3 or smode==4:
                fstatus="2"
                
            elif uname==fst:
                fstatus="1"
            else:
                fstatus="2"
                mess1="Face Not Matched"'''

            mycursor.execute("SELECT count(*) FROM ph_attendance where att_date=%s && docid=%s",(cdate,uname))
            cnt = mycursor.fetchone()[0]
            '''if cnt==0:
            
    
                sql = "INSERT INTO ph_attendance(id,docid,phc_id,geo_image,latitude,longitude,att_date,att_time,face_st,geo_st,time_st) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (maxid,uname,phc_id,dimg,lat,lon,rd[0],rd[1],fstatus,status,tstatus)
                mycursor.execute(sql, val)
                mydb.commit()
            else:'''
            
            print("####################################################################")
            
            att_st="0"

            if fstatus=="2" and status=="2":
                st="1"
                att_st="2"
                mess="Doctor ID: "+uname+", Face and Location not Matched"
                m1="1"
            elif fstatus=="1" and status=="2":
                st="1"
                att_st="2"
                mess="Doctor ID: "+uname+", Face Matched, Location not Matched"
                m1="2"
            elif fstatus=="2" and status=="1":
                st="1"
                att_st="2"
                mess="Doctor ID: "+uname+", Face not Matched, Location Matched"
                m1="3"
            elif fstatus=="1" and status=="1":
                st="2"
                att_st="1"
                mess="Doctor ID: "+uname+", Face and Location Matched"
                m1="4"
                fn5=uname+"_dt.txt"
                ff=open("static/check/"+fn5,"w")
                ff.write(rdate)
                ff.close()

            else:
                st="2"
                mess="Attendance Captured"

            count_random = 0
            count_att_fail = 0

            mycursor.execute("""
                SELECT count_random, count_att_fail
                FROM ph_attendance
                WHERE att_date=%s AND docid=%s
            """, (cdate, uname))

            rw = mycursor.fetchone()

            if rw is not None:
                count_random = rw[0] if rw[0] is not None else 0
                count_att_fail = rw[1] if rw[1] is not None else 0
            
            if att_st=="1":
                print("aa")
                count_random=count_random+1
            else:
                print("bb")
                count_random=count_random+1
                count_att_fail=count_att_fail+1

            scr=0
            
            if count_random>0 and count_att_fail>0:
                scr=(count_att_fail/count_random)*100

            if scr<70 and scr>0:
                st_alert="1"

            print("#-----------------#")
            print(cdate)
            print(uname)
            mycursor.execute("update ph_attendance set geo_image=%s,latitude=%s,longitude=%s,att_time=%s,face_st=%s,geo_st=%s,time_st=%s,att_st=%s where att_date=%s AND docid=%s",(dimg,lat,lon,rd[1],fstatus,status,tstatus,att_st,cdate,uname))
            mydb.commit()

            mycursor.execute("update ph_attendance set count_random=%s,count_att_fail=%s where att_date=%s AND docid=%s",(count_random,count_att_fail,cdate,uname))
            mydb.commit()
            
            
        
    return render_template('web/doc_capture.html', msg=msg,act=act,rs=data,dimg=dimg,mess=mess,st=st,email1=email1,email2=email2,email3=email3,mobile1=mobile1,mobile2=mobile2,m1=m1,uname=uname,st_alert=st_alert)

def is_time_between(start, end, check):
    fmt = "%H:%M"
    start = datetime.strptime(start, fmt).time()
    end = datetime.strptime(end, fmt).time()
    check = datetime.strptime(check, fmt).time()
    return start <= check <= end

def is_time_between2(start, end, check):
    fmt = "%H:%M"
    start = datetime.strptime(start, fmt).time()
    end = datetime.strptime(end, fmt).time()
    check = datetime.strptime(check, fmt).time()

    if start <= end:
        return start <= check <= end
    else:
        # crosses midnight
        return check >= start or check <= end


#Random Interval Verification Algorithm (Rule-based Scheduler)
def generate_random_intervals(start_time, end_time, count=3):
    intervals = []
    total_seconds = int((end_time - start_time).total_seconds())

    for _ in range(count):
        random_sec = random.randint(0, total_seconds)
        intervals.append(start_time + timedelta(seconds=random_sec))

    return sorted(intervals)

@app.route('/check_att',methods=['POST','GET'])
def check_att():
    st=""
    dst=""
    mess=""
    uname=""
    rst=""
    if 'username' in session:
        uname = session['username']
    time_st=False
    fn=uname+"_cr.txt"
    fn2=uname+"_tm.txt"
    fn3=uname+"_doc.txt"
    fn4=uname+"_fence.txt"
    fn5=uname+"_dt.txt"

    import datetime
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H:%M:%S")
    ctime=now.strftime("%H:%M")
    
    ff=open("static/check/"+fn,"r")
    dt=ff.read()
    ff.close()

    ff=open("static/check/"+fn2,"r")
    ftime=ff.read()
    ff.close()

    ff=open("static/check/"+fn3,"r")
    doc=ff.read()
    ff.close()

    ff=open("static/check/"+fn4,"r")
    fst=ff.read()
    ff.close()

    
    ff=open("static/check/"+fn5,"r")
    f_date=ff.read()
    ff.close()

    if f_date==rdate:
        dst="1"

    ##doc det,officer contact
    dc=doc.split("|")
    dname=dc[0]
    did=dc[1]
    mobile1=dc[2]
    email1=dc[3]
    mobile2=dc[4]
    email2=dc[5]
    email3=dc[6]
    phc_id=dc[7]
    ##Time
    atime=ftime.split(",")
    sh=atime[0].split(":")
    eh=atime[1].split(":")
    if sh<=eh:
        time_st=is_time_between(atime[0], atime[1], ctime)
    else:
        time_st=is_time_between2(atime[0], atime[1], ctime)
    a=1
    #if time_st==True:
    if a==1:
        rn1=randint(1,20)
        print(rn1)
        if rn1==5 or rn1==10 or rn1>=15:
            rst="1"
        
    
    return render_template('web/check_att.html',st=st,mess=mess,mobile1=mobile1,email1=email1,mobile2=mobile2,email2=email2,email3=email3,dst=dst,rst=rst)


#Continuous Location Monitoring Algorithm (Time-based Tracking)
GPS_INTERVAL_MINUTES = 15

def check_gps_updates(gps_logs):
    alerts = []
    for i in range(1, len(gps_logs)):
        time_diff = (gps_logs[i]["time"] - gps_logs[i-1]["time"]).seconds / 60
        if time_diff > GPS_INTERVAL_MINUTES + 5:
            alerts.append("GPS update missing or delayed")
    return alerts

@app.route('/check_loc',methods=['POST','GET'])
def check_loc():
    st=""
    dst=""
    mess=""
    status=""
    uname=""
    if 'username' in session:
        uname = session['username']

    conn = get_db_connection()
    mycursor = conn.cursor()
    time_st=False
    fn=uname+"_cr.txt"
    fn2=uname+"_tm.txt"
    fn3=uname+"_doc.txt"
    fn4=uname+"_fence.txt"
    fn5=uname+"_dt.txt"

    import datetime
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H:%M:%S")
    ctime=now.strftime("%H:%M")
    
    ff=open("static/check/"+fn,"r")
    dt=ff.read()
    ff.close()

    ff=open("static/check/"+fn2,"r")
    ftime=ff.read()
    ff.close()

    ff=open("static/check/"+fn3,"r")
    doc=ff.read()
    ff.close()

    ff=open("static/check/"+fn4,"r")
    fst=ff.read()
    ff.close()

    
    ff=open("static/check/"+fn5,"r")
    f_date=ff.read()
    ff.close()

    if f_date==rdate:
        dst="1"

    ##doc det,officer contact
    dc=doc.split("|")
    dname=dc[0]
    did=dc[1]
    mobile1=dc[2]
    email1=dc[3]
    mobile2=dc[4]
    email2=dc[5]
    email3=dc[6]
    phc_id=dc[7]
    ##Time
    atime=ftime.split(",")
    sh=atime[0].split(":")
    eh=atime[1].split(":")
    if sh<=eh:
        time_st=is_time_between(atime[0], atime[1], ctime)
    else:
        time_st=is_time_between2(atime[0], atime[1], ctime)
    
    

    ###loc coors
    coors=[]
    i=1    
    ds1=dt.split("|")
    glen=len(ds1)
    for ds11 in ds1:
        cr=[]
        if i<glen:
            ds2=ds11.split(",")
            clat=ds2[0]
            clon=ds2[1]
            g32=float(clat)
            g33=float(clon)
            cr.append(g32)
            cr.append(g33)
            coors.append(cr)
        i+=1

    
    ##

    if request.method=='POST':
        lat=request.form['lat']
        lon=request.form['lon']
        
        #lat="10.861600"
        #lon="78.647000"
        ##
        '''ff=open("static/gps_loc.txt","r")
        gloc=ff.read()
        ff.close()
        gloc1=gloc.split(",")
        lat=gloc1[0]
        lon=gloc1[1]'''
        ##
            
        lat1=lat.split(".")
        lon1=lon.split(".")

        lt1=lat1[1]
        lo1=lon1[1]

        lt2=lt1[0:6]
        lo2=lo1[0:6]

        lt3=lat1[0]+"."+lt2
        lo3=lon1[0]+"."+lo2

        lt4=float(lt3)
        lo4=float(lo3)
        
        if time_st==True:
            fence = Polygon(coors)
            point = Point(lt4,lo4)

            if fence.contains(point):
                print("inside hospital")

                if fst=="2" or fst=="":
                    
                    mycursor.execute("SELECT max(id)+1 FROM ph_logs")
                    maxid = mycursor.fetchone()[0]
                    if maxid is None:
                        maxid=1
                    status="Inside Hospital"
                    sql = "INSERT INTO ph_logs(id,doctor,docid,phc_id,status,rdate,rtime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    val = (maxid,dname,did,phc_id,status,rdate,rtime)
                    mycursor.execute(sql, val)
                    #mydb.commit()
                    
                ff=open("static/check/"+fn4,"w")
                ff.write("1")
                ff.close()
            else:
                print("Outside hospital")
                if fst=="1":
                    st="1"                    
                    mess="Doctor: "+dname+" [ID: "+did+"], Outside of Hospital"
                    
                    mycursor.execute("SELECT max(id)+1 FROM ph_logs")
                    maxid = mycursor.fetchone()[0]
                    if maxid is None:
                        maxid=1
                    status="Outside Hospital"
                    sql = "INSERT INTO ph_logs(id,doctor,docid,phc_id,status,rdate,rtime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    val = (maxid,dname,did,phc_id,status,rdate,rtime)
                    mycursor.execute(sql, val)
                    #mydb.commit()
                    
                    ff=open("static/check/"+fn4,"w")
                    ff.write("2")
                    ff.close()

                    
    mycursor.close()
    conn.close()
    return render_template('web/check_loc.html',st=st,mess=mess,mobile1=mobile1,email1=email1,mobile2=mobile2,email2=email2,email3=email3,dst=dst,status=status)

#Violation Detection & Alerting 
def detect_violations(face_ok, geo_ok, gps_ok, random_check_missed):
    violations = []

    if not face_ok:
        violations.append("Face verification failed")

    if not geo_ok:
        violations.append("Geofence breach detected")

    if not gps_ok:
        violations.append("GPS silence or delay")

    if random_check_missed:
        violations.append("Random verification missed")

    return violations

# Function to get GPS Coordinates
def get_gps_coordinates():
    g = geocoder.ip('me') 
    return g.latlng if g.latlng else (0.0, 0.0)

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json['image']  # Get base64 image data
    image_data = base64.b64decode(data.split(',')[1])  # Decode base64

    # Convert to OpenCV format
    np_arr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Save image
    image_path = "static/capture/c1.jpg"
    cv2.imwrite(image_path, image)

    return jsonify({"image_url": image_path})  # Send image URL back to frontend


@app.route('/doc_patview',methods=['POST','GET'])
def doc_patview():
    msg=""
    act=request.args.get("act")
    data=[]
    data1=[]
    st=""
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_doctor where uname=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        rdate=request.form['rdate']

        mycursor.execute("SELECT count(*) FROM ph_patient where docid=%s && rdate=%s",(uname,rdate ))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            st="1"
            mycursor.execute("SELECT * FROM ph_patient where docid=%s && rdate=%s",(uname,rdate ))
            data1 = mycursor.fetchall()
        
    return render_template('web/doc_patview.html', msg=msg,rs=data,st=st,data1=data1)

@app.route('/doc_addpat',methods=['POST','GET'])
def doc_addpat():
    msg=""
    act=request.args.get("act")
    data=[]
    st=""
    uname=""
    if 'username' in session:
        uname = session['username']


    import datetime
    now1 = datetime.datetime.now()
    rdate=now1.strftime("%d-%m-%Y")
    edate1=now1.strftime("%Y-%m-%d")
    rtime=now1.strftime("%H:%M")

    ed=edate1.split("-")
    mon=ed[1]
    yr=ed[0]
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_doctor where uname=%s",(uname, ))
    data = mycursor.fetchone()
    phc_id=data[10]

    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        age=request.form['age']
        aadhar=request.form['aadhar']  
        disease=request.form['disease']
        symptom=request.form['symptom']
        prescribe=request.form['prescribe']  

        mycursor.execute("SELECT max(id)+1 FROM ph_patient")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO ph_patient(id,docid,phc_id,name,gender,age,aadhar,disease,symptom,prescribe,rdate,month,year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,phc_id,name,gender,age,aadhar,disease,symptom,prescribe,edate1,mon,yr)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
        
    return render_template('web/doc_addpat.html', msg=msg,rs=data)
    
@app.route('/ddhs_home',methods=['POST','GET'])
def ddhs_home():
    msg=""
    act=request.args.get("act")
    data=[]
    st=""
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_ddhs where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
        
    return render_template('web/ddhs_home.html', msg=msg,rs=data)

@app.route('/ddhs_monitor',methods=['POST','GET'])
def ddhs_monitor():
    msg=""
    act=request.args.get("act")
    data=[]
    st=""
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_ddhs where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ph_hospital")
    phos = mycursor.fetchall()

    if request.method=='POST':
        phc_id=request.form['phc_id']        
        rdate=request.form['rdate']

        mycursor.execute("SELECT count(*) FROM ph_attendance where phc_id=%s && att_date=%s",(phc_id, rdate))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            st="1"
            mycursor.execute("SELECT * FROM ph_attendance where phc_id=%s && att_date=%s",(phc_id, rdate))
            data = mycursor.fetchall()
        else:
            st="2"
        
    return render_template('web/ddhs_monitor.html', msg=msg,data=data,st=st,phos=phos)


@app.route('/ddhs_report',methods=['POST','GET'])
def ddhs_report():
    msg=""
    act=request.args.get("act")
    adata=[]
    st=""
    uname=""
    month=""
    year=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_ddhs where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ph_hospital")
    phos = mycursor.fetchall()

    mycursor.execute("SELECT distinct(month) FROM ph_attendance order by month")
    mdata = mycursor.fetchall()

    mycursor.execute("SELECT distinct(year) FROM ph_attendance order by year desc")
    ydata = mycursor.fetchall()
    

    if request.method=='POST':
        phc_id=request.form['phc_id']
        month=request.form['month']
        year=request.form['year']   
       
        mycursor.execute("SELECT count(*) FROM ph_doctor where phc_id=%s",(phc_id, ))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            st="1"
            mycursor.execute("SELECT * FROM ph_doctor where phc_id=%s",(phc_id, ))
            dat = mycursor.fetchall()
            
            for dat1 in dat:
                dt1=[]
                dt1.append(dat1[1])
                dt1.append(dat1[6])
                dt1.append(dat1[3])
                dt1.append(dat1[4])

                t_pre=0
                t_abs=0
                c1=0
                mycursor.execute("SELECT * FROM ph_attendance where month=%s && year=%s group by att_date",(month,year))
                cntt = mycursor.fetchall()
                for cn in cntt:
                    c1+=1

                    
                tot_days=c1

                dimg=""
                per1=0
                
                mycursor.execute("SELECT count(*) FROM ph_attendance where docid=%s && month=%s && year=%s",(dat1[7],month,year))
                cnt = mycursor.fetchone()[0]
                if cnt>0:
                    mycursor.execute("SELECT count(*) FROM ph_attendance where docid=%s && month=%s && year=%s && att_st=1 ",(dat1[7],month,year))
                    cnt1 = mycursor.fetchone()[0]
                    t_pre=cnt1

                    mycursor.execute("SELECT count(*) FROM ph_attendance where docid=%s && month=%s && year=%s && att_st=0 ",(dat1[7],month,year))
                    cnt2 = mycursor.fetchone()[0]
                    t_abs=cnt2

                    mycursor.execute("SELECT * FROM ph_attendance where docid=%s order by id desc limit 0,1",(dat1[7],))
                    dd = mycursor.fetchall()
                    for dd1 in dd:
                        dimg=dd1[3]
                    

                per=(t_pre/tot_days)*100
                per1=round(per,2)

                dt1.append(t_pre)
                dt1.append(t_abs)
                dt1.append(per1)
                dt1.append(dimg)
                dt1.append(dat1[7])

                print(dt1)
                adata.append(dt1)
                
            


            
        else:
            st="2"
        
    return render_template('web/ddhs_report.html', msg=msg,data=data,adata=adata,st=st,phos=phos,mdata=mdata,ydata=ydata,month=month,year=year)

@app.route('/ddhs_pat',methods=['POST','GET'])
def ddhs_pat():
    msg=""
    act=request.args.get("act")
    docid=request.args.get("docid")
    month=request.args.get("month")
    year=request.args.get("year")
    adata=[]
    st=""
    uname=""
  
    if 'username' in session:
        uname = session['username']

                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_ddhs where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    mycursor.execute("SELECT * FROM ph_patient where docid=%s && month=%s && year=%s",(docid,month,year))
    data1 = mycursor.fetchall()

    return render_template('web/ddhs_pat.html', msg=msg,data=data,data1=data1,docid=docid)

                           
@app.route('/ddhs_report2',methods=['POST','GET'])
def ddhs_report2():
    msg=""
    data1=[]
    act=request.args.get("act")
    docid=request.args.get("docid")
    month=request.args.get("month")
    year=request.args.get("year")
    data=[]
    st=""
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_ddhs where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ph_hospital")
    phos = mycursor.fetchall()



    mycursor.execute("SELECT count(*) FROM ph_attendance where docid=%s && month=%s && year=%s",(docid, month,year))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM ph_attendance where docid=%s && month=%s && year=%s",(docid, month,year))
        data1 = mycursor.fetchall()
    else:
        st="2"
        
    return render_template('web/ddhs_report2.html', msg=msg,data=data,data1=data1,st=st,phos=phos,docid=docid,month=month,year=year)


@app.route('/hmo_monitor',methods=['POST','GET'])
def hmo_monitor():
    msg=""
    act=request.args.get("act")
    data=[]
    st=""
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_hmo where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ph_hospital")
    phos = mycursor.fetchall()

    if request.method=='POST':
        phc_id=request.form['phc_id']        
        rdate=request.form['rdate']

        mycursor.execute("SELECT count(*) FROM ph_attendance where phc_id=%s && att_date=%s",(phc_id, rdate))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            st="1"
            mycursor.execute("SELECT * FROM ph_attendance where phc_id=%s && att_date=%s",(phc_id, rdate))
            data = mycursor.fetchall()
        else:
            st="2"
        
    return render_template('web/hmo_monitor.html', msg=msg,data=data,st=st,phos=phos)

@app.route('/hmo_home',methods=['POST','GET'])
def hmo_home():
    msg=""
    act=request.args.get("act")
    data=[]
    st=""
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_hmo where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
        
    return render_template('web/hmo_home.html', msg=msg,rs=data)

@app.route('/hmo_report',methods=['POST','GET'])
def hmo_report():
    msg=""
    act=request.args.get("act")
    data=[]
    data1=[]
    st=""
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("static/cam1.txt","w")
    ff.write("")
    ff.close()
                    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ph_hmo where uname=%s",(uname, ))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ph_doctor")
    pdata = mycursor.fetchall()

    mycursor.execute("SELECT distinct(month) FROM ph_attendance order by month")
    mdata = mycursor.fetchall()

    mycursor.execute("SELECT distinct(year) FROM ph_attendance order by year desc")
    ydata = mycursor.fetchall()

    if request.method=='POST':
        docid=request.form['docid']        
        month=request.form['month']
        year=request.form['year']

        mycursor.execute("SELECT count(*) FROM ph_attendance where docid=%s && month=%s && year=%s && att_st=0",(docid, month,year))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            st="1"
            mycursor.execute("SELECT * FROM ph_attendance where docid=%s && month=%s && year=%s && att_st=0",(docid, month,year))
            data1 = mycursor.fetchall()
        else:
            st="2"
        
    return render_template('web/hmo_report.html', msg=msg,data=data,st=st,pdata=pdata,mdata=mdata,ydata=ydata,data1=data1)



@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #session.pop('username', None)
    return redirect(url_for('index'))


#######
def gen2(camera):
    while True:
        frame = camera.get_frame()
    

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/video_feed2')
def video_feed2():

    return Response(gen2(VideoCamera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
##########
def gen(camera):

    while True:
        frame = camera.get_frame()
    

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    
@app.route('/video_feed')
def video_feed():
    
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



#########
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
