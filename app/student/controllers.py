from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from werkzeug.datastructures import CombinedMultiDict
from app.commons.modules import student 
from app.db import get_mysql_conn
import datetime
import time
import models as student_model



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



@api.route('/job_search', methods = ['GET', 'POST'])
def job_search():
    all_jobs = student.get_all_jobs()
    if request.method == 'POST':
        print request.form['keyword'], '__________________________'
        all_jobs = student.get_all_jobs(keyword = request.form['keyword'])
        print '____________resulttttt', all_jobs
    return render_template('student_job_search.html', all_jobs = all_jobs['data'])


@api.route('/job_view', methods = ['GET'])
def job_view():
    job_id = request.args['job_id']
    data = student.get_job(job_id)
    st_id = student.get_id(session['user_email'])

    conn = get_mysql_conn()
    cursor = conn.cursor()
    print '__________previous insert'

    query = 'select * from job_applications where st_id = %d and job_id = %d' % (int(st_id), int(job_id))
    print query

    cursor.execute(query)
    if cursor.fetchone() is not None:
        print '+++++++++ already applied.. '
        conn.close()
        return render_template('job_announcement_view.html', data = data['data'][0], user_email = session['user_email'], job_id = job_id, applied = True)


    
    return render_template('job_announcement_view.html', data = data['data'][0], user_email = session['user_email'], job_id = job_id)



@api.route('/profile_edit', methods = ['GET', 'POST'])
def profile_edit():
    s_id = student.get_id(session['user_email'])
    if request.method == 'GET':
        data = student.get_student_profile(int(s_id))
        print data['data']
        return render_template('student_profile_edit.html', data = data['data'])
    else:
        resume = None
        # print '__________________PIOST aa gyaaa'
        print request.form, 'in the form'
        if request.files:
            resume = request.files['st_resume']
        # print resume, '<<<<<<<<<<<<<<'
        # resume_data = 
        # update db
        print 'before update'
        update_status = student.update_student_profile(int(s_id), resume = resume, data = request.form)
        print 'after calling update'
        data = student.get_student_profile(int(s_id))
        return render_template('student_profile_edit.html', msg = 'Updated.!', data = data['data'])


@api.route('/follow_company', methods = ['GET'])
def follow_company():
    # return request.args['c_id']
    print 'in controller'
    c_id = int(request.args['c_id'])
    st_id = student.get_id(session['user_email'])
    data = student.company_profile(int(c_id))
    recent_jobs = student.get_company_jobs(int(c_id))
    student.follow_company(c_id, st_id)
    allow_follow = True

    print 'after in controller'
    following = student.is_following_company(int(c_id), int(st_id))
    if following:
        allow_follow = False    
    return render_template('company_profile.html', data = data['data'], recent_jobs = recent_jobs, allow_follow = allow_follow, c_id = c_id)


@api.route('/view_company', methods = ['GET'])
def view_company():
    c_id = request.args['c_id']
    # c_id = 2
    data = student.company_profile(int(c_id))
    recent_jobs = student.get_company_jobs(int(c_id))
    st_id = student.get_id(session['user_email'])
    print st_id
    allow_follow = True

    print 'after in controller'
    following = student.is_following_company(int(c_id), int(st_id))
    if following:
        allow_follow = False    
    return render_template('company_profile.html', data = data['data'], recent_jobs = recent_jobs, allow_follow = allow_follow, c_id = c_id)


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

            print student.exists(user_email), '___user exists'
            print student.correct_credentials(user_email, password), 'correct pwd'
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





## TODO : correct these functions - currently directly contacting the model, should go via modules

