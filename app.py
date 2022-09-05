from ast import Str
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, IntegerField, HiddenField, FieldList, FormField 
from wtforms.validators import InputRequired, Email, Length, ValidationError
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, ForeignKey, and_, or_, update
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.fields.html5 import DateField

from time import sleep

import taxcalc
import dwollafull
import dwollav2

from venmo_api import Client
from sendfunds import *
from datetime import datetime




app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///purepayroll.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Dwolla
client = dwollav2.Client(
  key = 'A8PrXAX1kFM0hHktY3l8FYWPX8KZQMiB7zBgiyXeC09AO082EM',
  secret = 'E1cyNdJsjKm0IIv7MIwwAQchpTqtP7dP3YoTPY6bKichigm7EG',
  environment = 'sandbox', # defaults to 'production'
)
application_token = client.Auth.client()



# Bootstrap(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


##### CLI Commands to make easier to re-load database ####
#  INSTRUCTIONS: in the virtual environment, on the command line type 'flask initdb' to delete, clear and create new database, then on command line type 'flask dbseed' to seed the new database with the seed data.
@app.cli.command("initdb")
def reset_db():
    """Drops and Creates fresh database """
    db.drop_all()
    db.create_all()
    
    print("Initialized default DB")
    
### Populates db with dummy data ####
@app.cli.command("dbseed")
def dbseed_data():
    """Popluates database with data"""
    db.drop_all()
    db.create_all()
    
    db.session.add(
        User(
            fname="Tom",
            lname="Sawyer",
            email="tom1@gmail.com",
            phone="555 121-2121",
            password="sha256$HK4UxnqJ$2a39765e0400805af2128613791b8ca414c9f4a3c4fbeccaf6ba5deb98703efc",
            
        )
    )
    
    db.session.add(
        Company(
            userid = "1",
            cname = "Apple Inc.",
            fein = "123456789",
            cfirstname = "Steve",
            clastname = "Jobs",
            cemail = "TimCook@apple.com",
            cipaddress = "127.0.0.5",
            ctype = "Business",
            cdob = "01/01/1950",
            cssn = "123-45-6789",
            
            addr1 = "100 Infinity Drive",
            addr2 = "Suite #3456",
            city = "Cupertino",
            state = "CA",
            zcode = "94101",
            
            cbustype = "soleProprietorship",
            cbusclass = "9ed3f670-7d6f-11e3-b1ce-5404a6144203",
            phone = "650-555-1212",
            url = "www.apple.com",
            contactname = "Tim Cook",
            cphone = "650-555-1212",
            
            ccfirstname = "Paul",
            cclastname = "Wozniak",
            cctitle = "Controller",
            ccdob = "03/03/1953",
            ccssn = "555-12-1234",
            ccaddr1 = "123 Main Street",
            ccaddr2 = "Apt 100",
            ccaddr3 = "",
            cccity = "Cupertino",
            ccstate = "CA",
            cczip = "94201",
            cccountry = "USA",
            ccverified = "verified",
            
            bfirstname = "Jane",
            blastname = "Doe",
            bssn = "777-33-9876",           
            bdob = "05/05/1971",
            baddr1 = "333 Hilcoroft",
            baddr2 = "Apt 333",
            baddr3 = "",
            bcity = "Sunnyvale",
            bstate = "CA",
            bzip = "94025",
            bcountry = "USA",
            bverified = 'verified',
            
            
            cbankacct = "555444333",
            cbankrout = "123456789",
            cdwollaid = "xxxxxxxxxxxxxxx",
            cdwollasid = "yyyyyyyyyyyyyyyy",
            cdwacctype = "Checking",
            cbankacctnm = "Apple Bank Account"
            
        )
    )
    
    db.session.add(
        Employee(
        cid = "1",
        userid = "1",
        hiringdate = "01/01/2000",
        fname = "John",
        lname = "Smith",
        addr1 = "1234 Hilcorft Street",
        addr2 = "Apt 23",
        city = "Santa Clara",
        state = "CA",
        zcode = "94025",
        ssn = "555-12-6789",
        dob = "05/27/1999",
        email = "JohnSmith@apple.com",
        phone = "650-333-2211",
        paymethod = "ACH",
        bankacct = "123456789",
        bankrouting = "999111333",
        bankacctnm = "John Smith Bank Account",
        bankacctype = "checking",
        eedwollaid = "thisIsDwollaID",
        eedwollafid = "thisIsDwollaFiD",
        filing_status = "MFS",
        w4_step2c_jobs = "y",
        w4_step3 = "25",
        w4_step4a = "2",
        w4_step4b = "55",
        w4_step4c = "100",
        )
    )
    
    db.session.add(
        PayTable(
            userid="1",
            cid="1",
            eid="1",
            pfreq="26",
            prate="16",
            ptype="Hourly"
        )
    )
    
    db.session.add(
        Paycheck(
            userid = "1",
            cid = "1",
            eid = "1",
            grosspay = 1000,
            fedtax = 54.42,
            fica = 62,
            medicare = 14.50,
            state = 0,
            cfica = 62,
            cmedicare = 14.50,
            netpay=869.08,
            paid = 0,
        )
    )
    
    ### commit to db ###
    db.session.commit()
    

##################### Database Schema ###############################
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(80))

