from flask import Flask, redirect, url_for, render_template, request
from module import dbModule
import datetime
import time
from flask.json import JSONEncoder

app = Flask(__name__)

#MAIN PAGE
@app.route("/")

#수업 조회
@app.route("/class")
def home():
    db_class= dbModule.Database()

    sql2     = "SELECT * FROM test.study" # sql2 => test DB의 study TABLE
    row2     = db_class.executeAll(sql2)
    sql3     = "SELECT * FROM test.feedback" 
    row3     = db_class.executeAll(sql3)

    return render_template("index.html", study = row2, feed = row3) 

# 학생조회
@app.route("/student")
def student():
    db_class= dbModule.Database()
    sql1     = "SELECT * FROM test.student"
    row1     = db_class.executeAll(sql1)
    sql2     = "SELECT * FROM test.study"
    row2     = db_class.executeAll(sql2)
    sql3     = "SELECT * FROM test.feedback"
    row3     = db_class.executeAll(sql3)
    return render_template("tables.html", stu = row1, study = row2, feed = row3)


# 학생조회에서 개인별 학생 세부정보 조회 
@app.route("/detail",methods=['POST','GET'])
def detail():
    if request.method == "GET":
        keyy=request.args['keyy']
        asdf = int(keyy)
        db_class=dbModule.Database()
        sql1    ="SELECT*FROM test.student WHERE student_id = %d"%(asdf)     # 학생 정보에 대한 상세 페이지 가져오기
        row1    =db_class.executeAll(sql1)
        sql2    ="SELECT*FROM test.study WHERE student_id = %d"%(asdf)       # 학생에 대한 공부 기록 가져오기
        row2    =db_class.executeAll(sql2)       
        print(row2)
    
    return render_template("tables_detail.html", student= row1[0], study=row2)


#피드백 조회
@app.route("/feedback")
def feedback():
    db_class=dbModule.Database()

    sql3="SELECT * FROM test.feedback"
    row3=db_class.executeAll(sql3)

    return render_template("feedback.html",feed=row3)

# 학생설정
@app.route("/edit", methods=["POST","GET"])
def edit():
    db_class= dbModule.Database()
    if request.method == "POST":
        stu_id = request.form.get("delstu")
        print(stu_id)
        if (stu_id):
            stu_id = int(stu_id)
            sql2 = "DELETE FROM test.student WHERE student_id = %d" % (stu_id)
            db_class.execute(sql2)   
            db_class.commit()

    sql1     = "SELECT * FROM test.student WHERE student_id"

    row1     = db_class.executeAll(sql1)

    return render_template("edit.html", stu = row1)

    

# 학생 설정에서 개인별 학생 정보 수정사항 
@app.route("/edit_detail", methods = ['POST', 'GET'])
def edit_detail():
    if request.method == 'POST':
        db_class= dbModule.Database()
        # 세부내용 수정
        st = request.form.get("student_name")
        st = "'" + st + "'"
        k = request.form.get("student_key")
        k = int(k)
        
        sql2 = "UPDATE test.student SET name = %s WHERE student_id = %d" % (st, k)
        print(sql2)
        db_class.execute(sql2)
        db_class.commit()
        
        # 추가 세부사항 입력
        birth=request.form.get("birthday")
        birth="'"+birth+"'"
        gender=request.form.get("gender")
        gender="'"+gender+"'"
        phone=request.form.get("phone")
        phone="'"+phone+"'"
        email=request.form.get('email')
        email="'"+email+"'"
        # 주소를 추가한다면 다음 문구
        # address1=request.form.get('address-01')
        # address2=request.form.get('address-02')
        # address3=request.form.get('address-03')
        # address="'"+address1+" "+address2+" "+address3+"'"
        # sub = "UPDATE test.student SET birth = %s, gender = %s, phone = %s , email= %s, residence= %s WHERE student_id = %d" % (birth,gender,phone,email,address,k)
        sub = "UPDATE test.student SET birth = %s, gender = %s, phone = %s , email= %s WHERE student_id = %d" % (birth,gender,phone,email,k)
        db_class.execute(sub)
        db_class.commit()

        # 세부사항 수정 내용과 별개로 return 되면 edit 목록에 보이는 table
        sql1     = "SELECT * FROM test.student"
        row1     = db_class.executeAll(sql1)

        return render_template("edit.html", stu = row1)

    if request.method == "GET":
        keyy = request.args['keyy']
        asdf = int(keyy)
        db_class= dbModule.Database()
        sql2     = "SELECT * FROM test.student WHERE student_id = %d" % (asdf)
        row2     = db_class.executeAll(sql2)
        print(row2)
        return render_template("edit_detail.html", student = row2[0]) 






if __name__ == "__main__":
    app.run(debug=True)