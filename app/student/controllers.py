from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for

from werkzeug.datastructures import CombinedMultiDict

api = Blueprint('student', __name__, url_prefix = '/student')

# @api.before_request
# def before_request():
#     # if 'logged_in' not in session and request.endpoint != 'student.login':
#     if 'logged_in' not in session:
#         print session
#         print request.endpoint
#         print '@@@@@@@@@@@ through before request'
#         return render_template('student_login.html')
# @api.route('/shradha', methods=['GET'])
# def shradha():
#     return render_template('test.html')

@api.route('/', methods=['GET'])
def home():
    err_msg = None
    # err_msg = 'invalid email'
    return render_template('student_index.html', err_msg = err_msg)

@api.route('/home', methods=['GET'])
def home_page():
    print 'student home'
    if 'user_name' not in session:
        return render_template('student_index.html', err_msg='Please login..!')
    err_msg = None
    # err_msg = 'invalid email'
    return render_template('student_home.html', err_msg = err_msg)



@api.route('/login', methods = ['GET', 'POST'])
def login():
    print '________________________________________', request.method
    print '______', request.form
    print session
    if 'user_name' not in session:
        if request.method == 'GET':
            return render_template('student_index.html')
        elif request.method == 'POST':
            user_name = request.form['user_name']
            password = request.form['password']
            # check for valid credentials
            valid_user = True
            if valid_user:
                session['user_name'] = user_name
                return render_template('student_home.html')
            else:
                return render_template('student_index.html', err_msg= 'User Name not found.!')
    else:
        return render_template('student_home.html', user_name = session['user_name'])

@api.route('/logout', methods= ['GET'])
def logout():
    session.pop('user_name', None)
    print session
    return render_template('student_index.html', msg = 'Logout Successful.!')

@api.route('/test', methods=['GET'])
def test():
    print session
    return 'test from controller - student'

# @api.route('/', methods=['GET'])
# @api.route('/<rid>', methods=['GET'])
# def get_all(rid = None):
#     if rid is None:
#         all_data = module.get_all_students()
#     else:
#         print 'inside controller, rid given calling get rest'
#         all_data = module.get_student(rid)
#     return jsonify(all_data)

# @api.route('/add', methods=['POST'])
# def add_student():
#     required_parameters = ['name', 'address', 'city', 'state', 'contact']
#     incoming_data = dict(request.get_json())
#     incoming_parameters = incoming_data.keys()

#     if len(set(required_parameters) - set(incoming_parameters)) > 0:
#         return jsonify({
#                 'status' : 'failure',
#                 'message' : 'missing parameters.. you need to give it ALL.. :P (%s)' % (', '.join(required_parameters))
#                 })

#     response = module.add_student(incoming_data)
#     return jsonify(response)

# @api.route('/delete/<rid>', methods=['GET'])
# def delete_student(rid):
#     all_data = module.remove_student(rid)
#     return jsonify(all_data)
