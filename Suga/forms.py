from flask import Flask
from Suga import db
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,DateField,RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField,FileAllowed
from Suga.models import FoodGetters

class RegisterForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=4)])
    year=DateField('Establishment year',format='%Y-%m-%d')
    city=StringField('City',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=4,max=8)])
    Confirm=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    address=StringField('Address',validators=[DataRequired()])
    mobileno=StringField('MobileNumber',validators=[DataRequired()])
    pic=FileField('Upload Certificate image',validators=[DataRequired(),FileAllowed(['png','jpg'])])
    submit=SubmitField('Register')
    def validate_mobilenono(self,con):
        l=['0','1','2','3','4','5','6','7','8','9']
        c=0
        for i in con.data:
            if i in l:
                c=c+1
        if(c!=10):
            raise ValidationError('Please enter a valid contact number!')

    def validate_password(self,password):
        l=[]
        l1=['0','1','2','3','4','5','6','7','8','9']
        l2=[]
        cs=0
        cn=0
        cc=0
        for i in range(33,48):
            l.append(chr(i))
        for i in range(58,65):
            l.append(chr(i))
        for i in range(91,97):
            l.append(chr(i))
        for i in range(65,91):
            l2.append(chr(i))
        for i in password.data:
            if i in l:
                cs=cs+1
                break
        for i in password.data:
            if i in l1:
                cn=cn+1
                break
        for i in password.data:
            if i in l2:
                cc=cc+1
                break
        if cc==0 or cn==0 or cs==0:
            print(cc,cs,cn)
            print(l,l1,l2)
            raise ValidationError('Password must include atleast a special symbol,digit,Capital letter!')
    def validate_email(self,email):
        p=FoodGetters.query.filter_by(email=email.data).first()
        if p:
            raise ValidationError('This mail id is already taken,Please enter a new one!')
    def validate_city(self,c):
        c=c.data
        co=0
        l=[]
        for i in range(65,92):
            l.append(chr(i))
        for i in c:
            if i in l:
                co=co+1
        if co!=len(c):
            raise ValidationError('Please enter your city in all capital letters Ex:KURNOOL!')


class VolRegisterForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=4,max=8)])
    year=DateField('Date Of Birth',format='%Y-%m-%d')
    city=StringField('City',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=4,max=8)])
    Confirm=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    address=StringField('Address',validators=[DataRequired()])
    mobileno=StringField('MobileNumber',validators=[DataRequired()])
    pic=FileField('Upload Your image',validators=[DataRequired(),FileAllowed(['png','jpg'])])
    submit=SubmitField('Register')
    def validate_mobilenono(self,con):
        l=['0','1','2','3','4','5','6','7','8','9']
        c=0
        for i in con.data:
            if i in l:
                c=c+1
        if(c!=10):
            raise ValidationError('Please enter a valid contact number!')

    def validate_password(self,password):
        l=[]
        l1=['0','1','2','3','4','5','6','7','8','9']
        l2=[]
        cs=0
        cn=0
        cc=0
        for i in range(33,48):
            l.append(chr(i))
        for i in range(58,65):
            l.append(chr(i))
        for i in range(91,97):
            l.append(chr(i))
        for i in range(65,91):
            l2.append(chr(i))
        for i in password.data:
            if i in l:
                cs=cs+1
                break
        for i in password.data:
            if i in l1:
                cn=cn+1
                break
        for i in password.data:
            if i in l2:
                cc=cc+1
                break
        if cc==0 or cn==0 or cs==0:
            print(cc,cs,cn)
            print(l,l1,l2)
            raise ValidationError('Password must include atleast a special symbol,digit,Capital letter!')
    def validate_email(self,email):
        p=FoodGetters.query.filter_by(email=email.data).first()
        if p:
            raise ValidationError('This mail id is already taken,Please enter a new one!')
    def validate_city(self,c):
        c=c.data
        co=0
        l=[]
        for i in range(65,92):
            l.append(chr(i))
        for i in c:
            if i in l:
                co=co+1
        if co!=len(c):
             raise ValidationError('Please enter your city in all capital letters Ex:KURNOOL!')


class FoodForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    contactno=StringField('ContactNumber',validators=[DataRequired(),Length(min=10,max=10)])
    city=StringField('City',validators=[DataRequired()])
    address=StringField('Address',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    tfood=RadioField('Food Type', choices=[('Veg','Veg'), ('Non-veg','Non-Veg')],default=1,validators=[DataRequired()])
    submit=SubmitField('Done!')

    def validate_contactno(self,con):
        l=['0','1','2','3','4','5','6','7','8','9']
        c=0
        for i in con.data:
            if i in l:
                c=c+1
        if(c!=10):
            raise ValidationError('Please enter a valid contact number!')
    def validate_city(self,c):
        c=c.data
        co=0
        l=[]
        for i in range(65,92):
            l.append(chr(i))
        for i in c:
            if i in l:
                co=co+1
        if co!=len(c):
            raise ValidationError('Please enter your city in all capital letters Ex:KURNOOL!')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')

    def validate_email(self,email):
        u=FoodGetters.query.filter_by(email=email.data).first()
        if u is None:
            raise ValidationError("No!You are not registered!Please register and then Login in")
        
class CityForm(FlaskForm):
    city=StringField()
    submit=SubmitField()
    def validate_city(self,c):
        c=c.data
        co=0
        l=[]
        for i in range(65,92):
            l.append(chr(i))
        for i in c:
            if i in l:
                co=co+1
        if co!=len(c):
            raise ValidationError('Please enter city in all capital letters Ex:KURNOOL!')

class VolUpdateForm(FlaskForm):
    name=StringField('Name',validators=[Length(min=4,max=8)])
    year=DateField('Date Of Birth',format='%Y-%m-%d',validators=[DataRequired()])
    city=StringField('City')
    email=StringField('Email',validators=[Email()])
    address=StringField('Address')
    mobileno=StringField('MobileNumber')
    pic=FileField('Upload Your image',validators=[FileAllowed(['png','jpg'])])
    submit=SubmitField('Update')
    def validate_mobilenono(self,con):
        l=['0','1','2','3','4','5','6','7','8','9']
        c=0
        for i in con.data:
            if i in l:
                c=c+1
        if(c!=10):
            raise ValidationError('Please enter a valid contact number!')

    def validate_email(self,email):
        if email.data!=current_user.email:
           print("yes",email,current_user.email)
           p=FoodGetters.query.filter_by(email=email.data).first()
           if p:
              raise ValidationError('This mail id is already taken,Please enter a new one!')
    def validate_city(self,c):
        c=c.data
        co=0
        l=[]
        for i in range(65,92):
            l.append(chr(i))
        for i in c:
            if i in l:
                co=co+1
        if co!=len(c):
             raise ValidationError('Please enter your city in all capital letters Ex:KURNOOL!')

class UpdateRegisterForm(FlaskForm):
    name=StringField('Name',validators=[Length(min=4)])
    year=DateField('Establishment year',format='%Y-%m-%d',validators=[DataRequired()])
    city=StringField('City')
    email=StringField('Email',validators=[Email()])
    address=StringField('Address')
    mobileno=StringField('MobileNumber')
    pic=FileField('Upload Certificate image',validators=[FileAllowed(['png','jpg'])])
    submit=SubmitField('Update')
    def validate_mobilenono(self,con):
        l=['0','1','2','3','4','5','6','7','8','9']
        c=0
        for i in con.data:
            if i in l:
                c=c+1
        if(c!=10):
            raise ValidationError('Please enter a valid contact number!')

    def validate_email(self,email):
        if email.data!=current_user.email:
           print("yes",email,current_user.email)
           p=FoodGetters.query.filter_by(email=email.data).first()
           if p:
              raise ValidationError('This mail id is already taken,Please enter a new one!')
    def validate_city(self,c):
        c=c.data
        co=0
        l=[]
        for i in range(65,92):
            l.append(chr(i))
        for i in c:
            if i in l:
                co=co+1
        if co!=len(c):
            raise ValidationError('Please enter your city in all capital letters Ex:KURNOOL!')

class ResetLinkForm(FlaskForm):
   email=StringField('Email',validators=[DataRequired(),Email()])
   submit=SubmitField('OK')

   def validate_email(self,email):
       m=FoodGetters.query.filter_by(email=email.data).first()
       if m is None:
           raise ValidationError('No such email is found in registered user!Try the registered one!')

class ResetPassForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    Confirm=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('OK')
    def validate_password(self,password):
        l=[]
        l1=['0','1','2','3','4','5','6','7','8','9']
        l2=[]
        cs=0
        cn=0
        cc=0
        for i in range(33,48):
            l.append(chr(i))
        for i in range(58,65):
            l.append(chr(i))
        for i in range(91,97):
            l.append(chr(i))
        for i in range(65,91):
            l2.append(chr(i))
        for i in password.data:
            if i in l:
                cs=cs+1
                break
        for i in password.data:
            if i in l1:
                cn=cn+1
                break
        for i in password.data:
            if i in l2:
                cc=cc+1
                break
        if cc==0 or cn==0 or cs==0:
            print(cc,cs,cn)
            print(l,l1,l2)
            raise ValidationError('Password must include atleast a special symbol,digit,Capital letter!')
    