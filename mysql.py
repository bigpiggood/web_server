import pymysql
# import pymysql —> pymysql.connect(데이터베이스 연결을 위한 config ) —> cusor() —> excute(쿼리문) —> fetchall()

# 암호화 알고리즘. 256을 제일 많이 사용한다.
from passlib.hash import pbkdf2_sha256 


# 원문 비밀번호를, 암호화 하는 함수
def hash_password(original_password):
    salt = 'eungok'
    password = original_password + salt
    password = pbkdf2_sha256.hash(password)
    return password

def check_password(input_password, hashed_password):
    salt = 'eungok'
    password = input_password + salt
    result = pbkdf2_sha256.verify(password, hashed_password)
    print(result)    
    return result



class Mysql:
    def __init__(self, host='localhost', user='root', db='os', password='', charset='utf8'):
        self.host = host
        self.user = user
        self.db = db
        self.password = password
        self.charset = charset


    def get_user(self):    
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        
        sql = "select * from user"
        curs.execute(sql)
        
        rows = curs.fetchall()                
        # db.commit()
        db.close()
        return rows  
        
    def get_data(self):    
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        
        sql = "select * from list"
        curs.execute(sql)
        
        rows = curs.fetchall()                
        # db.commit()
        db.close()
        return rows      


    def insert_list(self, title, desc, author):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()    
            
        sql = '''insert into list (`title`, `desc`, `author`) values(%s,%s,%s)'''
        result = curs.execute(sql,(title, desc, author))
        print(result)
        db.commit()
        db.close()

        return result
    
    def insert_user(self, username, email, phone, password):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()    
            
        sql = '''insert into user (username, email, phone, password) values(%s,%s,%s,%s)'''
        password_1 = hash_password(password)   
        result = curs.execute(sql,(username, email, phone, password_1))
        print(result)
        db.commit()
        db.close()

        return result


    def verify_password(self, password, password_1):
        # db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        # curs = db.cursor()

        # sql = f'SELECT * FROM user WHERE email = %s'
        # curs.execute(sql)

        # rows = curs.fetchall()  
        # print(rows)              
        # # db.commit()
        # db.close()
        # if len(rows) != 0:
        #     hash_password = rows[0][4]
        #     result = check_password(password, hash_password)
        #     if result:
        #         print("Welcome to my World")        
        #     else:
        #         print("MissMatch Password")    
        # else:
        #     print("User is not founded")

        result = check_password(password, password_1)
        return result

    def del_user(self, email):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()        
        sql = f"delete from user where email=%s"
        result = curs.execute(sql,email)
        print(result)    
        db.commit()
        db.close()
    


# mysql = Mysql(password='java')    
# rows = mysql.get_user()
# print(rows)

# mysql.insert_user("garykim", "2@naver.com", "010-8496-9889", "1234")

# mysql.del_user("1@naver.com")

# password = hash_password("1234")
# print(password)

# result = check_password("1234", "$pbkdf2-sha256$29000$CeE8R6hVSimFcI5xDsHYuw$sJe/Vyi5Q.giRgFoWYIyw0itQez7WGeVX5A3CGg1l6s")

# mysql.verify_password(f"1@naver.com", "1234")
# mysql.verify_password("2@naver.com", "1234")