from Suga import app,bcrypt,db,mail
from flask import Flask,url_for,render_template,redirect,flash,request
from flask_login import current_user,login_user,logout_user,login_required,current_user
from Suga.forms import RegisterForm,FoodForm,LoginForm,CityForm,VolRegisterForm,VolUpdateForm,UpdateRegisterForm,ResetLinkForm,ResetPassForm
from Suga.models import FoodDonors,FoodGetters,notifyme
import os
import secrets
from Suga.req import fun
from flask_mail import Message


@app.route('/',methods=['GET','POST'])
def home():
    f=FoodForm()
    x,y=fun()
    if f.validate_on_submit():
        print(f.name.data,f.tfood.data)
        u=FoodDonors(name=f.name.data,contactno=f.contactno.data,city=f.city.data,email=f.email.data,address=f.address.data,tfood=f.tfood.data)
        db.session.add(u)
        db.session.commit()
        print(u.id)
        flash('You have posted succesfully.Thankyou for helping the needy!God Bless','success')
        return redirect(url_for('home'))
    return render_template('home.html',f=f,x=x,y=y)

@app.route('/donorsready',methods=['GET','POST'])
@login_required
def donorsready():
    f=CityForm()
    if f.validate_on_submit():
         letcity=FoodDonors.query.filter_by(city=f.city.data).order_by(FoodDonors.date.desc())
         x,y=fun()
         print(x,y)
         l=[]
         for i in letcity:
             if i.taken=='False' or i.taken=='TrueP':
                 l.append(i)
         return render_template('donorsready.html',f=f,fd=l,x=x,y=y)
    city=current_user.city
    print(city)
    l=[]
    fd=FoodDonors.query.filter_by(city=city).order_by(FoodDonors.date.desc())
    for i in fd:
        if i.taken=="False" or i.taken=='TrueP':
            l.append(i)
    print(l)
    x,y=fun()
    print(x,y)
    return render_template('donorsready.html',f=f,fd=l,x=x,y=y)

def save_pic(pic,name):
       x=secrets.token_hex(8)
       f_name,f_ext=os.path.splitext(pic.filename)
       filename=x+name+f_ext
       print(filename)
       path=os.path.join(app.root_path,'static/certpics',filename)
       pic.save(path)
       return filename


@app.route('/Register',methods=['GET','POST'])
def register():
    f=RegisterForm()
    flash('Register','success')
    x,y=fun()
    if request.method=='POST':
         if f.validate_on_submit():
            certname=save_pic(f.pic.data,f.name.data)
            hashed=bcrypt.generate_password_hash(f.password.data).decode('utf-8')
            g=FoodGetters(name=f.name.data,year=f.year.data,city=f.city.data,email=f.email.data,password=hashed,address=f.address.data,mobileno=f.mobileno.data,pic=certname,volunteer="False")
            db.session.add(g)
            db.session.commit()
            flash('Success','success')
            return redirect(url_for('home'))
         else:
              print(f.errors)
              print('cant validate')    

    return render_template('register.html',title="Register",f=f,x=x,y=y)


@app.route('/volregister',methods=['GET','POST'])
def volregister():
    f=VolRegisterForm()
    x,y=fun()
    if request.method=='POST':
         if f.validate_on_submit():
            picname=save_pic(f.pic.data,f.name.data)
            hashed=bcrypt.generate_password_hash(f.password.data).decode('utf-8')
            g=FoodGetters(name=f.name.data,year=f.year.data,city=f.city.data,email=f.email.data,password=hashed,address=f.address.data,mobileno=f.mobileno.data,pic=picname,volunteer="True")
            db.session.add(g)
            db.session.commit()
            flash('Success','success')
            return redirect(url_for('home'))
         else:
              print(f.errors)
              print('cant validate')    

    return render_template('volregister.html',title="Register",f=f,x=x,y=y)

@app.route("/login",methods=['GET','POST'])
def login():
    f=LoginForm()
    x,y=fun()
    if f.validate_on_submit():
        u=FoodGetters.query.filter_by(email=f.email.data).first()
        if  u and bcrypt.check_password_hash(u.password,f.password.data):
            login_user(u,remember=False)
            flash('Hey!Logged in succesfully!','success')
            if request.args.get('next'):
                next=request.args.get('next')
                print(next)
                return redirect(url_for(next[1:]))
            else:
                  t=FoodGetters.query.filter_by(volunteer="True")
                  for i in t:
                      print(i)
                  return redirect(url_for('home'))
        else:
            flash('Check your credentials; if not registered,register and login!','danger')
    return render_template("login.html",f=f,x=x,y=y)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged Out!Come back soon!','warning')
    return redirect(url_for('home'))

@app.route('/about',methods=['GET'])
def about():
    x,y=fun()
    return render_template('about.html',x=x,y=y)

def send_mail(donor,user):
    print("fun",donor,user)
    msg=Message('Someone is interested to take your food!Check who it is',sender='Sugathanoreply@gmail.com',recipients=[donor.email])
    msg.body=f'''One of the user is interested and likely to contact you.Here are his/her details
     {user.name}
     {user.email}
     {user.address}
     Your food is being utilized in the right way!
     ! '''
    print(msg)
    mail.send(msg)


