import app.student.models as model
import app.company.models as company_model
import hashlib

def get_all_jobs(keyword = None):
    response = {}
    try:
        if keyword is None:
            data = company_model.get_all_jobs()
        else:
            print keyword, '$$$$$$$'
            data = company_model.get_filtered_jobs( keyword = keyword)
        response['status'] = 'success'
        response['data'] = data
    except Exception as e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
    return response

def get_all_companies(keyword = None):
    response = {}
    try:
        if keyword is None:
            data = company_model.get_all_companies()
        else:
            print keyword, '$$$$$$$'
            data = company_model.get_filtered_companies( keyword = keyword)
        response['status'] = 'success'
        response['data'] = data
    except Exception as e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
    return response

def get_job(job_id):
    response = {}
    try:
        data = company_model.get_job(int(job_id))
        response['status'] = 'success'
        response['data'] = data
    except Exception as e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
    return response


def get_all_students():
    response = {}
    try:
        data = model.fetch_all_students()
        response['status'] = 'success'
        response['data'] = data
    except Exception as e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
    return response

def update_student_profile(st_id, resume = None, data = None):
    response = {}
    print 'inside update module'
    print data
    try:
        data = model.update_student_profile(st_id=st_id, resume = resume, data = data)
        print data, 'model after function'
        response['status'] = 'success'
        response['data'] = data
    except Exception as e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
        print e, '____ERRRORRRR'
    return response


def get_student_profile(email):
    response = {}
    try:
        data = model.get_student_profile(email)
        response['status'] = 'success'
        response['data'] = data
    except Exception as e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
    return response

def company_profile(cid):
    response = {}
    try:
        data = company_model.fetch_company(cid)
        response['status'] = 'success'
        response['data'] = data
    except Exception as e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
    return response

def is_following_company(c_id, st_id):
    return model.is_following_company(c_id, st_id)


def follow_company(c_id, st_id):
    response = {}
    try:
        model.follow_company(c_id, st_id)
        print 'model called'
        response['status'] = 'success'
        response['data'] = data
    except Exception, e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
    return response


def exists(email):
    return model.exists(email)

def get_id(email):
    return model.get_id(email)

def get_popular_data():
    return company_model.get_popular_data()

def get_recent_jobs():
    return company_model.get_recent_jobs()

def get_company_jobs(c_id):
    return company_model.get_company_jobs(c_id)

def get_student(rid):
    response = {}
    data = model.fetch_student(rid)
    try:
        data = model.fetch_student(rid)
        if data == {}:
            return {'status': 'failure', 'message': 'student doesn\'t exist'}
        response['status'] = 'success'
        response['data'] = data
    except Exception, e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
    return response

def register(form_data):
    response = {}
    data = {}
    data['user_name'] = str(form_data['user_name'])
    data['user_email'] = str(form_data['user_email'])
    data['user_password'] = hashlib.md5(str(form_data['password'])).hexdigest()

    try:
        status = model.register_student(data)
        response['status'] = 'success'
        response['user_email'] = data['user_email']
        response['user_name'] = data['user_name']
    except Exception as e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
    return response

def correct_credentials(user_email, user_password):
    stored_pass = model.get_pass(user_email)
    
    print '++++', hashlib.md5(str(user_password)).hexdigest()
    print '++++',stored_pass
    # print user_password, user_email

    return hashlib.md5(str(user_password)).hexdigest() == str(stored_pass)

   
def remove_student(rid):
    response = {}
    try:
        model.delete_student(rid)
        response['status'] = 'success'
    except Exception as e:
        response['status'] = 'failure'
        response['message'] = str(e)
    return response
