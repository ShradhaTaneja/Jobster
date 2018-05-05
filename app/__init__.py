from flask import Flask, session, request, render_template

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
	return render_template('index.html')

@app.route('/test', methods=['GET'])
def test():
    print session
    return render_template('ui-cards.html')
    return 'test from controller - student'


from app.student.controllers import api as student_api


app.register_blueprint(student_api)