class Company(UserMixin, db.Model):
    __tablename__ = 'company'
    userid = db.Column(db.Integer, ForeignKey('user.id'))
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cname = db.Column(db.String(80))
    fein = db.Column(db.Integer)
    
    cfirstname = db.Column(db.String(80))
    clastname = db.Column(db.String(80))
    cemail = db.Column(db.String(100))
    cipaddress = db.Column(db.String(100))
    ctype = db.Column(db.String(80))
    cdob = db.Column(db.String(40))
    cssn = db.Column(db.String(20))
    addr1 = db.Column(db.String(150))
    addr2 = db.Column(db.String(150))
    city = db.Column(db.String(100))
    state = db.Column(db.String(20))
    zcode = db.Column(db.Integer)
    # following is Soleproprietorship or LLC
    cbustype = db.Column(db.String(100))
    cbusclass = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    url = db.Column(db.String(150))
    contactname = db.Column(db.String(150))
    cphone = db.Column(db.String(20))

    # Controller fields cc=Company Controller
    ccfirstname = db.Column(db.String(100))
    cclastname = db.Column(db.String(100))
    cctitle = db.Column(db.String(100))
    ccdob = db.Column(db.String(100))
    ccssn = db.Column(db.String(20))
    ccaddr1 = db.Column(db.String(100))
    ccaddr2 = db.Column(db.String(100))
    ccaddr3 = db.Column(db.String(100))
    cccity = db.Column(db.String(100))
    ccstate = db.Column(db.String(100))
    cczip = db.Column(db.String(100))
    cccountry = db.Column(db.String(100))
    ccverified = db.Column(db.String(10))
    
    # Beneficial owner information b=Beneficial Owner
    bfirstname = db.Column(db.String(100))
    blastname = db.Column(db.String(100))
    bssn = db.Column(db.String(20))
    bdob = db.Column(db.String(100))
    baddr1 = db.Column(db.String(100))
    baddr2 = db.Column(db.String(100))
    baddr3 = db.Column(db.String(100))
    bcity = db.Column(db.String(100))
    bstate = db.Column(db.String(100))
    bzip = db.Column(db.String(100))
    bcountry = db.Column(db.String(100))
    bverified = db.Column(db.String(10))
    
     
    #Adding fields for dwollla 
    cbankacct = db.Column(db.Integer)
    cbankrout = db.Column(db.Integer)
    cdwollaid = db.Column(db.String(100))
    cdwollasid = db.Column(db.String(100))
    cdwacctype = db.Column(db.String(100))
    cbankacctnm = db.Column(db.String(100))
    
    

class Employee(UserMixin, db.Model):
    '''
    Keeping it simple for now
    May want to add: SSN, DOB, email, phone, address, prate, pfreq, deductions
    '''
    __tablename__ = 'employee'
    eid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date=db.Column(db.DateTime, default=datetime.now)
    cid = db.Column(db.Integer, ForeignKey('company.cid'))
    userid = db.Column(db.Integer, ForeignKey('user.id'))
    hiringdate = db.Column(db.String(15))
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    addr1 = db.Column(db.String(150))
    addr2 = db.Column(db.String(150))
    city = db.Column(db.String(20))
    state = db.Column(db.String(10))
    zcode = db.Column(db.Integer)
    ssn = db.Column(db.String(11))
    dob = db.Column(db.String(10))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(15))
    paymethod = db.Column(db.String(20))
    bankacct = db.Column(db.String(20))
    bankrouting = db.Column(db.String(20))
    bankacctnm = db.Column(db.String(20))
    bankacctype = db.Column(db.String(20))
    eedwollaid = db.Column(db.String(100))
    eedwollafid = db.Column(db.String(100))
    filing_status = db.Column(db.String(3))
    w4_step2c_jobs = db.Column(db.String(2))
    w4_step3 = db.Column(db.Integer)
    w4_step4a = db.Column(db.Integer)
    w4_step4b = db.Column(db.Integer)
    w4_step4c = db.Column(db.Integer)

class Paycheck(db.Model):
    __tablename__ = 'paycheck'
    paycheckid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, ForeignKey('user.id'))
    cid = db.Column(db.Integer, ForeignKey('company.cid'))
    eid = db.Column(db.Integer, ForeignKey('employee.eid'))
    created_date=db.Column(db.DateTime, default=datetime.now)
    paydate = db.Column(db.DateTime, default=datetime.utcnow)
    grosspay = db.Column(db.Numeric)
    ytdgross = db.Column(db.Numeric)
    fedtax = db.Column(db.Numeric)
    fica = db.Column(db.Numeric)
    medicare = db.Column(db.Numeric)
    state = db.Column(db.Numeric)
    cfica = db.Column(db.Numeric)
    cmedicare = db.Column(db.Numeric)
    netpay = db.Column(db.Numeric)
    paid = db.Column(db.Boolean, default=False)
    
class PayTable(db.Model):
    __tablename__ = 'paytable'
    payid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, ForeignKey('user.id'))
    cid = db.Column(db.Integer, ForeignKey('company.cid'))
    eid = db.Column(db.Integer, ForeignKey('employee.eid'))
    created_date=db.Column(db.DateTime, default=datetime.now)
    ptype = db.Column(db.String(15))
    prate = db.Column(db.Numeric)
    pfreq = db.Column(db.Numeric)
    
    

      
