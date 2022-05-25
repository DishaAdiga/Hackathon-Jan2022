from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
import mysql.connector
from main.distance import location
from random import randint
from main.mails import send_mail
# Create your views here.
def clogin(request,*args,**kwargs):
    if request.method=="POST":
            name=request.POST['name']
            password=request.POST['password']
            user=auth.authenticate(username=name,password=password)
            if user is not None: #if user id and password is same
                hostelid=name
                auth.login(request,user)
                return redirect('chome')
            else:
                messages.info(request,'invalid credentials')
                return render(request,"clogin.html")   

    return render(request,'clogin.html')
def feedback(request,*args,**kwargs):
    return render(request,'feedback.html')
def customerhistory(request,*args,**kwargs):
    return render(request,'customerhistory.html')


def tocmrit(request,*args,**kwargs):
    arr=[
    ["MAHADEVAPURA",1],
    ["HOODI",2],
    ["WHITEFIELD",3],
    ["MARATHAHALLI",4],
    ["KR PURAM",5],
    ["MG ROAD",6],
    ["HAL",7],
    ["RM NAGAR",8]
    ]
    my_dicti={'val':arr}
    if(request.method=='POST'):
        first_point="TO CMRIT"
        date=request.POST['date']
        d_location=arr[int(request.POST['location'])-1][0]
        print("check below")
        print(first_point,date,d_location)
        db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon") 
        cur = db.cursor()
        cur.execute("select time,name,vtype,date from otrip,owner where date=%s and source=%s and stops=%s and oid=id",(date,first_point,d_location,))
        s=cur.fetchall()
        price=randint(100,151)
        
    
        my_dicti={'val':arr,'auxi':s,'location':d_location,'price':price}
        print(s)
        return render(request,'tocmrit.html',my_dicti)
    return render(request,'tocmrit.html',my_dicti)
def ownerequest(request,*args,**kwargs):
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon") 
    cur = db.cursor()
    cur.execute("select username from auth_user where id=%s",(request.user.id,))
    s=cur.fetchall()
    name=s[0][0]
    status=2
    cur.execute("select c_name,location,date,price,for_trip from request where o_name=%s and status=%s",(name,status,))
    s=cur.fetchall()
    my_dicti={'val':s}
    if(request.method=='POST'):
        status=0
        c_name=request.POST.get('c_name',False)
        print("this is post")
        print(c_name)
        send_mail(100,c_name,name)
        cur.execute("update request set status=%s where c_name=%s",(status,c_name,))
        db.commit() 
        db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon")
        db.commit() 
        cur = db.cursor()
        cur.execute("select username from auth_user where id=%s",(request.user.id,))
        s=cur.fetchall()
        name=s[0][0]
        status=2
        cur.execute("select c_name,location,date,price,for_trip from request where o_name=%s and status=%s and o_name=%s",(name,status,name))
        s=cur.fetchall()

        
        return render(request,'ownerequest.html',my_dicti);


    return render(request,'ownerequest.html',my_dicti);
def tohome(request,*args,**kwargs):
    arr=[
    ["MAHADEVAPURA",1],
    ["HOODI",2],
    ["WHITEFIELD",3],
    ["MARATHAHALLI",4],
    ["KR PURAM",5],
    ["MG ROAD",6],
    ["HAL",7],
    ["RM NAGAR",8]
    ]
    my_dicti={'val':arr}
    if(request.method=='POST'):
        first_point="FROM CMRIT"
        date=request.POST['date']
        d_location=arr[int(request.POST['location'])-1][0]
        print("check below")
        print(first_point,date,d_location)
        db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon") 
        cur = db.cursor()
        cur.execute("select time,name,vtype,date from otrip,owner where date=%s and source=%s and stops=%s and oid=id",(date,first_point,d_location,))
        s=cur.fetchall()
        if(len(s)!=0):
            c_type=s[0][2][5]
        price=randint(100,151)
        my_dicti={'val':arr,'auxi':s,'location':d_location,'price':price}
        print(s)
        return render(request,'tohome.html',my_dicti)

    return render(request,'tohome.html',my_dicti)
def chome(request,*args,**kwargs):
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon") 
    cur = db.cursor()
    cur.execute("update auth_user set is_staff=1 where id=%s",(request.user.id,))
    db.commit()
    return render(request,'chome.html')

def cregister(request,*args,**kwargs):
    if(request.method == 'POST'):
        name=request.POST['name'] #gets value from the frontend 
        password=request.POST['password']
        if User.objects.filter(username=name).exists(): #checks if the user requests
             messages.info(request,'Username Taken')
             return render(request,'cregister.html')  #redirects the register page again
        else:
            user = User.objects.create_user(username=name, password=password)
            user.save() #its saves the users id and password in the databasse
            return render(request,'clogin.html')
    return render(request,'cregister.html')
    
def reqc(request,*args,**kwargs):
    arr=[
    ["MAHADEVAPURA",1],
    ["HOODI",2],
    ["WHITEFIELD",3],
    ["MARATHAHALLI",4],
    ["KR PURAM",5],
    ["MG ROAD",6],
    ["HAL",7],
    ["RM NAGAR",8]
    ]
    my_dicti={'val':arr}
    o_name=request.POST.get('name',False) #gets value from the frontend 
    date=request.POST.get('date',False)
    price=request.POST.get('price',False)
    location=request.POST.get('location',False)
    for_trip="FROM CMRIT"
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon") 
    cur = db.cursor()
    print(request.user)
    cur.execute("select username from auth_user where id=%s",(request.user.id,))
    s=cur.fetchall()
    c_name=s[0][0]
    print(o_name,c_name,location,date)
    status=2
    cur.execute("insert into request(o_name,c_name,location,date,price,for_trip,status) values(%s,%s,%s,%s,%s,%s,%s)",(o_name,c_name,location,date,price,for_trip,status,));
    db.commit()
    return render(request,'tohome.html',my_dicti)


