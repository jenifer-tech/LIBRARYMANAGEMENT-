import pymysql
conn=pymysql.connect(
                    host='sql12.freemysqlhosting.net',
                    database='sql12375682',
                    user='sql12375682',
                    password='nL9hwqHpV7',
                    cursorclass=pymysql.cursors.DictCursor
                    )  
cursor=conn.cursor()
query="""CREATE TABLE IF NOT EXISTS book(b_id INTEGER AUTO_INCREMENT PRIMARY KEY,
                                          b_author VARCHAR(25) NOT NULL,
                                          b_name VARCHAR(20) NOT NULL,
                                          b_types VARCHAR(20) NOT NULL
                                          
)"""

qu="""CREATE TABLE IF NOT EXISTS user(u_id INTEGER AUTO_INCREMENT PRIMARY KEY,
                                           u_name VARCHAR(50) NOT NULL,
                                           u_mail VARCHAR(50),
                                           u_dept VARCHAR(25)                                     
                                          
)"""
que="""CREATE TABLE IF NOT EXISTS transaction(t_id INTEGER AUTO_INCREMENT PRIMARY KEY,
                                               b_id INTEGER NOT NULL,
                                               u_id INTEGER NOT NULL,                    
                                               FOREIGN KEY(b_id) REFERENCES book(b_id),
                                               FOREIGN KEY(u_id) REFERENCES user(u_id)
                                          
)"""

que="""ALTER TABLE book ADD status VARCHAR(50) NOT NULL """   

cursor.execute(query)                                          
cursor.execute(qu)
cursor.execute(que)
conn.close()


