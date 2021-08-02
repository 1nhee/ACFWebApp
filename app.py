from flask import Flask, render_template, request, session, redirect, url_for
import pymysql

#Create Flask object instance
app = Flask(__name__)

db = pymysql.connect(host='acfwebapp.mysql.database.azure.com',
                                  user='acfwebapp@acfwebapp',
                                  db='userdb', password='HelloAC4all!20Always1', charset='utf8',
                     ssl={'ca': 'BaltimoreCyberTrustRoot.crt.pem'})

@app.route('/', methods=['GET', 'POST'])
def home():
  error = None
  id = session['signInId']
  return render_template('home.html', error=error, name=id)

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
  error = None

  if request.method == 'POST':
    id = request.form['signInId']
    password = request.form['signInpw']

    try:
      with db.cursor() as cursor:
        sql = "SELECT id FROM userdb WHERE id = %s AND password = %s"
        value = (id, password)
        cursor.execute(sql, value)
        data = cursor.fetchall()

        for row in data:
            data = row[0]

        if data:
            session['signInId'] = id
            return redirect(url_for('home'))
        else:
            error = 'invalid input data detected !'

    finally:
      cursor.close()
      db.close()

  return render_template('signIn.html', error=error)

@app.route('/signUp', methods=['GET', 'POST'])
def register():
  error = None
  if request.method == 'POST':
    id = request.form['signUpId']
    password = request.form['signUpPw']

    try:
      with db.cursor() as cursor:
        sql = "INSERT INTO users VALUES ('%s', '%s')" % (id, password)
        cursor.execute(sql)
        data = cursor.fetchall()

        if not data:
          db.commit()
          return redirect(url_for('home'))
        else:
          db.rollback()
          return "Sign-Up Failed"

    finally:
      cursor.close()
      db.close()

  return render_template('signUp.html', error=error)

if __name__=="__main__":
  app.run(debug=True)
  # If you want to access a specifiy address or port #
  # app.run(host="127.0.0.1", port="5000", debug=True)

