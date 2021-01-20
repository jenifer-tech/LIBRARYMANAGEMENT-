from flask import Flask,request,jsonify  
import json
import pymysql
import re



app=Flask(__name__)

def db_connection():    

    conn=None

    try:
        conn=pymysql.connect(   host='sql12.freemysqlhosting.net',
                                database='sql12375682',
                                user='sql12375682',
                                password='nL9hwqHpV7',
                                cursorclass=pymysql.cursors.DictCursor
                            )
    except pymysql.Error as e :
        print(e)    
    return conn   


def exe_query(conn,cursor):
    conn=db_connection()
    cursor=conn.cursor()  
    return conn,cursor   

def validation(new_author,new_bname,new_btypes):
    if not new_author or not new_bname or not new_btypes :
        return "Please enter all values"
    if not new_author.isalpha():
        return "Book author allowed only strings"
    elif not new_bname.isalpha():
        return "Book name allowed only strings"
    elif not new_btypes.isalpha():
        return "Book types allowed only strings"
def validate(new_uname,new_email,new_udpt):
    if  not new_uname or not new_email or not new_udpt:
        return "Please enter all values"        
    elif not new_uname.isalpha():
        return "User name allowed only strings"    
    elif not re.match  (r'[^@]+@[^@]+\.[^@]+',new_email):   
        return "Invalid Email address " 
    elif not  new_udpt.isalpha():
        return "User department ony string"
def check_lword(q):
    word =q.split()
    y=word.index(word[len(word) -1])  
    return y 
def check_word(q):
    target="VALUES"        
    word=q.split()
    for i,w in enumerate(word):
        if w==target:
            return  word.index(word[i])

def insert_val(q,qParam): 
    
    y = ""
    c="%s%s" % (q,y)     
    if qParam!=None:     
        y = " '%s' " % (qParam) 
        if check_word(q) != check_lword(q):   
            y="," +y
        else:
            y="(" + y 
    c="%s%s" % (q,y)
    return c            
   
@app.route("/addbook",methods=["POST","GET","PUT","DELETE"])  
def book():
    a,b=exe_query('con','cursor')
    new_id=request.form.get('b_id')
    new_author=request.form.get('b_author')
    new_bname=request.form.get('b_name')   
    new_btypes=request.form.get('b_types') 
    new_status=request.form.get('status')
    if request.method=="POST":                      
        error_msg=validation(new_author,new_bname,new_btypes)
        if error_msg:
            return jsonify({"message":error_msg}),400   
               
        q = "INSERT INTO book VALUES"         
        q = insert_val(q,new_id) 
        q = insert_val(q,new_author)
        q = insert_val(q,new_bname) 
        q = insert_val(q,new_btypes) 
        q = insert_val(q,new_status)    

        if check_word(q) != check_lword(q) :
            q=q + ")"
            #return q            
            res=b.execute(q)
            a.commit()
            return jsonify({"message":"Book  added successfully!"}),200 

    if request.method=="GET":
        b.execute("SELECT * FROM book") 
        books=b.fetchall()
        if books:  
            return jsonify(books),200
        else:
            return "Something wrong",404 

    if request.method=="PUT":
          
        sql="""UPDATE book SET b_author=%s,b_name=%s,b_types=%s WHERE b_id=%s"""  
        update_book={"b_id":new_id,
                 "b_author":new_author,   
                 "b_name":new_bname,
                 "b_types":new_btypes
    }               
    b.execute(sql,(new_author,new_bname,new_btypes,new_id))    
    a.commit()
    return jsonify(update_book)                     

@app.route("/adduser",methods=["POST","GET","PUT"])  
def user():
    a,b=exe_query('con','cursor')
    new_uid=request.form.get('u_id')
    new_uname=request.form.get('u_name')  
    new_email=request.form.get('u_mail')
    new_udpt=request.form.get('u_dept')
    if request.method=="POST":   
        error_msg=validate(new_uname,new_email,new_udpt)
        if error_msg:
            return jsonify({"message":error_msg}),400   
       
        q= "INSERT INTO user VALUES"
        q = insert_val(q,new_uid) 
        q = insert_val(q,new_uname)
        q = insert_val(q,new_email)
        q = insert_val(q,new_udpt)
        if check_word(q) != check_lword(q) :
            q=q + ")"                                           
            res=b.execute(q)
            a.commit()
            return jsonify({"message":"User  added successfully!"}),200   
                       
             
    if request.method=="GET":
        b.execute("SELECT * FROM user") 
        user=b.fetchall()
        if user:  
            return jsonify(user),200
        else:
            return "Something wrong",404 
    if request.method=="PUT":
        sql="""UPDATE user SET u_name=%s,u_mail=%s,u_dept=%s WHERE u_id=%s"""  
        update_user={"u_id":new_uid,
                 "u_name":new_uname,
                 "u_mail":new_email,   
                 "u_dept":new_udpt                 
    }               
    b.execute(sql,(new_uname,new_email,new_udpt,new_uid,))    
    a.commit()
    return jsonify(update_user)  

