from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for

from werkzeug.datastructures import CombinedMultiDict

api = Blueprint('student', __name__, url_prefix = '/student')

@api.before_request
def before_request():
    # if 'logged_in' not in session and request.endpoint != 'student.login':
    if 'logged_in' not in session:
        print session
        print request.endpoint
        print '@@@@@@@@@@@ through before request'
        return render_template('student_login.html')


@api.route('/login', methods = ['GET', 'POST'])
def login():
    print request.method, '_________________'
    print session, '<<< session'
    if 'logged_in' in session.keys() and session['logged_in']:
        print 'logged in returning home'
        return render_template('student_home.html')
    elif request.method == 'GET':
        print 'get request.. returing login page'
        return render_template('student_login.html')
    elif request.method == 'POST' and 'logged_in' not in session.keys():
        print 'post req.. creating session'
        session['logged_in'] = True
        session['user'] = request.form['user']
        print session    
        return render_template('student_home.html')




    # if 'logged_in' in session and session['logged_in']:
    #     print 'not logged in'
    #     return render_template('student_home.html')
    # if request.method == 'GET':
    #     return render_template('student_login.html')
    # print '>>>>>>>>>>>>> not get.. setting session value'
    # session['logged_in'] = True
    # session['user'] = request.form['user']
    # return 'kya tum logged in ho ? '
    # return render_template('student_home.html')

@api.route('/logout', methods= ['GET'])
def logout():
    session.pop('logged_in')
    session.pop('user')
    print session


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
