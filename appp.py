from flask import *
import pymysql

app = Flask(__name__)


@app.route('/appointments', methods = ['POST', 'GET'])
def appointments():
    if request.method == "POST":
        email = request.form['email']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        specialist = request.form['specialist']

        from datetime import date
        today = date.today()
        if appointment_date < str(today):
            return render_template('appointments.html', messsage="Invalid date")

        else:
            connection = pymysql.connect(host='localhost', user='root', password='', datbase='modcom_db')
            sql = "INSERT INTO appointments(email, appointment_date, appointment_time, specialist) Values (%s,%s,%s,%s)"
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

if  __name__ =='__main__':
    app.run()