def bookid(q,qLabel,qParam):
    if qParam != None:                
        y = " %s= '%s' " % (qLabel,qParam,) 
        c="%s%s" % (q,y) 
        return c
                
@app.route("/status",methods=["POST","GET","PUT"]) 
def book_status():
    if request.method=="POST":
        a,b=exe_query('con','cursor') 
        new_id=request.form.get('b_id')     
        sql = "select status from book where" 
        sql=bookid(sql,"b_id",new_id)        
        b.execute(sql)
        res=b.fetchone()
        return res

def user_issue_status():  
    a,b=exe_query('con','cursor')
    new_uid=request.form.get('u_id')   
    new_dor=request.form.get('dor') 
    sql ="select * from transaction where"
    sql=bookid(sql,"u_id",new_uid) 
    sq=sql+"and dor is null"      
    b.execute(sq)
    result = b.fetchall()
    return result
def book_issue_status():
    a,b=exe_query('con','cursor') 
    new_id=request.form.get('b_id')
    new_uid=request.form.get('u_id')   
    sql = "select * from transaction where"     
    sql=bookid(sql,"b_id",new_id)
    sql=bookid(sql,"u_id",new_uid)    
    b.execute(sql,(new_id,new_uid,))
    result = b.fetchall()
    return result

@app.route("/issuebook",methods=["POST","GET","PUT"])  
def issue_book():
    a,b=exe_query('con','cursor') 
    new_tid=request.form.get('t_id')
    new_id=request.form.get('b_id')
    new_uid=request.form.get('u_id')
    new_doi=request.form.get('doi')
    new_dor=request.form.get('dor')  
    if request.method=="POST":  
        book=book_status()
        user=user_issue_status()         
        if len(user)==0:  
            if re.search("available",str(book)):
                q= "INSERT INTO transaction VALUES"
                q = insert_val(q,new_tid)  
                q = insert_val(q,new_id)
                q = insert_val(q,new_uid)
                q = insert_val(q,new_dor)            
                q = insert_val(q,new_doi)
                if q:
                    q=q + ")"              
                    sq = "update book set status='issued' where"
                    sql=bookid(sq,"b_id",new_id)                
                    b.execute(q)
                    b.execute(sql)   
                    a.commit() 
                    return jsonify({"message":"Book issued successfully!"}),200
            return jsonify({"message":"Book has not available for ISSUE"}),400          
        return jsonify({"message":"User has not elligible for taking book."}),400           

    if request.method=="GET":
        b.execute("SELECT * FROM transaction") 
        trans=b.fetchall()
        if trans:  
            return jsonify(trans),200
        else:
            return "Something wrong",404 
    
@app.route("/returnbook",methods=["POST","GET","PUT"])  
def return_book():
    a,b=exe_query('con','cursor') 
    new_tid=request.form.get('t_id')
    new_id=request.form.get('b_id')
    new_uid=request.form.get('u_id')
    new_status=request.form.get('status')
    new_dor=request.form.get('dor')
    if request.method=="POST": 
        return_book = book_issue_status()
        if return_book==None:
            return 'Book is not issued'
        else:
            sql='update book set status ="available" where b_id =%s'  
            sq= 'update transaction set dor=%s where b_id =%s'       
            b.execute(sql,(new_id,))
            b.execute(sq,(new_dor,new_id,))
            a.commit()
            return jsonify({"message":"Book returned successfully"})
            
@app.route("/userhistory",methods=["POST","GET","PUT"])  
def hist_user():
    if request.method=="POST":
        a,b=exe_query('con','cursor')  
        new_id=request.form.get('b_id')   
        new_uid=request.form.get('u_id') 
        new_uname=request.form.get('u_name')   
        new_doi=request.form.get('doi')
        sql = "select a.u_id,a.u_name,b.b_id,b.doi from user a inner join transaction b on a.u_id=%s = b.u_id=%s"        
        b.execute(sql,(new_uid,new_uid,))
        result = b.fetchall()
        return jsonify(result),200
@app.route("/bookhistory",methods=["POST","GET","PUT"])  
def hist_book():
    if request.method=="POST":
        a,b=exe_query('con','cursor')  
        new_id=request.form.get('b_id')   
        new_uid=request.form.get('u_id') 
        new_uname=request.form.get('u_name')   
        new_doi=request.form.get('doi')
        sq = "select * from book a inner join transaction b on a.b_id=%s = b.b_id=%s" 
        b.execute(sq,(new_id,new_id,))
        result = b.fetchall()
        return jsonify(result),200
         
 
if __name__=='__main__':
    app.run(debug=True) 
