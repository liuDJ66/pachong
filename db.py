import pymysql

db=pymysql.connect(host="192.168.80.201",user="root",password="123456",database="gaokao")

def insert(jsondata):
    sql=f"insert into speciallist(boy_rate,degree,girl_rate,hightitle,id,level1,level1_name,level2,level2_name,level3, \
    level3_name,limit_year,name,rankstr,salaryavg,spcode,special_id,view_month,view_total,view_week) values('{jsondata.get('boy_rate')}', \
      '{jsondata.get('degree')}','{jsondata.get('girl_rate')}','{jsondata.get('hightitle')}','{jsondata.get('id')}','{jsondata.get('level1')}', \
      '{jsondata.get('level1_name')}','{jsondata.get('level2')}','{jsondata.get('level2_name')}', '{jsondata.get('level3')}',\
    '{jsondata.get('level3_name')}','{jsondata.get('limit_year')}','{jsondata.get('name')}', '{jsondata.get('rank')}',\
            '{jsondata.get('salaryavg')}','{jsondata.get('spcode')}','{jsondata.get('special_id')}', '{jsondata.get('view_month')}',\
                '{jsondata.get('view_total')}','{jsondata.get('view_week')}'\
    )"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

#专业介绍
def insertdetail(data):
    sql=f"insert into detail(special_id,code,limit_year,impress,is_what,jobrate,course,jobdetail_hy,jobdetail_dq,jobdetail_fx,learn_what,do_what \
    ) values('{data[0]}','{data[1]}','{data[2]}','{data[3]}','{data[4]}','{data[5]}','{data[6]}','{data[7]}','{data[8]}','{data[9]}','{data[10]}','{data[11]}'\
    )"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

#就业率
def insertjyl(data):
    sql=f"insert into jyl(special_id,id,rate,year) values('{data[0]}','{data[1]}','{data[2]}','{data[3]}')"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

#就业情况  1 行业 2地区 3工作方向
def insertjyqk(data):
    sql=f"insert into jyqk(area,detail_job,detail_pos,id,name,rate,sort,special_id,type) values('{data[0]}','{data[1]}','{data[2]}','{data[3]}','{data[4]}','{data[5]}','{data[6]}','{data[7]}','{data[8]}')"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

#第一印象
def insertimpress(data):
    sql=f"insert into impress(id,key_word,special_id) values('{data[0]}','{data[1]}','{data[2]}')"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

def QuerySpid():
    sql=f"select special_id from speciallist where special_id not in ( select special_id from detail )"
    cursor = db.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    return data

def Query(sql):
    cursor = db.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    return data