@app.route('/updateit/<int:foodid>',methods=['GET','POST'])
@login_required
def updateit(foodid):
    print("imp*************************************************************")
    print("c",current_user)
    print('1st',current_user.takenfoodid)
    p=current_user.takenfoodid
    print(p)
    if p is None:
        p=str(foodid)
        print(p)
    else:
       p=p+','+str(foodid)
       print(p)
    current_user.takenfoodid=p
    db.session.commit()
    print("*",current_user.takenfoodid)
    donor=FoodDonors.query.get(foodid)
    print("donor",donor)
    donor.taken="TrueP"
    db.session.commit()
    print("donor taken",donor)
    send_mail(donor,current_user)
    return redirect(url_for('allmytakenfood'))


@app.route('/allmytakenfood',methods=['GET'])
@login_required
def allmytakenfood():
    x,y=fun()
    l1=[]
    print("allmytaken-------------------------------------------------------------******imp")
    req=current_user.takenfoodid
    if req is not None:
        print("not None",len(current_user.takenfoodid))
    print('req',req)
    if req is None:
         return render_template("allmytakenfood.html",l=[],x=x,y=y)
    if len(req)==1:
         q=FoodDonors.query.get(int(req))
         print("donor",q)
         if q.taken=='TrueP':
                print("one")
                print(q.taken,q)
                l1.append(q)
    else:
      print(req)
      reql=list(req.split(","))
      #reql=reql[1:]
      print(reql)
      l=list(map(int,reql))
      print(l)
      for i in l:
             q=FoodDonors.query.get(i)
             print("donors:",q)
             if q.taken=='TrueP':
                print(q.taken,q)
                l1.append(q)
      s=set(l1)
      l1=list(s)
    print("only true list",l1)
    return render_template("allmytakenfood.html",l=l1,x=x,y=y)

def send_cancel_mail(donor,user):
    print("fun",donor,user)
    msg=Message('Someone dropped from taking your food!Check who it is',sender='Sugathanoreply@gmail.com',recipients=[donor.email])
    msg.body=f'''One of the user has dropped from taking your food!.Here are his/her details
     {user.name}
     {user.email}
     {user.address}
     Your food is being utilized in the right way!
     ! '''
    print(msg)
    mail.send(msg)

def send_notify_mail(donor,user):
    #print("fun",donor,user)
    msg=Message('Notifying you as food is available now',sender='Sugathanoreply@gmail.com',recipients=[user.email])
    msg.body=f'''The food details posted by 
     {donor.name} is now available.As someone has dropped from taking it.Here are the further details
     {donor.email}
     {donor.address}
     Here is the link to check the donors!
     {url_for('donorsready',_external=True)}
     ! '''
    print(msg)
    mail.send(msg)

@app.route('/cancelling/<int:id>',methods=['GET','POST'])
@login_required
def cancelling(id):
    t=FoodDonors.query.get(id)
    t.taken="False"
    db.session.commit()
    print("t in cancelling",t)
    send_cancel_mail(t,current_user)
    m=notifyme.query.filter_by(foodid=id).first()
    print(m.id,m.foodid,m.userid)
    print(m)
    l=list(m.userid.split(","))
    print(l)
    l=list(map(int,l))
    for i in l:
        e=FoodGetters.query.get(i)
        send_notify_mail(t,e)
    flash('You have cancelled your interest for food!','warning')
    return redirect(url_for('allmytakenfood'))

def send_successful_mail_g(user,donor):
    print("fun2s",donor,user)
    msg=Message('Success!',sender='Sugathanoreply@gmail.com',recipients=[donor.email])
    msg.body=f'''You have taken this donor's food {donor.contactno}!!
     {donor.email}
     {donor.address}
     ! '''
    print(msg)
    mail.send(msg)

def send_successful_mail_d(donor,user):
    print("fun1s",donor,user)
    msg=Message('This user has taken your food!',sender='Sugathanoreply@gmail.com',recipients=[donor.email])
    msg.body=f'''This user has taken your food and did not let it go waste!.Here are his/her details
     {user.name}
     {user.email}
     {user.address}
     Your food is being utilized in the right way!
     ! '''
    print(msg)
    mail.send(msg)

@app.route('/completed/<int:id>',methods=['GET','POST'])
@login_required
def completed(id):
    t=FoodDonors.query.get(id)
    t.taken="TrueC"
    db.session.commit()
    send_successful_mail_d(t,current_user)
    send_successful_mail_g(current_user,t)
    if current_user.volunteer=='True':
        w=current_user.count
        w=w+1
        current_user.count=w
        db.session.commit()
    print('completed route----------------------------------------------------------------------------')
    print(current_user,t)
    flash('You have succesfully taken the food!','success')
    return redirect(url_for('home'))

