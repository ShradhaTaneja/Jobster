from app.db import get_mysql_conn

def exists(email):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select c_id from company_details where c_email = "%s" or c_name = "%s" ;' % (str(email), str(cname))
    cursor.execute(query)

    if cursor.fetchone() is None:
        return False
    return True

def get_pass(email):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select st_password from student_profile where st_email = "%s" ;' % str(email)
    cursor.execute(query)
    print cursor.fetchone()[0], '=========='
    conn.close()
    return cursor.fetchone()[0]
    if cursor.fetchone() is None:
        return False
    return True


def fetch_all_companys():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select rid, rname, raddress, rcity, rstate, rating, rcontact, rwebsite, remail from company;'
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


def fetch_company(rid):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select rid, rname, raddress, rcity, rstate, rating, rcontact, rwebsite, remail from company where rid =  %s;' % (rid)
    cursor.execute(query)
    data =  cursor.fetchone()
    if data is None:
        return {}
    details = {}
    details['rid'] = data[0]
    details['name'] = data[1]
    details['address'] = data[2]
    details['city'] = data[3]
    details['state'] = data[4]
    details['rating'] = data[5]
    details['contact'] = data[6]
    details['website'] = data[7]
    details['email'] = data[8]

    conn.close()
    return details



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


def delete_company(rid):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    delete_query = 'DELETE FROM company where rid = %d ' % int(rid)

    cursor.execute(delete_query)
    conn.commit()
    conn.close()
