#SIGNUP

from flask import *
import pymysql

app = Flask(__name__)
#Set key to secure your session
app.secret_key = "gfdfhvnnxbsfkjvfi--gnvknkgedv-edvni45336ikfawier4q534qt____uyuwree68763"
# print(__name__)
#add your functions
@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == "POST":
        names = request.form['names']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        tel = request.form['tel']

        #Validation
        if ' ' not in names:
            return render_template('signup.html', message="Names should be 2 words")
        elif '@' not in email:
            return render_template('signup.html', message="Invalid Email")
        elif len(password) <2:
            return render_template('signup.html', message="Password must equal to 8")
        elif password != confirm:
            return render_template('signup.html', message="Passwords do not match")
        elif len(tel) !=13:
            return render_template('signup.html', message="Invalid phone")
        elif not tel.startswith("+"):
            return render_template('signup.html', message="Must start with a +")
        else:
            connection = pymysql.connect(host='localhost', user='root',
                                         password='', database='modcom_db')

            #CRUD  C-create R-reading U-update D-delete
            #we start with Create(it uses insert)
            #%s means value placeholder
            #sql = INSERT INTO `users`(`names`, `email`, `password`, `tel`) VALUES ('Tom','tom@gmail.com','1234','76578886')
            sql = "INSERT INTO `users`(`names`, `email`, `password`, `tel`) VALUES (%s,%s,%s,%s)"
            #CREATE a CURSOR -  to be used in sql

            cursor = connection.cursor()
            try:
                cursor.execute(sql,(names, email, password, tel))
                connection.commit()
                #send email, send sms
                #how to send email in python
                #send mail from your gmail account using python
                #https://justpaste.it/68np5
                import africastalking
                africastalking.initialize(
                    username='joe2022', api_key='15d1fb388bcb3cb033f75b7fffcb9d0b45ff71352a9bed062487b99c0b5ce670'
                )

                sms = africastalking.SMS
                recipients =[tel]
                message = "Dear {}, congratulations, sign up successful ".format(names)
                sender = "AFRICASTKNG"

                try:

                    response = sms.send(message, recipients)
                    print(response)
                except:
                    print("SMS NOT sent")


                return render_template('signup.html', message="Successful")
            except:
                connection.rollback()
                return render_template('signup.html', message="Errror Occured")

    else:
      return render_template('signup.html')   #no post done
       #return render_template('signin.html)



#SIGNIN
@app.route("/signin", methods=['POST', 'GET'])
def signIn():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        connection = pymysql.connect(host='localhost', user='root',
                                     password='', database='modcom_db')
        sql = "SELECT * FROM users WHERE email = %s and password = %s"

        cursor = connection.cursor()     #execute sql
        cursor.execute(sql, (email, password))
        #you count the cursor
        if cursor.rowcount ==0:
           return render_template('signin.html', message="Incorrect Email or Password!")
        elif cursor.rowcount ==1:
            #Logic needed
            #You need to create user session key
            session['key'] = email  #Attach the key to an email, Use PK(Primary Key)
            return redirect('/appointments')
            # return render_template('signin.html', message="Successful login")
        else:
            return render_template('signin.html', message="Error try again")
    else:
        return render_template('signin.html')

#Logout
@app.route("/logout")
def logout():
    session.pop('key', None)
    return  redirect('/signin')



#Appointments
@app.route('/appointments', methods = ['POST', 'GET'])
def appointments():
    if 'key' not in session:
        return redirect('/signin') #send the user to signin to get a key
    else:  #user has a key and they are logged in
        if request.method == "POST":
            email = request.form['email']
            appointment_date = request.form['appointment_date']
            appointment_time = request.form['appointment_time']
            specialist = request.form['specialist']

            from datetime import date
            today = date.today()
            if appointment_date > str (today):
                return render_template('appointments.html', message="Invalid date")

            else:
                connection = pymysql.connect(host='localhost', user='root', password='', database='modcom_db')
                sql = "INSERT INTO medicines(medicine_name, category, expiry_date, quantity, cost) Values (%s,%s,%s,%s,%s)"
                cursor = connection.cursor()

                try:
                    cursor.execute(sql, (email, appointment_date, appointment_time, specialist))
                    connection.commit()
                    return render_template('appointments.html', message="Done")
                except:
                    connection.rollback()
                    return render_template('appointments.html', message="Not Done")

        else:
                return render_template('appointments.html')





#MEDICINES
@app.route('/medicines', methods = ['POST', 'GET'])
def medicines():
    if request.method == "POST":
        medicine_name = request.form['medicine_name']
        category = request.form['category']
        expiry_date = request.form['expiry_date']
        quantity = request.form['quantity']
        cost = request.form['cost']


        if float(cost) < 0:
            return render_template('medicines.html', message="Invalid")

        else:
            connection = pymysql.connect(host='localhost', user='root', password='', database='modcom_db')
            sql = "INSERT INTO medicines(medicine_name, category, expiry_date, quantity, cost) Values (%s,%s,%s,%s,%s)"
            cursor = connection.cursor()

            try:
                cursor.execute(sql, (medicine_name, category, expiry_date, quantity, cost))
                connection.commit()
                return render_template('medicines.html', message="Done")
            except:
                connection.rollback()
                return render_template('medicines.html', message="Not Done")

    else:
        return render_template('medicines.html')