@api.route('/apply_job', methods = ['GET', 'POST'])
def apply_job():
    job_id = int(request.args['job_id'])
    st_id = student.get_id(session['user_email'])
    applied_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    applied = False

    # if request.method == 'GET':
    
    print '___________________________________________', request.method
    data = student.get_job(job_id)
    print data
    conn = get_mysql_conn()
    cursor = conn.cursor()
    print '__________previous insert'

    query = 'select * from job_applications where st_id = %d and job_id = %d' % (int(st_id), int(job_id))
    print query

    cursor.execute(query)
    if cursor.fetchone() is not None:
        print '+++++++++ already applied.. '
        conn.close()
        return render_template('job_announcement_view.html', data = data['data'][0], user_email = session['user_email'], job_id = job_id, applied = True)


    # else:
    conn = get_mysql_conn()
    cursor = conn.cursor()
    print '__________previous insert'

    query = 'Insert into job_applications (st_id, job_id, applied_at) values (%d,%d, "%s");' % (int(st_id), int(job_id), applied_at)
    print query
    
    try:
        cursor.execute(query)
        conn.commit()
        print '___________after insert'
        conn.close()
        print 'conn closed'
        data = student.get_job(job_id)
        print data
        applied = True
        return render_template('job_announcement_view.html', data = data['data'][0], user_email = session['user_email'], job_id = job_id, applied = applied)

    except Exception, e:
        conn.close()
        print '___________________thukaa ', e
        data = student.get_job(job_id)
        print data
        return render_template('job_announcement_view.html', data = data['data'][0], user_email = session['user_email'], job_id = job_id, applied = applied)
        return False



@api.route('/applied_jobs', methods = ['GET'])
def applied_jobs():
    st_id = student.get_id(session['user_email'])
    conn = get_mysql_conn()
    cursor = conn.cursor()
    print '__________wohoooooooooo'

    query = 'select c_name, job_title, job_state, job_city, c_id, job_id from job_announcements natural join company_details natural join job_applications where st_id = %d order by applied_at desc;' % int(st_id)

    print query



    cursor.execute(query)

    all_data = []

    for row in cursor.fetchall():
        row_data = {}
        row_data['c_name'] = row[0]
        row_data['job_title'] = row[1]
        row_data['job_state'] = row[2]
        row_data['job_city'] = row[3]
        row_data['c_id'] = row[4]
        row_data['job_id'] = row[5]
        # row_data['contact'] = row[6]
        # row_data['website'] = row[7]
        # row_data['email'] = row[8]
        all_data.append(row_data)

    conn.close()
    return render_template('student_applied_jobs.html', user_email = session['user_email'], data = all_data)



@api.route('/view_student', methods = ['GET', 'POST'])
def student_profile():
    other_id = int(request.args['other_id'])
    st_id = int(student.get_id(session['user_email']))
    send_invite = True

    # get friend data
    data = student_model.get_student_profile(other_id)
    data.pop('st_gpa', None)
    data.pop('st_email', None)
    data.pop('profile_status', None)

    print data, '_________________'


    if other_id == st_id:
        return render_template('student_profile.html', data = data, send_invite = False)

    send_invite, status = are_friends(st_id, other_id)
    print send_invite, status, '\\\\\\\\\\\\\\\\\\\\\\\\\\'

    if not send_invite:
        return render_template('student_profile.html', data = data, send_invite = False, other_id = other_id, status = status)

    # conn.close()
    return render_template('student_profile.html', data = data, send_invite = True, other_id = other_id)