##### F l a s k    F o r m s ###############
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=4, max=50)])
    #username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)]) 
    remember = BooleanField('remember me')

class UserForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=4, max=50)])
    fname = StringField('First name')
    lname = StringField('Last name')
    phone = StringField('phone')
    #username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
  
class EmployerForm(FlaskForm):
    cfirstname = StringField('Owner First Name', validators=[InputRequired(), Length(min=4, max=50)])
    clastname = StringField('Owner Last Name', validators=[InputRequired(), Length(min=4, max=50)])
    cemail = StringField('Email Address', validators=[InputRequired()])
    cipaddress = StringField('IP Address (ex: 148.156.7.8)', validators=[InputRequired()])
    ctype = SelectField('Company Type', choices=['Business', 'other'])
    cdob = StringField('Owner DOB', validators=[InputRequired()])
    cssn = StringField('Owner SSN', validators=[InputRequired(), Length(min=4, max=9)])
    addr1 = StringField('Address 1', validators=[InputRequired()])
    addr2 = StringField('Address 2')
    city = StringField('City', validators=[InputRequired()])
    STATE_ABBREV = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO','CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    state = SelectField('State', choices = STATE_ABBREV, validators=[InputRequired(), Length(min=1, max=50)]) 
    zcode = StringField('Zip code', validators=[InputRequired(), Length(min=5, max=12)])
    cbusclass = StringField('Business Classification', validators=[InputRequired()])
    cbustype = SelectField('Business Type', choices=[('SoleProprietorship', 'SoleProprietorship'), ('LLC','LLC')])
    cname = StringField('Company Name', validators=[InputRequired()])
    fein = IntegerField('FEIN 9 digit', validators=[InputRequired(), Length(min=9, max=9)])
    cbankrout = StringField('Bank routing (9 digit) #', validators=[InputRequired(), Length(min=9, max=9)])
    cbankacct = StringField('Bank Account #', validators=[InputRequired(), Length(min=1, max=12)])
    cdwacctype = StringField('Account Type', validators=[InputRequired()])
    cbankacctnm = StringField('Name on Bank Account', validators=[InputRequired()])
    phone = StringField('Phone Number', validators=[InputRequired()])
    url = StringField('Company URL')
    contactname = StringField('Contact Name')
    cphone = StringField("Contact Name's Phone")


class VenmoForm(FlaskForm):
    venusername = StringField('Venmo Username', validators=[InputRequired(), Length(min=4, max=50)])
    venpassword = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    
class EmployeeForm(FlaskForm):
    eid = HiddenField(IntegerField())
    cid = HiddenField(IntegerField())
    hiringdate = DateField('Hiring date', format='%m/%d/%Y',validators=[InputRequired()])
    fname = StringField('First name', validators=[InputRequired(), Length(min=1, max=50)])
    lname = StringField('Last name', validators=[InputRequired(), Length(min=1, max=50)])
    addr1 = StringField('Address')
    addr2 = StringField('Suite/Apt')
    city = StringField('City')
    STATE_ABBREV = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO','CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    state = SelectField('State', choices = STATE_ABBREV, validators=[InputRequired(), Length(min=1, max=50)]) 
    zcode = StringField('Zip code', validators=[InputRequired(), Length(min=5, max=12)])
    ssn = StringField('SSN')
    dob = StringField('DOB')
    email = StringField('email', validators=[InputRequired()])
    phone = StringField('phone')
    paymethod = SelectField('Payment Method', choices=[('ACH', 'Bank Transfer - ACH'), ('other', 'Other'),])
    bankacct = StringField('Bank Account#', validators=[InputRequired(), Length(min=9, max=9)])
    bankacctnm = StringField('Name on bank account')
    bankacctype = SelectField('Account Type', choices=['Checking', 'Savings'], validators=[InputRequired()])
    bankrouting = StringField('Bank routing #', validators=[InputRequired(), Length(min=9, max=9)])
    eedwollaid = StringField('EE Dwolla ID')
    eedwollafid = StringField('EE Dwolla Funding ID')

    filing_status = SelectField('Filing Status',  choices=[('MFS', 'Single or Married Filing Separately'), ('MFJ', 'Married Filing Jointly or Qualified widow(er)'), ('HH','Head of household')])
    w4_step2c_jobs = BooleanField('Jobs', default=True)
    w4_step3 = IntegerField('')
    w4_step4a = IntegerField('(a) Other income (not from jobs)')
    w4_step4b = IntegerField('(b) Deductions')
    w4_step4c = IntegerField('(c) Extra witholding')
    ptype = SelectField('Pay Type', choices=[('Hourly','Hourly'), ('Monthly', 'Monthly')])
    prate = IntegerField('Rate')
    pfreq = SelectField('Pay Frequency', choices=[('2','Seminnually'), ('4', 'Quarterly'), ('12', 'Monthly'), ('24', 'Semimonthly'), ('26', 'Biweekly'), ('52', 'Weekly'), ('260', 'Daily')])
    
class PayForm(FlaskForm):
    userid = HiddenField(IntegerField())
    cid = HiddenField(IntegerField())
    eid = HiddenField(IntegerField())
    grosspay = IntegerField('Gross Pay')
    submit = SubmitField("Submit Gross Pay")   
    

