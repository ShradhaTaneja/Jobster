from flask import Flask, session, request, render_template
from app.student.controllers import api as student_api

app = Flask(__name__)

# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
# 	return User.get(user_id)


@app.route('/', methods = ['GET'])
def home():
	return render_template('index.html')

@app.route('/test', methods=['GET'])
def test():
    print session
    return render_template('ui-cards.html')
    return 'test from controller - student'




app.register_blueprint(student_api)
