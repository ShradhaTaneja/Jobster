from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from werkzeug.datastructures import CombinedMultiDict
from app.commons.modules import student 

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
def index(err_msg = None, msg = None):
    err_msg = None
    # err_msg = 'invalid email'
    return render_template('student_index.html', err_msg = err_msg, msg = msg)

@api.route('/home', methods=['GET'])
def home_page():
    # print 'student home'
    if 'user_email' not in session:
        return render_template('student_index.html', err_msg='Please login..!')
    err_msg = None
    popular_data = student.get_popular_data()
    recent_jobs = student.get_recent_jobs()
    # print popular_data, '$$$$$$$$$$$$$$$'
    # err_msg = 'invalid email'
    return render_template('student_home.html', err_msg = err_msg, popular_data = popular_data, recent_jobs = recent_jobs)



@api.route('/profile_edit', methods = ['GET', 'POST'])
def profile_edit():
    s_id = student.get_id(session['user_email'])
    if request.method == 'GET':
        data = student.get_student_profile(int(s_id))
        print data['data']
        return render_template('student_profile_edit.html', data = data['data'])
    else:
        print request.form
        resume = request.files['resume']
        print resume, '<<<<<<<<<<<<<<'
        # resume_data = 
        # update db
        data = student.update_student_profile(int(s_id), resume = resume, data = request.form)
        return render_template('student_profile_edit.html', msg = 'Updated.!', data = data['data'])


@api.route('/view_company', methods = ['GET'])
def view_company():
    c_id = request.args['c_id']
    # c_id = 2
    data = student.company_profile(int(c_id))
    # err_msg = None
    # popular_data = student.get_popular_data()
    # recent_jobs = student.get_recent_jobs()
    # # print popular_data, '$$$$$$$$$$$$$$$'
    # # err_msg = 'invalid email'
    # return render_template('student_home.html', err_msg = err_msg, popular_data = popular_data, recent_jobs = recent_jobs)

    return render_template('company_profile.html', data = data)

@api.route('/login', methods = ['GET', 'POST'])
def login():
    print '________________________________________', request.method
    print '______', request.form
    print session
    if 'user_email' not in session:
        if request.method == 'GET':
            return render_template('student_index.html')
        elif request.method == 'POST':
            popular_data = student.get_popular_data()
            recent_jobs = student.get_recent_jobs()
            user_email = request.form['user_email']
            password = request.form['password']
            # check for valid credentials
            valid_user = True
            # print student.exists(user_email), '>>>>>>>>>>>'
            # print '###########', student.correct_credentials(user_email, password)
            if student.exists(user_email) and student.correct_credentials(user_email, password):
                # print '################'
                session['user_email'] = user_email
                # print '_________user inserted ', session

                print '++++++++++++ ', recent_jobs
                return render_template('student_home.html', user_email = user_email, popular_data = popular_data, recent_jobs = recent_jobs)
            else:
                return render_template('student_index.html', err_msg= 'User not found, or Invalid credentials!')
    else:
        popular_data = student.get_popular_data()
        recent_jobs = student.get_recent_jobs()
        return render_template('student_home.html', user_email = session['user_email'], popular_data = popular_data, recent_jobs = recent_jobs)

@api.route('/logout', methods= ['GET'])
def logout():
    session.pop('user_email', None)
    # print session
    return redirect(url_for('student.index'))
    # return render_template('student_index.html', msg = 'Logout Successful.!')

@api.route('/test', methods=['GET'])
def test():
    err_msg = None
    popular_data = student.get_popular_data()
    recent_jobs = student.get_recent_jobs()
    # print popular_data, '$$$$$$$$$$$$$$$'
    # err_msg = 'invalid email'
    return render_template('student_home.html', err_msg = err_msg, popular_data = popular_data, recent_jobs = recent_jobs)

    print session
    return 'test from controller - student'

@api.route('/register', methods = ['POST'])
def register():
    response = student.register(request.form)
    if student.exists(str(request.form['user_email'])):
        return render_template('student_index.html', err_msg = 'Email already used.! ')
    if response['status'] == 'success':
        return render_template('student_index.html', msg = 'Success.! Please login now.!')
    else:
        return render_template('student_index.html', err_msg = 'Error.! Please try later. ')