#GETMEDICINES
#This is the main route
@app.route('/')
def getmedicines():
    connection = pymysql.connect(host='localhost', user='root', password='', database='modcom_db')
    sql = "SELECT * FROM medicines ORDER BY qty DESC"
    cursor =  connection.cursor()
    cursor.execute(sql)
    if cursor.rowcount == 0:
        return render_template('getmedicines.html', message='No medicines')
    else:
        rows = cursor.fetchall()
        return render_template('getmedicines.html', rows = rows)




#PHONES
@app.route('/phones', methods=['POST', 'GET'])
def phones():
    if request.method == "POST":
        phone_name = request.form['phone_name']
        brand_name = request.form['brand_name']
        cost = request.form['cost']
        discount = request.form['discount']
        specifications = request.form['specifications']

        if float(cost) < 0:
            return render_template('phones.html', message="Invalid")

        else:
            connection = pymysql.connect(host='localhost', user='root', password='', database='modcom_db')
            sql = "INSERT INTO phones(phone_name, brand_name, cost, discount, specifications) Values (%s,%s,%s,%s,%s)"
            cursor = connection.cursor()

            try:
                 cursor.execute(sql, (phone_name, brand_name, cost, discount, specifications))
                 connection.commit()
                 return render_template('phones.html', message="Done")
            except:
                connection.rollback()
                return render_template('phones.html', message="Not Done")

    else:
        return render_template('phones.html')


    #GETPHONES
@app.route('/getphones', methods = ['POST', 'GET'])
def getphones():
    connection = pymysql.connect(host='localhost', user='root', password='', database='modcom_db')
    sql = "SELECT * FROM phones ORDER BY cost DESC"
    cursor = connection.cursor()
    cursor.execute(sql)
    if cursor.rowcount == 0:
        return render_template('getphones.html', message='No phones')
    else:
        rows = cursor.fetchall()
        return render_template('getphones.html', rows = rows)


#This route recieves a product_id for the selected product from previous page
@app.route('/single/<medicine_id>')
def single(medicine_id):
    sql = "select * from medicines where medicine_id = %s"
    connection = pymysql.connect(host='localhost', user='root', password='', database='modcom_db')
    cursor = connection.cursor()
    cursor.execute(sql, (medicine_id))   #Provide medicine id to sql
    row = cursor.fetchone()      #We only fetch one row based on medicine ID
    return  render_template('single.html', row = row)



#Check out route
#CHECKOUT
#Save to database, 2.Send sms 3.Send email 4.make payments
#Sign up daraja, consumer key and secret key
#modcom.co.ke/codes/mpesa.txt
#Make payments
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
@app.route('/checkout', methods = ['POST','GET'])
def mpesa_payment():
        if request.method == 'POST':
            phone = str(request.form['phone'])
            amount = float(request.form['amount'])
            qty = float(request.form['qty'])
            amount = amount * qty

            address = str(request.form['address'])
            medicine_id = str(request.form['medicine_id'])
            # GENERATING THE ACCESS TOKEN
            consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
            consumer_secret = "amFbAoUByPV2rM5A"

            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
            r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

            data = r.json()
            #If your consumer and secret keys are valid you get a vtoken
            access_token = "Bearer" + ' ' + data['access_token']

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
            business_short_code = "174379"
            data = business_short_code + passkey + timestamp
            encoded = base64.b64encode(data.encode())  #UTF 8
            password = encoded.decode('utf-8')


            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379", #Test paybill
                "Password": "{}".format(password),
                "Timestamp": "{}".format(timestamp),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                "AccountReference": "MUNENE WANDARE",
                "TransactionDesc": "account"
            }

            # POPULAING THE HTTP HEADER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

            response = requests.post(url, json=payload, headers=headers)
            print (response.text)
                  #TODO
            #Save to database
            #pay_id(PK AI), medicine_id, amount, phone, qty, address
            #TODO
            #Create a table named orders with above columns
            #Use insert to save medicine_id, amount, phone, qty, address
            connection = pymysql.connect(host='localhost', user='root', password='', database='modcom_db')
            sql = "INSERT INTO `orders`(`medicine_id`, `amount`, `phone`, `qty`, `address`) VALUES (%s,%s,%s,%s,%s)"
            cursor = connection.cursor()
            cursor.execute(sql, (medicine_id, amount, phone, qty, address))
            connection.commit()
            #Do more products routes
            return render_template('payment.html', msg = 'Please Complete Payment in Your Phone')
        else:
            return render_template('payment.html')

           #TASK
#create a table called appointments
#columns are email VARCHAR, appointments_date VARCHAR, appointment_time VARCHAR
#ceate a template named appointment.html create input as pre above table
#create python route named / appointments and save to sql.
#Refer sign up
#can specify parameter port=9000

        #TASK
 #how to send email with gmail in python (tutorialspoint.com)
 #send mail from your Gmail account using python

           #TASK
#create another table name medicines
#columns: medicine_id PK, AI, medicine_name, category, expiry_date, quantity, cost
#Do a form and python route to save
#route name is / medicines
#templates medicines.html


         #TASK
#Create a table named products, must have cost, qty, image_url, name
#Create a route to retrieve the products(Load 10 products)
#Create a template to display the product

if __name__ == '__main__':
 app.run()