class DwollaCustForm(FlaskForm):
    dfname = StringField('First Name')
    dlname = StringField('Last Name')
    demail = StringField('email')
    dbnkacct = StringField('Bank Account Number')
    dbnkrout = StringField('Bank Routing Number')
    dacctype = StringField('Account type checking or savings')
    dacctnm = StringField('Name on Account')    
    
    
    # others to be added like all of W4 form here ####                  
    



############################### R O U T E S #############################################################
@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)


### L O G I N ###
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                companys = Company.query.filter_by(userid=user.id).all()
                message = "Logged in and going to Main.html"
                ###returns to MAIN.HTML #####
                return render_template('main.html', name=current_user.email, companys=companys, message=message)
            return '<h1>Invalid email or password</h1>'

    else:
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        else:
            user = current_user
            companys = Company.query.filter_by(userid=user.id).all()
            return render_template('main.html', name=user.email, companys=companys)


########### S I G N   U P #############
@app.route('/indexsignup', methods=['GET', 'POST'])
def indexsignup():
    form = UserForm()
    return render_template('indexsignup.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()
    
    #First perform a check whether the useremail already exits or not  
    if form.validate_on_submit():
        if request.method == "POST":
            new_email=request.form.get('email')
            try:
                user=User.query.filter_by(email=new_email).first()
                text = str(user.id)
                message="Welcome back"
                return render_template('userexists.html', name=new_email, form=LoginForm(), message=message)
            
            #then input into db entry if it does not exist
            except:
                hashed_password = generate_password_hash(form.password.data, method='sha256')
                new_user = User(email=form.email.data, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=form.remember.data)
                message="Welcome to payroll, it is quick and easy. First you create a Company, then you Add Employees, and then your Run Payroll. So lets get started, Click on Company to add a new company..."
                
                #sending user to main.html page with user email credentials    
                return render_template('main.html', name=new_email, message=message)
    else:
        return form.errors



################## A D D I N G   EMPLOYEES  ########################
@app.route('/addemp', methods=['GET', 'POST'])
@login_required
def addemp():    
    form = EmployeeForm()
    cname = request.args.get('company')
    company = Company.query.filter(and_(Company.cname==cname, Company.userid==current_user.id)).first()
    if company:
        return render_template('employeeform.html', company=company, form=form)
    else:
        return "Invalid URL"

@app.route('/addemployee', methods=['GET', 'POST'])
@login_required
def addemployee():
    '''
    Redirect to this route after user has filled a form to add a new employee.
    '''
    if request.method == "POST":
        hiringdate = request.form.get('hiringdate')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        addr1 = request.form.get('addr1')
        addr2 = request.form.get('addr2')
        city = request.form.get('city')
        state = request.form.get('state')
        zcode = request.form.get('zcode')
        ssn = request.form.get('ssn')
        dob = request.form.get('dob')
        email = request.form.get('email')
        phone = request.form.get('phone')
        paymethod = request.form.get('paymethod')
        bankacct = request.form.get('bankacct')
        bankrouting = request.form.get('bankrouting')
        bankacctnm = request.form.get('bankacctnm')
        bankacctype = request.form.get('bankacctype')
        eedwollaid = request.form.get('eedwollaid')
        eedwollafid = request.form.get('eedwollafid')

        filing_status = request.form.get('filing_status')
        w4_step2c_jobs = request.form.get('w4_step2c_jobs')
        w4_step3 = request.form.get('w4_step3')
        w4_step4a = request.form.get('w4_step4a')
        w4_step4b = request.form.get('w4_step4b')
        w4_step4c = request.form.get('w4_step4c')
        cid = request.form.get('cid')
        userid = current_user.id
        existName = Employee.query.filter(and_(Employee.fname==fname, Employee.cid==cid)).first()
        ptype = request.form.get('ptype')
        prate = request.form.get('prate')
        pfreq = request.form.get('pfreq')
        #checking to see if employee exists, if it does not exist then add employee
        if existName == None:
            (z,y) = dwollafull.createemplyee(fname,lname,email,bankrouting,bankacct,bankacctype, bankacctnm)
            #adding the new employee to database
            new_employee = Employee(hiringdate=hiringdate,fname=fname, lname= lname, addr1=addr1, addr2=addr2, city=city, state=state, zcode=zcode, ssn=ssn, dob=dob, email=email, phone=phone, paymethod= paymethod, bankacct=bankacct, bankrouting=bankrouting, bankacctype=bankacctype, bankacctnm=bankacctnm, eedwollaid=z, eedwollafid=y, filing_status=filing_status, w4_step2c_jobs=w4_step2c_jobs, w4_step3=w4_step3, w4_step4a=w4_step4a, w4_step4b=w4_step4b, w4_step4c=w4_step4c, cid=cid, userid=userid)
            db.session.add(new_employee)
            db.session.commit()
            
            # querying to get employee.eid
            employee=Employee.query.filter(Employee.fname==fname).first()
            eid=employee.eid
            
            #add employee info to paytable in db
            newpaytable = PayTable(userid=userid, cid=cid, eid=eid, ptype=ptype, prate=prate, pfreq=pfreq)
            db.session.add(newpaytable)
            db.session.commit()
            
            
            message = "Employee Added"
            employees = Employee.query.filter(Employee.cid==cid).all()
            company = Company.query.filter_by(cid=cid).first()
            return render_template('eemain.html', message=message, employees=employees, company=company, name=current_user)
        else:
            message = "Employee Already Exits"
            employees = Employee.query.filter(Employee.cid==cid).all()
            company = Company.query.filter_by(cid=cid).first()
            return render_template('eemain.html', message=message, employees=employees, company=company)

        return "Employee Added to Database"

### EDIT EMPLOYEE ###
@app.route('/editemp')
@login_required
def editEmployee():
    form=EmployeeForm()
    fname=request.args.get('fname')
    lname=request.args.get('lname')
    eid=request.args.get('eid')
    cid=request.args.get('cid')
    userid=current_user.id
    # now need to pull employee data from db to edit #
    #first query database to get employee details, making sure its the right employee 
    employee=Employee.query.filter(and_(Employee.fname==fname, Employee.lname==lname, Employee.eid==eid, Employee.cid==cid, Employee.userid==userid)).first()
    company=Company.query.filter(Company.cid==cid).first()
    paytable=PayTable.query.filter(PayTable.eid==eid).first()
    
    #then if employee exists, pull all the information on Employee and show as value in the eeedit.html page
    # if company:
    return render_template('eeedit.html', employee=employee, company=company, paytable=paytable, form=form)

### UPDATE Employee ### This is where the information on EE Update comes back
@app.route('/updateemp', methods=['GET', 'POST'])
@login_required
def updateEmployee():
    if request.method == "POST":
        neweid = request.form.get('eid')
        employee=Employee.query.filter(Employee.eid==neweid).first()
        employee.hiringdate=request.form.get('hiringdate')
        employee.fname=request.form.get('fname')
        employee.lname=request.form.get('lname')
        employee.addr1=request.form.get('addr1')
        employee.addr2=request.form.get('addr2')
        employee.city=request.form.get('city')
        employee.state=request.form.get('state')
        employee.zcode=request.form.get('zcode')
        employee.ssn=request.form.get('ssn')
        employee.dob=request.form.get('dob')
        employee.email=request.form.get('email')
        employee.phone=request.form.get('phone')
        employee.paymethod=request.form.get('paymethod')
        employee.bankacct = db.Column(db.String(20))
        employee.bankrouting = db.Column(db.String(20))
        employee.venmoacct = db.Column(db.String(30))
        employee.filing_status=request.form.get('filing_status')
        employee.w4_step2c_jobs=request.form.get('w4_step2c_jobs')
        employee.w4_step3=request.form.get('w4_step3')
        employee.w4_step4a=request.form.get('w4_step4a')
        employee.w4_step4cb=request.form.get('w4_step4b')
        employee.w4_step4c=request.form.get('w4_step4c')      
        db.session.commit()
        newcid=request.form.get('cid')
        company=Company.query.filter(Company.cid==newcid).first()
        employee=Employee.query.filter(Employee.eid==neweid).first()
        
        
        return render_template('eeprofileupdate.html', company=company, employee=employee)
    

@app.route('/addcompany')
@login_required
def addCompany():
    form = EmployerForm()
    name = current_user.email
    return render_template('addcompany.html', name=name, form=form)

#Edit Company information of an already created Company
@app.route('/editcomp', methods=['GET', 'POST'])
@login_required
def editCompany():
    name = current_user.email
    cname=request.args.get("company")
    company=Company.query.filter(and_(Company.cname==cname, Company.userid==current_user.id)).first()
    if company:
        message="Edit company on this page"
        user = current_user.email
        return render_template('editcompany.html', name=user, message=message, company=company)
    else:
        return "Invalid URL"


@app.route('/all_companies', methods=['GET', 'POST'])
@login_required
def all_companies():
    '''
    Simple query to get all companies for current user
    '''
    companies = Company.query.filter(Company.userid==current_user.id).all()
    companies = {i:company.cname for i, company in enumerate(companies)}
    return companies


# This route is to see all the employees of a particular company

@app.route('/viewee', methods=['GET', 'POST'])
@login_required
def viewEE():
    cname=request.args.get('company')
    # company=Company.query.filter(Company.cname==cname).first()
    user=current_user.id
    
    company=Company.query.filter(and_(Company.cname==cname, Company.userid==current_user.id)).first()
    
    if not company: 
        return "Company does not exist in Database"
    else:
        employees = Employee.query.filter_by(cid=company.cid).all()
        return render_template('eeview.html', company=company, employees=employees)
        
    
#RUN pay from here
@app.route('/newrunpay', methods=['GET', 'POST'])
@login_required    
def newrunPay():
    form = PayForm()
    name = current_user.email
    cname=request.args.get("company")
    company=Company.query.filter(and_(Company.cname==cname, Company.userid==current_user.id)).first()
    employees = Employee.query.filter_by(cid=company.cid).all()
    return render_template('newrunpay.html', name=name, company=company, employees=employees, form=form)


#Gross Pay to Net Pay
@app.route('/grossnetpay', methods=['GET', 'POST'])
@login_required    
def grossnetPay():
    gform = request.form
    # return (gform)
    grosspay = { x:gform[x] for x in gform}
    cid=grosspay.get('cid')
    userid=grosspay.get('userid')
    grosspay.pop("cid")
    grosspay.pop("userid")
    grosspay.pop('csrf_token')
    grosspay.pop('submit')
    paymaster = grosspay
    for x in grosspay:
    #     # first get each employees: netpay, fedincomtx, FICA, Medicare, cfica, cmedicare
    #     #TODO get 'eid' retrieve from Employee and get 'filing_status' from paytable
        try:
            
            paytable = PayTable.query.filter_by(eid=x).first()
            employee = Employee.query.filter_by(eid=x).first()

            filing_status = employee.filing_status
            pfreq = int(paytable.pfreq)
            gpay = int(grosspay[x])
            paydict = taxcalc.witholding(gpay, pfreq, filing_status)
            
            new_paycheck = Paycheck(userid=userid,cid=cid, eid=x, grosspay=grosspay[x], fedtax=paydict.get("fedtax"), fica=paydict.get("fica"), medicare=paydict.get("medicare"), cfica=paydict.get("cfica"), cmedicare=paydict.get("cmedicare"), netpay=paydict.get("netpay"))
            db.session.add(new_paycheck)
            db.session.commit()
            
            
        except:
            return "not working"
    #This query allows you to select only employees from cid and then joins the paycheck table
    employees = db.session.query(Employee, Paycheck).join(Paycheck).where(Employee.cid==cid, Paycheck.paid==0).all()

    # employees = Paycheck.query.filter_by(paid=False).all()
    # return (tobepaid)
        
    # return "Records of Gross Pay, Net Pay, Fed Tax, FICA, Medicare all entered into datbase."
    return render_template('netpay.html', employees=employees, cid=cid)


    # return render_template('netpay.html', grosspay=grosspay, cid=cid, userid=userid)


# @app.route('/runpay', methods=['GET', 'POST'])
# @login_required    
# def runPay():
#     form = VenmoForm()
#     name = current_user.email
#     cname=request.args.get("company")
#     company=Company.query.filter(and_(Company.cname==cname, Company.userid==current_user.id)).first()
#     if not company: 
#         return "Invalid URL"
#     else:
#         eeall = Employee.query.filter_by(cid=company.cid).all()
#         return render_template('runpaywiz.html', employees=eeall, company=company, name=name, form=form)





#Dwolla - Customer Creation and ID Retrieval

# @app.route('/dwolla', methods=['GET', 'POST'])
# def dwolla():
#     form = DwollaCustForm()
#     return render_template('dwcustcrt.html', form = form)

# @app.route('/dwcustsetup', methods=['GET', 'POST'])
# def dwcustsetup():
#     fname = request.form.get('dfname')
#     lname = request.form.get('dlname')
#     email = request.form.get('demail')
#     bankacct = request.form.get('dbnkacct')
#     bankrout = request.form.get('dbnkrout')
#     banktype = request.form.get('dacctype')
#     bankacctname = request.form.get('dacctnm')
#     z,y = dwollafull.createemplyee('fname','lname','email','bankrout','bankacct','banktype', 'bankacctname')
#     return ("Hello Dwolla Customer!" + (z,y))



#Venmo credentials coming back
@app.route('/vlogin', methods=['GET', 'POST'])
@login_required
def vlogin():
    form = VenmoForm()
    name = current_user.email
    if request.method == 'POST':
        venusername = form.venusername.data
        venpassword = form.venpassword.data
        bankaccounts = venmologin(venusername=venusername, venpassword=venpassword)
        return  render_template('eeconfirmpay.html', name=name, bankaccounts=bankaccounts, vusername=venusername, vpasswd=venpassword)
    
@app.route('/vlink', methods=['GET', 'POST'])
@login_required
def vlink():
    if request.method == 'POST':
        bankaccount = request.form.get('bankaccount')
        vusername = request.form.get('vusername')
        vpasswd = request.form.get('vpasswd')
        
    return render_template('submitvenmo.html', account=bankaccount, vusername=vusername, vpasswd=vpasswd )

@app.route('/submitvenmo', methods=['GET', 'POST'])
@login_required
def submitevenmo():
    if request.method == 'POST':
        account = request.form.get('account')
        venacct = request.form.get('venmoacct')
        amount = request.form.get('amount')
        note = request.form.get('note')
        vusername = request.form.get('vusername')
        vpasswd = request.form.get('vpasswd')
        message = send_funds(vnum=account, vacct=venacct, vamount=amount, vnote=note, venusername=vusername, venpassword=vpasswd)
          
    return (message)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.email)


