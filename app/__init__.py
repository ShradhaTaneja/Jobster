from flask import Flask, session, request, render_template
from flask.ext.login import LoginManager
from user import User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods = ['GET'])
def home():
	return render_template('index.html')


from app.student.controllers import api as student_api


app.register_blueprint(student_api)

