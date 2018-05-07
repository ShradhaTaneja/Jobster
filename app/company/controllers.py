from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from werkzeug.datastructures import CombinedMultiDict
from app.commons.modules import company

api = Blueprint('company', __name__, url_prefix = '/company')

# @api.before_request
# def before_request():
#     # if 'logged_in' not in session and request.endpoint != 'company.login':
#     if 'logged_in' not in session:
#         print session
#         print request.endpoint
#         print '@@@@@@@@@@@ through before request'
#         return render_template('company_login.html')
# @api.route('/shradha', methods=['GET'])
# def shradha():
#     return render_template('test.html')

@api.route('/', methods=['GET'])
def index(err_msg = None, msg = None):
    err_msg = None
    # err_msg = 'invalid email'
    return render_template('company_index.html', err_msg = err_msg, msg = msg)

@api.route('/home', methods=['GET'])
def home_page():
    print 'company home'
    if 'user_email' not in session:
        return render_template('company_index.html', err_msg='Please login..!')
    err_msg = None
    # err_msg = 'invalid email'
    return render_template('company_home.html', err_msg = err_msg)

# @api.route('/view/profile/<c_id>', methods = ['GET'])
# def view_profile(c_id):
#     details = company.get_details(c_id)
#     return render_template('company_profile.html', details = details)

@api.route('/job/<id>', methods = ['GET'])
def job(id):
    details = company.get_job_details()
    return render_template('job_details.html', details)


@api.route('/login', methods = ['GET', 'POST'])
def login():
    print '________________________________________', request.method
    print '______', request.form
    print session
    if 'user_email' not in session:
        if request.method == 'GET':
            return render_template('company_index.html')
        elif request.method == 'POST':
            user_email = request.form['user_email']
            password = request.form['password']
            # check for valid credentials
            valid_user = True
            print company.exists(user_email), '>>>>>>>>>>>'
            print '###########', company.correct_credentials(user_email, password)
            try:
                if company.exists(user_email) and company.correct_credentials(user_email, password):
                    print '################'
                    session['user_email'] = user_email
                    print '_________user inserted ', session
                    return render_template('company_home.html', user_email = user_email)
                else:
                    return render_template('company_index.html', err_msg= 'User not found, or Invalid credentials!')
            except Exception, e:
                return render_template('company_index.html', err_msg= 'Oops..Something went wrong!')
    else:
        return render_template('company_home.html', user_email = session['user_email'])

@api.route('/logout', methods= ['GET'])
def logout():
    session.pop('user_email', None)
    print session
    return redirect(url_for('company.index'))
    return render_template('company_index.html', msg = 'Logout Successful.!')

@api.route('/test', methods=['GET'])
def test():
    print session
    return 'test from controller - company'

@api.route('/register', methods = ['POST'])
def register():
    response = company.register(request.form)
    if company.exists(str(request.form['user_email'])):
        return render_template('company_index.html', err_msg = 'Account already created! ')

    if response['status'] == 'success':
        return render_template('company_index.html', msg = 'Success.! Please login now.!')
    else:
        print '_________ERROR:', response['message']
        return render_template('company_index.html', err_msg = 'Error.! Please try later. ')