##### USER PROFILE #######
@app.route('/profile')
@login_required
def profile():
    form = UserForm()
    return render_template('profile.html', current_user=current_user, form=form)

@app.route('/profileupdate', methods=['GET', 'POST'])
@login_required
def profileupdate():
    form=UserForm()
    if request.method == 'POST':
        ##### STOPPED HERE NEED TO INPUT FORM DATA INTO DB #######
        user = User.query.filter_by(id=current_user.id).first()
        user.email=form.email.data
        user.fname=form.fname.data
        user.lname=form.lname.data
        user.phone=form.phone.data
        user.password=generate_password_hash(form.password.data, method='sha256')
        db.session.commit()
        
        return render_template('updatedprofile.html', user=user)

##### LOGOUT ##############
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/company', methods=['GET', 'POST'])
@login_required
def company():
    return render_template('company.html')


@app.route('/addcompany2', methods=['GET', 'POST'])
@login_required
def addcompany2():
    
    if request.method == "POST":
        #check company name if already there then don't add and redirect with msg to login
        company = request.form.get('cname')
        existCompany = Company.query.filter(and_(Company.cname==request.form.get('cname'), Company.userid==current_user.id)).first()
        if existCompany == None:
            # company = request.form.get('cname')
            cfirstname = request.form.get('cfirstname')
            clastname = request.form.get('clastname')
            cemail = request.form.get('cemail')
            cipaddress = request.form.get('cipaddress')
            ctype = request.form.get('ctype')
            cdob = request.form.get('cdob')
            cssn = request.form.get('cssn')
            addr1 = request.form.get('addr1')
            addr2 = request.form.get('addr2')
            city = request.form.get('city')
            state = request.form.get('state')
            zcode = request.form.get('zcode')
            cbusclass = request.form.get('cbusclass')
            cbustype = request.form.get('cbustype')
            cname = request.form.get('cname')
            fein = request.form.get('fein')
            cbankrout = request.form.get('cbankrout')
            cbankacct = request.form.get('cbankacct')
            cdwacctype = request.form.get('cdwacctype')
            cbankacctnm = request.form.get('cbankacctnm')
            phone = request.form.get('phone')
            url = request.form.get('url')
            contactname = request.form.get('contactname')
            cphone = request.form.get('cphone')
            
            #Dwolla - folloing sets up customer in Dwolla and provides Dwollaid and Dwolla Source ID
            # v,w = dwollafull.createemployer(cfirstname, clastname, cemail, cipaddress, ctype, cdob, cssn, addr1, city, state, zcode, cbusclass, cbustype, cname,'11-1111111', cbankrout, cbankacct, cdwacctype, cbankacctnm)
            v,w = dwollafull.createemployer(cfirstname, clastname, cemail, cipaddress, ctype, cdob, cssn,addr1,city, state, zcode, '9ed3f670-7d6f-11e3-b1ce-5404a6144203', cbustype, cname, fein,cbankrout, cbankacct, cdwacctype, cbankacctnm)

            # v,w = dwollafull.createemployer('Business2','Owner','BizzOwner66@email.com','143.156.7.8','business','1980-01-31','6789','99-99 33rd St','Some City', 'NY', '11101', 'restaurant', 'soleProprietorship', 'Jinx', '11-1111111','222222226','987654321','checking', 'BusinessBankAcctName')

            
            
            new_company = Company(cfirstname=cfirstname, clastname=clastname, cemail=cemail, cipaddress=cipaddress, ctype=ctype, cdob=cdob, cssn=cssn, addr1=addr1, addr2=addr2, city=city, state=state, zcode=zcode, cbusclass=cbusclass, cbustype=cbustype, cname=cname, fein=fein, cbankrout=cbankrout, cbankacct=cbankacct, cdwacctype=cdwacctype, cbankacctnm=cbankacctnm,  userid=current_user.id, phone=phone, url=url, contactname=contactname, cphone=cphone, cdwollaid=v, cdwollasid=w)
            db.session.add(new_company)
            db.session.commit()
            return redirect('/login')
        #the company EXITS here: 
        else:
            user = current_user
            companys = Company.query.filter_by(userid=user.id).all()
            message = "Company already exists"
            return render_template('main.html', message=message, name=user.email, companys=companys )
    