@api.route('/add_friend', methods = ['GET', 'POST'])
def add_friend():
    fr_id = int(request.args['fr_id'])
    st_id = int(student.get_id(session['user_email']))
    requested_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = student_model.get_student_profile(fr_id)
    data.pop('st_gpa', None)
    data.pop('st_email', None)
    data.pop('profile_status', None)

    send_invite = True

    conn = get_mysql_conn()
    cursor = conn.cursor()
    
    print '__________previous insert'

    query = 'SELECT st_name, st_major , st_university FROM ( (SELECT fr_id AS friend FROM friends WHERE st_id = %d and fr_id = %d AND status = "accepted") \
     UNION (SELECT st_id AS friend FROM friends WHERE fr_id = %d AND st_id = %d and status = "accepted") ) AS filter INNER JOIN student_profile ON student_profile.st_id = filter.friend;'  \
     % (st_id, fr_id, fr_id, st_id)
    cursor.execute(query)

    print query, '<<<<<<<AASDFASDF'


    if cursor.fetchone() is not None:
        print '+++++++++ already friends.. '
        cursor.execute('select status from friends where (st_id = %d and fr_id = %d) OR (st_id = %d and fr_id = %d)' % (st_id, fr_id, fr_id, st_id))
        res = cursor.fetchone()[0]
        print res
        if res == 'accepted':
            res = 'friends'
        conn.close()
        return render_template('student_profile.html', data = data, user_email = session['user_email'], send_invite = False, status = res)


    # else:
    conn = get_mysql_conn()
    cursor = conn.cursor()
    print '__________previous insert'

    query = 'Insert into friends (st_id, fr_id, requested_at) values (%d,%d, "%s");' % (int(st_id), int(fr_id), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print query
    
    try:
        cursor.execute(query)
        conn.commit()
        print '___________after insert'
        conn.close()
        print 'conn closed'
        data = student_model.get_student_profile(fr_id)
        print data
        send_invite = False
        status = 'requested'
        return render_template('student_profile.html', data = data, user_email = session['user_email'], send_invite = False, status = 'pending')

    except Exception, e:
        # conn.close()
        print '___________________thukaa ', e
        data = student_model.get_student_profile(fr_id)
        print data
        return render_template('student_profile.html', data = data, user_email = session['user_email'], send_invite = False, status = 'pending')
        return False



@api.route('/friends_accepted', methods = ['GET', 'POST'])
def friends():
    st_id = int(student.get_id(session['user_email']))

    query = 'SELECT st_name, st_major, st_university, st_id FROM ( (SELECT fr_id AS friend FROM friends WHERE st_id = %d AND status = "accepted") \
     UNION (SELECT st_id AS friend FROM friends WHERE st_id = %d and status = "accepted") ) AS filter INNER JOIN student_profile ON student_profile.st_id = filter.friend and student_profile.st_id != %d;'  \
     % (st_id, st_id, st_id)
     # print query
    print query

    conn = get_mysql_conn()
    cursor = conn.cursor()

    cursor.execute(query)
    res = cursor.fetchall()

    all_data = []

    for r in res:
        row = {}
        row['st_name'] = r[0]
        row['st_major'] = r[1]
        row['st_university'] = r[2]
        row['st_id'] = int(r[3])
        all_data.append(row)

    return render_template('student_friends.html', data = all_data)



def are_friends(st_id, fr_id):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    send_invite = True
    status = ''
    query = 'SELECT st_name, st_major , st_university FROM ( (SELECT fr_id AS friend FROM friends WHERE st_id = %d and fr_id = %d AND status = "accepted") \
     UNION (SELECT st_id AS friend FROM friends WHERE fr_id = %d AND st_id = %d and status = "accepted") ) AS filter INNER JOIN student_profile ON student_profile.st_id = filter.friend;'  \
     % (st_id, fr_id, fr_id, st_id)
    res = cursor.execute(query)
    print query, '_________are friends'
    print res, type(res)



    if res is not None:
        send_invite = False
        print '+++++++++ already friends.. '
        try:
            cursor.execute('select status from friends where (st_id = %d and fr_id = %d) OR (st_id = %d and fr_id = %d)' % (st_id, fr_id, fr_id, st_id))
            status = cursor.fetchone()[0]
            print status
            if status == 'accepted':
                status = 'friends'
        except:
            send_invite = True
        conn.close()


    return send_invite, status
    


@api.route('/friends_add_new', methods = ['GET', 'POST'])
def friends_add_new():
    st_id = int(student.get_id(session['user_email']))

    query = 'SELECT st_name, st_major, st_university, st_id FROM student_profile'

    conn = get_mysql_conn()
    cursor = conn.cursor()

    cursor.execute(query)
    res = cursor.fetchall()

    all_data = []

    for r in res:
        row = {}
        row['st_name'] = r[0]
        row['st_major'] = r[1]
        row['st_university'] = r[2]
        row['st_id'] = int(r[3])
        all_data.append(row)

    return render_template('student_friends_add_new.html', data = all_data)



@api.route('/friends_messages_all', methods = ['GET'])
def friends_messages_all():
    st_id = int(student.get_id(session['user_email']))

    friends_query = "(SELECT fr_id AS friend FROM friends WHERE st_id = %d AND status = 'accepted') UNION (SELECT st_id AS friend FROM friends WHERE fr_id = %d AND status = 'accepted');" \
     % (st_id, st_id)

    conn = get_mysql_conn()
    cursor = conn.cursor()  
    res = cursor.execute(friends_query)
    res_data = cursor.fetchall()
    all_friends = []

    all_recent_msgs = []

    for one in res_data:
        all_friends.append(int(one[0]))

    print all_friends, '_________________________'

    for fr_id in all_friends:
        recent_msg_query = 'select * from (select max(sent_at) as max_sent_at from messages where (st_id = %d and fr_id = %d) or (st_id = %d and fr_id = %d)) as max inner join (select st_id, fr_id, message, sent_at from messages where (st_id = %d and fr_id = %d) or (st_id = %d and fr_id = %d)) as f on f.sent_at = max.max_sent_at;'  % (st_id, fr_id, fr_id, st_id, st_id, fr_id, fr_id, st_id)
        cursor.execute(recent_msg_query)
        res = cursor.fetchone()
        
        print recent_msg_query
        try:
            data = {}
            print res, '???????????????????????????'
            data['date'] = res[0].strftime("%Y-%m-%d %H:%M:%S")
            if res[1] == st_id:
                data['sender'] = st_id
                data['receiver'] = fr_id
            else:
                data['sender'] = fr_id
                data['receiver'] = st_id

            data['message'] = res[3]
            data['fr_id'] = fr_id
            all_recent_msgs.append(data)
        except Exception, e:
            continue
        
    # return str(all_recent_msgs)
    return render_template('student_friends_messages_all.html', data = all_recent_msgs)
        # data[''] = res[]
        # data[''] = res[]
        # data[''] = res[]


@api.route('friends_messages_single', methods = ['GET'])
def friends_messages():
    st_id = int(student.get_id(session['user_email']))
    fr_id = int(request.args['fr_id'])
    conn = get_mysql_conn()
    cursor = conn.cursor()  
    res = cursor.execute(friends_query)
    res_data = cursor.fetchall()
    return 'in friends msgs'
    all_recent_msgs = []

    # for fr_id in all_friends:
    recent_msg_query = 'select * from messages where (st_id = %d and fr_id = %d) or (st_id = %d and fr_id = %d) order by sent_at desc;'  % (st_id, fr_id, fr_id, st_id)
    cursor.execute(recent_msg_query)
    res = cursor.fetchall()
    
    print recent_msg_query

    for m in res:
        data = {}
        data['date'] = m[3].strftime("%Y-%m-%d %H:%M:%S")
        # data['date'] = res[0].strftime("%Y-%m-%d %H:%M:%S")
        if res[1] == st_id:
            data['sender'] = st_id
            data['receiver'] = fr_id
        else:
            data['sender'] = fr_id
            data['receiver'] = st_id

        data['message'] = res[5]
        data['fr_id'] = fr_id
        all_recent_msgs.append(data)

    # return str(all_recent_msgs)
    return render_template('student_friends_messages.html', data = all_recent_msgs)
   


@api.route('/company_search', methods = ['GET', 'POST'])
def company_search():
    all_companies = student.get_all_companies()
    if request.method == 'POST':
        print request.form['keyword'], '__________________________'
        all_companies = student.get_all_companies(keyword = request.form['keyword'])
        # print '____________resulttttt', all_jobs
    return render_template('student_company_search.html', all_companies = all_companies['data'])


@api.route('/company_following', methods = ['GET'])
def company_following():
    st_id = int(student.get_id(session['user_email']))
    # fr_id = int(request.args['fr_id'])
    conn = get_mysql_conn()
    cursor = conn.cursor()  
    # res = cursor.execute(friends_query)
    # res_data = cursor.fetchall()
    # return 'in friends msgs'
    # all_recent_msgs = []

    # for fr_id in all_friends:
    recent_msg_query = 'select c_name, c_id, c_headquarter_location, c_industry from company_details natural join follow where st_id = %d'  % (st_id)
    cursor.execute(recent_msg_query)
    res = cursor.fetchall()
    all_data = []

    for row in res:
        row_data = {}
        row_data['c_name'] = row[0]
        row_data['c_headquarter_location'] = row[2]
        row_data['c_industry'] = row[3]
        # row_data['job_city'] = row[3]
        row_data['c_id'] = row[1]
        # row_data['posted_date'] = row[5]
        # row_data['job_id'] = row[6]
        # row_data['website'] = row[7]
        # row_data['email'] = row[8]
        all_data.append(row_data)


    # return str(all_recent_msgs)
    return render_template('student_follow_companies.html', data = all_data)
   


# 'SELECT st_name, st_major , st_university FROM ( (SELECT fr_id AS friend FROM friends WHERE st_id = 6 AND status = 'accepted') UNION (SELECT st_id AS friend FROM friends WHERE fr_id = 6 AND status = 'accepted') ) AS filter INNER JOIN student_profile ON student_profile.st_id = filter.friend;'