import app.student.models as model

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

def exists(rid):
    return model.exists(rid)

def get_student(rid):
    response = {}
    data = model.fetch_student(rid)
    try:
        data = model.fetch_student(rid)
        if data == {}:
            return {'status': 'failure', 'message': 'student doesn\'t exist'}
        response['status'] = 'success'
        response['data'] = data
    except Exception as e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
    return response

def add_student(data):
    response = {}
    try:
        rid = model.insert_student(data)
        response['status'] = 'success'
        response['data'] = {'rid' : rid}
    except Exception as e:
        response['status'] = 'failure'
        response['data'] = None
        response['message'] = str(e)
    return response




def remove_student(rid):
    response = {}
    try:
        model.delete_student(rid)
        response['status'] = 'success'
    except Exception as e:
        response['status'] = 'failure'
        response['message'] = str(e)
    return response