# if __name__ == '__main__':
#     app.run(debug=True)

@app.route('/eeinput')
def eeinput():
    # return "Employee {name} Input route".format(name="Vajih")
    title = 'Input Page'
    return render_template('eeinput.html', title=title)

@app.route('/eepreview', methods=['GET', 'POST'])
def eeconfirm():
    # return "Confirm html page here"
    if request.method == "POST":
        vacct = request.form.get('vacct')
        vamount = request.form.get('npay')
        vnote = request.form.get('note')
        #print(vnote)
        title = 'Preview'
        return render_template('eeconfirm.html', vacct=vacct, vamount=vamount, vnote=vnote)

@app.route('/eeconfirmpay', methods=['GET', 'POST'])
def eeconfirmpay():
    if request.method == "POST":
        vacct = request.form.get('vacct')
        vamount = request.form.get('vamount')
        vnote = request.form.get('vnote')
        venusername = request.form.get('venusername')
        venpassword = request.form.get('venpassword')
        bankaccts = login(venusername=venusername, venpassword=venpassword)
        # return login(venusername=venusername, venpassword=venpassword)
        
        #return send_funds(vacct=vacct, vamount=vamount, vnote=vnote, venusername=venusername, venpassword=venpassword)
        return render_template('eeconfirmpay.html', bankaccts=bankaccts)