def reqp(request,*args,**kwargs):
    arr=[
    ["MAHADEVAPURA",1],
    ["HOODI",2],
    ["WHITEFIELD",3],
    ["MARATHAHALLI",4],
    ["KR PURAM",5],
    ["MG ROAD",6],
    ["HAL",7],
    ["RM NAGAR",8]
    ]
    my_dicti={'val':arr}
    o_name=request.POST.get('name',False) #gets value from the frontend 
    date=request.POST.get('date',False)
    price=request.POST.get('price',False)
    location=request.POST.get('location',False)
    for_trip="TO CMRIT"
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon") 
    cur = db.cursor()
    print(request.user)
    cur.execute("select username from auth_user where id=%s",(request.user.id,))
    s=cur.fetchall()
    c_name=s[0][0]
    print(o_name,c_name,location,date)
    status=2
    cur.execute("insert into request(o_name,c_name,location,date,price,for_trip,status) values(%s,%s,%s,%s,%s,%s,%s)",(o_name,c_name,location,date,price,for_trip,status,));
    db.commit()
    return render(request,'tocmrit.html',my_dicti)

def login(request,*args,**kwargs):

    if request.method=="POST":
            name=request.POST['name']
            password=request.POST['password']
            user=auth.authenticate(username=name,password=password)
            global hostelid
            if user is not None: #if user id and password is same
                hostelid=name
                auth.login(request,user)
                return redirect('home')
            else:
                messages.info(request,'invalid credentials')
                return render(request,"login.html")   

    return render(request,'login.html')


def home(request,*args,**kwargs):
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon") 
    cur = db.cursor()
    cur.execute("select vtype,vno,seats,contact,name from owner where id=%s",(request.user.id,))
    s=cur.fetchall()
    print(s)
    my_dicti={}
    if(len(s)!=0):
        my_dicti={'vtype':s[0][0],'vno':s[0][1],'seats':s[0][2],'contact':s[0][3],'name':s[0][3]}
    return render(request,'home.html',my_dicti)
def index(request,*args,**kwargs):
    return render(request,'index.html')

def register(request,*args,**kwargs):
    if(request.method == 'POST'):
        name=request.POST['name'] #gets value from the frontend 
        password=request.POST['password']
        if User.objects.filter(username=name).exists(): #checks if the user requests
             messages.info(request,'Username Taken')
             return render(request,'register.html')  #redirects the register page again
        else:
            user = User.objects.create_user(username=name, password=password)
            user.save() #its saves the users id and password in the databasse
            return render(request,'login.html')
    return render(request,'register.html')

def vehicleDetails(request,*args,**kwargs):
    if(request.method=='POST'):
        db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon") 
        cur = db.cursor()
        cur.execute("select username from auth_user where id=%s",(request.user.id,))
        s=cur.fetchall()
        user=s[0][0]
        id=request.user.id
        print(id,user)
        vno=request.POST['vno']
        vtype=request.POST['vtype']
        vseats=request.POST['vseats']
        vcontact=request.POST['vcontact']

        values= (id,user,vno,vtype,vseats,vcontact,)
        db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon") 
        cur = db.cursor()
        cur.execute("INSERT INTO owner(id,name,vno,vtype,seats,contact) VALUES(%s,%s,%s,%s,%s,%s)",values)
        db.commit()
        print(vno,vtype,vseats,vcontact)
        return redirect('home')
    
    return render(request,'vehicledetails.html')

def otrip(request,*args,**kwargs):
    user_id=request.user.id
    arr=[
    ["MAHADEVAPURA",1],
    ["HOODI",2],
    ["WHITEFIELD",3],
    ["MARATHAHALLI",4],
    ["KR PURAM",5],
    ["MG ROAD",6],
    ["HAL",7],
    ["RM NAGAR",8]
    ]
    
    db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon") 
    cur = db.cursor()
    cur.execute("select oid,stops,time from otrip where oid=%s",(user_id,))
    temp=cur.fetchall()
    my_dicti={'val':arr,'auxi':temp}
    if(request.method=='POST'):
        location=request.POST['location']
        if(location=='1'):
            location="FROM CMRIT"
        else:
            location="TO CMRIT"
        date=request.POST['date']
        stops=request.POST.get('stops', False)
        stops=arr[int(stops)-1][0]
        time=request.POST['time']
        print(request.POST)
        db = mysql.connector.connect(host="localhost",user="root",password="2580",database="hackathon") 
        cur = db.cursor()
        user_id=request.user.id
        values=(user_id,date,location,stops,time)
        print(user_id,date,location,stops,time)
        cur.execute("INSERT INTO otrip(oid,date,source,stops,time) VALUES(%s,%s,%s,%s,%s)",values)
        db.commit()
        return redirect('otrip')
    
    return render(request,'otrip.html',my_dicti)

def ownerhistory(request,*args,**kwargs):
    return render(request,'ownerhistory.html')

def payments(request,*args,**kwargs):
    return render(request,'payment.html')