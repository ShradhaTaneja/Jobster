from flask import Flask, session, request, render_template

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
	return render_template('index.html')


from app.student.controllers import api as student_api


app.register_blueprint(student_api)

