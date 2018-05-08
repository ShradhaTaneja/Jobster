from app.db import get_mysql_conn

def exists(email):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select st_name from student_profile where st_email = "%s" ;' % str(email)
    cursor.execute(query)

    if cursor.fetchone() is None:
        return False
    return True

def get_id(email):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select st_id from student_profile where st_email = "%s" ;' % str(email)
    cursor.execute(query)
    res = cursor.fetchone()[0]
    print res, '=========='
    conn.close()
    return res

def get_pass(email):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select st_password from student_profile where st_email = "%s" ;' % str(email)
    cursor.execute(query)
    res = cursor.fetchone()[0]
    print res, '=========='
    conn.close()
    return res
    conn.close()
    return cursor.fetchone()[0]


def fetch_all_restaurants():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select rid, rname, raddress, rcity, rstate, rating, rcontact, rwebsite, remail from restaurant;'
    cursor.execute(query)

    all_data = []

    for row in cursor.fetchall():
        row_data = {}
        row_data['rid'] = row[0]
        row_data['name'] = row[1]
        row_data['address'] = row[2]
        row_data['city'] = row[3]
        row_data['state'] = row[4]
        row_data['rating'] = row[5]
        row_data['contact'] = row[6]
        row_data['website'] = row[7]
        row_data['email'] = row[8]
        all_data.append(row_data)

    conn.close()
    return all_data


def get_student_profile(st_id):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select st_name, st_university, st_major, st_gpa, st_keywords, profile_status, degree_type, st_email from student_profile where st_id =  %d;' % (st_id)
    print query
    cursor.execute(query)
    data =  cursor.fetchone()
    print data, '******************************'
    if data is None:
        return {}
    details = {}
    details['st_name'] = data[0]
    details['st_university'] = data[1]
    details['st_major'] = data[2]
    details['st_gpa'] = data[3]
    details['st_keywords'] = data[4]
    details['profile_status'] = data[5]
    details['recent_degree'] = data[6]
    details['st_email'] = data[7]
    # details['email'] = data[8]

    conn.close()

    return details

def update_student_profile(st_id, resume = None, data = None):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    print '~~~~~~~~~~~~~~~~~~~~~~~~ update'
    print resume

    if resume:
        print 'yayyyyyyyyyyyyyyyyyyyyyy'
        print resume.read()
        update_query = 'UPDATE student_profile SET st_resume = "%s" where st_id = %d' % (resume.read(), int(st_id))
        try:
            cursor.execute(update_query)
            conn.commit()
            conn.close()
            return True
        except Exception, e:
            print '_________________________ERRORRRRRRRRRRRRRRRRRRRRRRRRRRR', e
            return False

    input_columns = data.keys()


    input_column_data = []
    input_value_data = []

    for col in input_columns:
        input_column_data.append(col.replace('user', 'st'))
        input_value_data.append(data[col])

    # this is a temp thing, the column name mapping needs to be improved
    insert_query = 'INSERT INTO `student_profile` (%s) values (%s);' % ( "`" + "`, `".join(input_column_data) + "`", "'" + "', '".join(input_value_data) + '\'')
    try:
        cursor.execute(insert_query)
        conn.commit()
        conn.close()
        return True
    except Exception, e:
        print '_________________________ERRORRRRRRRRRRRRRRRRRRRRRRRRRRR', e
        return False



def register_student(data):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    input_columns = data.keys()

    input_column_data = []
    input_value_data = []

    for col in input_columns:
        input_column_data.append(col.replace('user', 'st'))
        input_value_data.append(data[col])

    # this is a temp thing, the column name mapping needs to be improved
    insert_query = 'INSERT INTO `student_profile` (%s) values (%s);' % ( "`" + "`, `".join(input_column_data) + "`", "'" + "', '".join(input_value_data) + '\'')
    try:
        cursor.execute(insert_query)
        conn.commit()
        conn.close()
        return True
    except Exception, e:
        print '_________________________ERRORRRRRRRRRRRRRRRRRRRRRRRRRRR', e
        return False


def delete_restaurant(rid):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    delete_query = 'DELETE FROM restaurant where rid = %d ' % int(rid)

    cursor.execute(delete_query)
    conn.commit()
    conn.close()
