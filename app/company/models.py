# company model
from app.db import get_mysql_conn




def exists(email):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select c_id from company_details where c_email = "%s";' % (str(email))
    cursor.execute(query)

    if cursor.fetchone() is None:
        return False
    return True

def get_pass(email):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select c_password from company_details where c_email = "%s" ;' % str(email)
    cursor.execute(query)
    res = cursor.fetchone()[0]
    print res, '========== @@@@@@@@@@@@@'
    conn.close()
    return res
    if res is None:
        return False
    return True

def get_popular_data():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    job_query = 'select job_title, job_id from job_announcements natural join job_applications \
        natural join company_details group by job_id order by count(*) desc limit 4;'
    cursor.execute(job_query)

    all_data = {}
    all_data['jobs'] = []
    all_data['company'] = []

    for row in cursor.fetchall():
        row_data = {}
        row_data['job_id'] = row[1]
        row_data['job_title'] = row[0]
        # row_data['address'] = row[2]
        # row_data['city'] = row[3]
        # row_data['state'] = row[4]
        # row_data['rating'] = row[5]
        # row_data['contact'] = row[6]
        # row_data['website'] = row[7]
        # row_data['email'] = row[8]
        all_data['jobs'].append(row_data)

    company_query = 'select c_id, c_name from job_announcements natural join job_applications \
        natural join company_details group by c_id order by count(*) desc limit 4;'
    cursor.execute(company_query)

    for row in cursor.fetchall():
        row_data = {}
        row_data['c_name'] = row[1]
        row_data['c_id'] = row[0]
        # row_data['address'] = row[2]
        # row_data['city'] = row[3]
        # row_data['state'] = row[4]
        # row_data['rating'] = row[5]
        # row_data['contact'] = row[6]
        # row_data['website'] = row[7]
        # row_data['email'] = row[8]
        all_data['company'].append(row_data)


    conn.close()
    return all_data


def get_job(job_id):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    # if keyword is None:
    query = 'select c_name, job_title, job_state, job_city, c_id, posted_date, job_id, job_salary, job_deadline, degree_type, \
     major, job_description from job_announcements natural join company_details where job_id = %d;' % job_id
    # else:
    #     query = " \
    #     select c_name, job_title, job_state, job_city, c_id, posted_date, job_id \
    #     from job_announcements natural join company_details \
    #     where c_name like '%%%s%%' or job_title like '%%%s%%' or job_state like '\%\%%s\%\%' or job_city like '\%\%%s\%\%' order by posted_date desc" % (keyword, keyword, keyword, keyword)
    print query, '++'
    cursor.execute(query)

    all_data = []

    for row in cursor.fetchall():
        row_data = {}
        row_data['c_name'] = row[0]
        row_data['job_title'] = row[1]
        row_data['job_state'] = row[2]
        row_data['job_city'] = row[3]
        row_data['c_id'] = row[4]
        row_data['posted_date'] = row[5]
        row_data['job_id'] = row[6]
        row_data['job_salary'] = row[7]
        row_data['job_deadline'] = row[8]
        row_data['degree_type'] = row[9]
        row_data['major'] = row[10]
        row_data['job_description'] = row[11]
        # row_data['job_deadline'] = row[8]
        # row_data['job_deadline'] = row[8]

        all_data.append(row_data)

    conn.close()
    return all_data


def get_filtered_jobs(keyword):
    print keyword, '<<<<<<<<<<<<<<'
    conn = get_mysql_conn()
    cursor = conn.cursor()
    # if keyword is None:
    #     query = 'select c_name, job_title, job_state, job_city, c_id, posted_date, job_id from job_announcements natural join company_details order by posted_date DESC;'
    # else:
    key_str = '"%%' + keyword + '%%"'
    query = " \
    select c_name, job_title, job_state, job_city, c_id, posted_date, job_id \
    from job_announcements natural join company_details \
    where c_name like %s or job_title like %s or job_state like %s or job_city like %s " % (key_str, key_str, key_str, key_str)
    print query, '++'
    cursor.execute(query)

    all_data = []

    for row in cursor.fetchall():
        row_data = {}
        row_data['c_name'] = row[0]
        row_data['job_title'] = row[1]
        row_data['job_state'] = row[2]
        row_data['job_city'] = row[3]
        row_data['c_id'] = row[4]
        row_data['posted_date'] = row[5]
        row_data['job_id'] = row[6]
        # row_data['website'] = row[7]
        # row_data['email'] = row[8]
        all_data.append(row_data)

    conn.close()
    return all_data


def get_all_jobs(keyword = None):
    print keyword, '<<<<<<<<<<<<<<'
    conn = get_mysql_conn()
    cursor = conn.cursor()
    # if keyword is None:
    query = 'select c_name, job_title, job_state, job_city, c_id, posted_date, job_id from job_announcements natural join company_details order by posted_date DESC;'
    # else:
    #     query = " \
    #     select c_name, job_title, job_state, job_city, c_id, posted_date, job_id \
    #     from job_announcements natural join company_details \
    #     where c_name like '%%%s%%' or job_title like '%%%s%%' or job_state like '\%\%%s\%\%' or job_city like '\%\%%s\%\%' order by posted_date desc" % (keyword, keyword, keyword, keyword)
    print query, '++'
    cursor.execute(query)

    all_data = []

    for row in cursor.fetchall():
        row_data = {}
        row_data['c_name'] = row[0]
        row_data['job_title'] = row[1]
        row_data['job_state'] = row[2]
        row_data['job_city'] = row[3]
        row_data['c_id'] = row[4]
        row_data['posted_date'] = row[5]
        row_data['job_id'] = row[6]
        # row_data['website'] = row[7]
        # row_data['email'] = row[8]
        all_data.append(row_data)

    conn.close()
    return all_data

def get_recent_jobs():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select c_name, job_title, job_state, job_city, c_id, job_id from job_announcements natural join company_details order by posted_date desc limit 6;'
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
    return all_data


def fetch_company(c_id):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    query = 'select c_name, c_headquarter_location , c_industry from company_details where c_id =  %d;' % int(c_id)
    cursor.execute(query)
    data =  cursor.fetchone()
    if data is None:
        return {}
    details = {}
    details['c_name'] = data[0]
    details['c_headquarter_location'] = data[1]
    details['c_industry'] = data[2]
    # details['city'] = data[3]
    # details['state'] = data[4]
    # details['rating'] = data[5]
    # details['contact'] = data[6]
    # details['website'] = data[7]
    # details['email'] = data[8]

    conn.close()
    return details



def register(data):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    input_columns = data.keys()

    input_column_data = []
    input_value_data = []

    for col in input_columns:
        input_column_data.append(col.replace('user', 'c'))
        input_value_data.append(data[col])

    # this is a temp thing, the column name mapping needs to be improved
    insert_query = 'INSERT INTO `company_details` (%s) values (%s);' % ( "`" + "`, `".join(input_column_data) + "`", "'" + "', '".join(input_value_data) + '\'')
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