# ******* A C H   ********


#Dwolla payment from Employer to Employee
@app.route('/achpay', methods=['GET', 'POST'])
@login_required
def achpay():
    cid = request.args.get('cid')
    eid = request.args.get('eid')
    value = request.args.get('netpay')
    company = Company.query.filter(and_(Company.cid==cid)).first()
    employee = Employee.query.filter(and_(Employee.cid==cid, Employee.eid==eid)).first()
    transourceid = company.cdwollasid
    transdestinationid = employee.eedwollafid

    item = request.args.get('paycheckid')

    update = db.session.query(Paycheck).filter(Paycheck.paycheckid==item).first()
    update.paid = True
    db.session.commit()

    dwollafull.transfer(transourceid,transdestinationid,value, "paymentid", 'note')


    return("Paycheck Processed - ID:" + str(update.paycheckid) + "<br>" + "Employee name:" + (employee.fname) + " " + (employee.lname) + "<br>" + "From Company:" + (company.cname) + "<br>" + "Amount: " + (value))






###### This is the section to calculate Net Wage from Gross Wage and deductions per From IRS 15-T (2021) and W4 inputs###

@app.route('/<int:wage>/<int:period>/<status>')
def witholding(wage, period,status):
    fica_witholding=wage * 0.062
    meidcare_witholding=wage * 0.0145
    
    one_a = wage
    one_b = period
    one_c = wage * period

    
    one_d= w4_4a = 0.0
    one_e = one_c + one_d
    one_f = w4_4b = 0.0
    
    if status == 'mfj':
        one_g = w4_setp2 = 12900
    else:
        one_g=8600
        
    one_h = one_f + one_g
    one_i = aawa = one_e - one_h
    


    # base_witholding = 0
    # tax_bracket = 0
    # aawe = 0
    
