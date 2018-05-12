from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from werkzeug.datastructures import CombinedMultiDict
from app.commons.modules import company
from app.db import get_mysql_conn
import models as company
from app.commons.modules import company as company_module

from app.commons.modules import student as student_module

api = Blueprint('company', __name__, url_prefix = '/company')


def get_id(email):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select c_id from company_details where c_email = "%s" ;' % str(email)
    cursor.execute(query)
    res = cursor.fetchone()[0]
    # print res, '=========='
    conn.close()
    return int(res)


def current_jobs(c_id):
    all_data = company.get_all_company_jobs(c_id)
    return all_data

@api.route('/', methods=['GET'])
def index(err_msg = None, msg = None):
    err_msg = None
    # err_msg = 'invalid email'
    return render_template('company_index.html', err_msg = err_msg, msg = msg)

@api.route('/home', methods=['GET'])
def home():
    print 'company home'
    if 'user_email' not in session:
        return render_template('company_index.html', err_msg='Please login..!')
    err_msg = None
    all_jobs = current_jobs(get_id(session['user_email']))
    print all_jobs, '<<<<<<<<<<<<<<<<<<<<<<<<<<<'
    # err_msg = 'invalid email'
    return render_template('company_home.html', err_msg = err_msg, all_jobs = all_jobs)

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
    err_msg = None
    
    if 'user_email' not in session:
        if request.method == 'GET':
            return render_template('company_index.html')
        elif request.method == 'POST':
            # popular_data = student.get_popular_data()
            # recent_jobs = student.get_recent_jobs()
            user_email = request.form['user_email']
            password = request.form['password']
            # check for valid credentials
            valid_user = True
            # print student.exists(user_email), '>>>>>>>>>>>'
            # print '###########', student.correct_credentials(user_email, password)

            # print student.exists(user_email), '___user exists'
            # print student.correct_credentials(user_email, password), 'correct pwd'
            if company.exists(user_email) and company_module.correct_credentials(user_email, password):
                # print '################'
                session['user_email'] = user_email
                print 'logged in ..................................................'
                # print '_________user inserted ', session
                # print '++++++++++++ ', recent_jobs
                # return redirect(url_for(company.home))
                # return render_template('company_home.html', user_email = user_email, popular_data = popular_data, recent_jobs = recent_jobs)
                err_msg = None
                all_jobs = current_jobs(get_id(session['user_email']))
                print all_jobs, '<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                # err_msg = 'invalid email'
                return render_template('company_home.html', err_msg = err_msg, all_jobs = all_jobs)
            else:
                return render_template('company_home.html', err_msg = 'invalid credentials')
    else:
        # popular_data = student.get_popular_data()
        # recent_jobs = student.get_recent_jobs()
        return render_template('company_home.html', err_msg = err_msg)

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
            print '###########', company_module.correct_credentials(user_email, password)
            try:
                if company.exists(user_email) and company_module.correct_credentials(user_email, password):
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


@api.route('/student_view', methods = ['GET'])
def view_student():

    data = student_module.get_student_profile(int(request.args['st_id']))
    return render_template('company_view_student.html', data = data['data'])

@api.route('/job', methods = ['GET'])
def job_details_fn():
    data = company.get_job(int(request.args['job_id']))
    print data
    return render_template('job_view_company.html', data=data[0])


@api.route('/applications', methods = ['GET'])
def applications():
    all_data = []

    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select st_id,st_name, job_id,job_title,  c_id, st_university, st_major from job_applications natural join company_details natural join student_profile natural join job_announcements  where c_id = %d;' % int(get_id(str(session['user_email'])))
    cursor.execute(query)
    res = cursor.fetchall()

    for r in res:
        data = {}
        data['st_id'] = r[0]
        data['st_name'] = r[1]
        data['job_id'] = r[2]
        data['job_title'] = r[3]
        data['st_university'] = r[4]
        data['st_major'] = r[5]
        # data[''] = r[]
        all_data.append(data)

    return render_template('applications.html', data = all_data)
   