@app.route('/updatedetails',methods=['GET','POST'])
@login_required
def updatedetails():
   if current_user.volunteer=='True':
       f=VolUpdateForm()
       x,y=fun()
       if f.validate_on_submit():
           current_user.name=f.name.data
           current_user.email=f.email.data
           current_user.year=f.year.data
           current_user.address=f.address.data
           current_user.city=f.city.data
           current_user.mobileno=f.mobileno.data
           if f.pic.data is not None:
               picname=save_pic(f.pic.data,f.name.data)
               current_user.pic=picname
           db.session.commit()
           flash('Details Updated Succesfully','success')
           return redirect(url_for('home'))
       elif request.method=='GET':
           f.name.data=current_user.name
           f.email.data=current_user.email
           #f.year.data=current_user.year
           f.address.data=current_user.address
           f.city.data=current_user.city
           f.mobileno.data=current_user.mobileno
       return render_template('volupdate.html',f=f,x=x,y=y,title="Update")
   else:
            f=UpdateRegisterForm()
            x,y=fun()
            if f.validate_on_submit():
                    current_user.name=f.name.data
                    current_user.email=f.email.data
                    #current_user.year=f.year.data
                    current_user.address=f.address.data
                    current_user.city=f.city.data
                    current_user.mobileno=f.mobileno.data
                    if f.pic.data is not None:
                         picname=save_pic(f.pic.data,f.name.data)
                         current_user.pic=picname
                    db.session.commit()
                    flash('Details Updated Succesfully','success')
                    return redirect(url_for('home'))
            elif request.method=='GET':
                    f.name.data=current_user.name
                    f.email.data=current_user.email
                    #f.year.data=current_user.year
                    f.address.data=current_user.address
                    f.city.data=current_user.city
                    f.mobileno.data=current_user.mobileno
            return render_template('update.html',x=x,y=y,f=f,title="Update")

def send_reset_link(user):
    print(user)
    token=user.set_idtoken()
    print(token)
    msg=Message('Password reset link',sender='Sugathanoreply@gmail.com',recipients=[user.email])
    msg.body=f'''The link to reset your password is below
    {url_for('resetpass',token=token,_external=True)}
     If it is not you never mind and ignore! '''
    print(msg)
    mail.send(msg)

   
@app.route('/resetlink',methods=['GET','POST'])
def resetlink():
    x,y=fun()
    if current_user.is_authenticated:
        flash('You are already logged in!Logout to change your password','danger')
        return redirect(url_for('home'))
    f=ResetLinkForm()
    if f.validate_on_submit():
        user=FoodGetters.query.filter_by(email=f.email.data).first()
        print(user)
        send_reset_link(user)
        flash('A password reset link has been sentto your mail!','success')
        return redirect(url_for('login'))
    return render_template('resetlink.html',f=f,title="Request Password Reset",x=x,y=y)

@app.route('/resetpass/<token>',methods=['GET','POST'])
def resetpass(token):
    x,y=fun()
    if current_user.is_authenticated:
        flash('You are already logged in!You need to logout to reset your password!','danger')
        return redirect(url_for('home'))
    user=FoodGetters.verify_token(token)
    if user is None:
        flash('An invalid token!','danger')
        return redirect(url_for('resetlink'))
    f=ResetPassForm()
    if f.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(f.password.data)
        user.password=hashed_password
        db.session.commit()
        flash('You have succesfully changed your password.Now you can login with your new password','success')
        return redirect(url_for('login'))
    return render_template('resetpass.html',f=f,ttile="Password Reset",x=x,y=y)
@app.route('/volunteers',methods=['GET','POST'])
def volunteers():
    print("***************************************************************************************")
    x,y=fun()
    p=FoodGetters.query.filter_by(volunteer='True').order_by(FoodGetters.count.desc())
    max1=0
    li=[]
    for i in p:
        if i.count>max1:
            max1=i.count
    print(max1)
    q=FoodGetters.query.filter_by(volunteer='True',count=max1).order_by(FoodGetters.date.asc())
    for i in q:
        li.append(i)
    print(li)
    #print(li[0].pic)
    if len(li)==0:
         return render_template('topvol.html',x=x,y=y,len=0)
    elif len(li)==1:
       return render_template('topvol.html',x=x,y=y,j=li[0],pic=li[0].pic,len=1)
    else:
        return render_template('topvol.html',x=x,y=y,j=li[0],pic=li[0].pic,j1=li[1],pic1=li[1].pic,len=2)

@app.route('/notify/<int:foodid>',methods=['GET','POST'])
def notify(foodid):
    print('notify..............................................')
    q=notifyme.query.filter_by(foodid=foodid).first()
    if q is None:
        print('first')
        w=current_user.id
        x=str(w)
        print(x)
        p=notifyme(foodid=foodid,userid=x)
        db.session.add(p)
        db.session.commit()
        es=notifyme.query.filter_by(foodid=foodid).first()
        print(notifyme.query.filter_by(foodid=foodid).first())
        print(es.userid)
    else:
        print('more')
        print(q.userid)
        s=q.userid
        c=current_user.id
        m=s+","+str(c)
        print(m)
        q.userid=m
        db.session.commit()
    a=notifyme.query.filter_by(foodid=foodid).first()
    t=str(current_user.id)
    flash('You will be notified via mail once it is cancelled by the one who was interested in it!','success')
    return redirect(url_for('donorsready'))