#Single or Married Filing Separately Tax Table look up.
# def witholding(wage):
# def witholding(aawa, period):
    if status == "mfj":
        if aawa >= 0 and aawa <12200:
            base_witholding = 0
            tax_bracket = 0
            aawe=0
        if aawa >= 12200 and aawa < 32100:
            base_witholding = 0
            tax_bracket =.1
            aawe=12200
        if aawa >= 32100 and aawa < 93250:
            base_witholding = 1990
            tax_bracket =.12
            aawe=32100
        if aawa >= 93250 and aawa < 184950:
            base_witholding = 9328
            tax_bracket =.22
            aawe=93250
        if aawa >= 184950 and aawa < 342050:
            base_witholding = 29502
            tax_bracket =.24
            aawe=184950
        if aawa >= 342050 and aawa < 431050:
            base_witholding = 67206
            tax_bracket =.32
            aawe=342050
        if aawa >= 431050 and aawa < 640500:
            base_witholding = 95686
            tax_bracket =.35
            aawe=431050
        if aawa >= 640500:
            base_witholding = 168993.5
            tax_bracket =.37
            aawe=640505
    
    if status == "mfs":
        if aawa >= 0 and aawa <3950:
            base_witholding = 0
            tax_bracket = 0
            aawe=0
        if aawa >= 3950 and aawa < 13900:
            base_witholding = 0
            tax_bracket =.1
            aawe=3950
        if aawa >= 13900 and aawa < 44475:
            base_witholding = 995
            tax_bracket =.12
            aawe=13900
        if aawa >= 44475 and aawa < 90325:
            base_witholding = 4664
            tax_bracket =.22
            aawe=44475
        if aawa >= 90325 and aawa < 168875:
            base_witholding = 14751
            tax_bracket =.24
            aawe=90325
        if aawa >= 168875 and aawa < 213375:
            base_witholding = 33603
            tax_bracket =.32
            aawe=168875
        if aawa >= 213375 and aawa < 527550:
            base_witholding = 47843
            tax_bracket =.35
            aawe=213375
        if aawa >= 527550:
            base_witholding = 157804.25
            tax_bracket =.37
            aawe=527550
    
    if status == "hh":
        if aawa >= 0 and aawa <10200:
            base_witholding = 0
            tax_bracket = 0
            aawe=0
        if aawa >= 10200 and aawa < 24400:
            base_witholding = 0
            tax_bracket =.1
            aawe=10200
        if aawa >= 24400 and aawa < 64400:
            base_witholding = 1420
            tax_bracket =.12
            aawe=24400
        if aawa >= 64400 and aawa < 96550:
            base_witholding = 6220
            tax_bracket =.22
            aawe=64400
        if aawa >= 96550 and aawa < 175100:
            base_witholding = 13293
            tax_bracket =.24
            aawe=96550
        if aawa >= 175100 and aawa < 219600:
            base_witholding = 32145
            tax_bracket =.32
            aawe=175100
        if aawa >= 219600 and aawa < 533800:
            base_witholding = 46385
            tax_bracket =.35
            aawe=219600
        if aawa >= 533800:
            base_witholding = 156355
            tax_bracket =.37
            aawe=533800
        
    fed_witholding = (base_witholding+(tax_bracket * (aawa - aawe))) / period
    
    cfica = str(0.062 * one_a)
    cmedicare =  str(0.0145 * one_a)
    
    #Make strings for printing
    gross_wage=str(one_a)
    netpay=str(round((one_a - fed_witholding-fica_witholding-meidcare_witholding),2))
    fica=str(fica_witholding)
    medicare=str(round(meidcare_witholding,2))
    tax_bracket=str(tax_bracket)
    fed_witholding = str(round(fed_witholding, 2))
    
    
    
    
    return "Gross Pay: ${gross_wage}<br> Net Pay: ${netpay}<br>Federal Income Tax Witholding: <strong>${fed_witholding}</strong><br> FICA: <strong>${fica}</strong><br> Medicare: <strong>${medicare}</strong><br>Corp FICA (upto wage of $142,800 wage in 2021): <strong>${cfica}</strong><br>Corp Medicare: <strong>${cmedicare}</strong>".format(gross_wage=gross_wage, netpay=netpay,fed_witholding=fed_witholding, fica=fica, medicare=medicare, cfica=cfica, cmedicare=cmedicare)

@app.route('/w4')
def w4():
    return render_template('w4_form.html')


# app.run(debug=True)