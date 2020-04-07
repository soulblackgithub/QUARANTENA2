from flask import Flask, render_template, json, request , url_for , redirect , flash
from flask_sqlalchemy import SQLAlchemy
#from flaskext.mysql import MySQL
#from werkzeug import generate_password_hash, check_password_hash
app = Flask(__name__)
#mysql.init__app(app)
# MySQL configurations
#db = SQLAlchemy(app)

# MySQL configurations
app.config[SECRET_KEY] ='12345'
app.config['SQLALCHEMY_USER_URI'] ='sqlite:///site.db' ###'jay'
app.config['SQLALCHEMY_DATABASE_PASSWORD_URI'] = 'sqlite:///site.db'###'jay'
app.config['SQLALCHEMY_DATABASE_DB_URI'] ='sqlite:///site.db' ###'BucketList'
app.config['SQLALCHEMY_DATABASE_HOST_URI'] ='sqlite:///site.db'### 'localhost'



@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

if __name__ == "__main__":
    app.run(port=5002)
