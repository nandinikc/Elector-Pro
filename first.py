from flask import Flask,render_template,request,session

app = Flask(__name__)
app.secret_key="praveen"

#picfolder=os.path.join('static','images')
#app.config['UPLOAD_FOLDER']=picfolder

import mysql.connector

@app.route('/')
def student():
    if "user" in session:
        return render_template("voting.html")
    return render_template('home.html')

@app.route('/result',methods=['POST','GET'])
def result():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    mycursor = mydb.cursor()
    if request.method=='POST':
        result = request.form
        Id=result.get('Id')
        Name = result.get('Name')
        mycursor.execute("select * from se")
        k=mycursor.fetchall()
        flag =0
        i=0
        for i in k:
            if (i[0]==Id and i[1]==Name):
                flag=1
        if flag==1:
            session['user']=Id
            mycursor.execute("select vote from se where id='%s'" % (session["user"]))
            pj= mycursor.fetchall()
            print("pj value is",pj[0][0])
            if(pj[0][0]==None or pj[0][0]==""):

                return render_template('voting.html',result=Id)
            else:
                return render_template('home.html', ab=0)
        #return render_template('',result=k)
        else:
            flag_admin = 0
            mycursor.execute("select * from adm")
            t = mycursor.fetchall();
            mycursor.execute("SELECT COUNT(Id) FROM se WHERE vote = '0'")
            x = mycursor.fetchall()
            mycursor.execute("SELECT COUNT(Id) FROM se WHERE vote = '1'")
            y = mycursor.fetchall()
            mycursor.execute("SELECT COUNT(Id) FROM se WHERE vote = '2'")
            z = mycursor.fetchall()
            mycursor.execute("SELECT COUNT(Id) FROM se WHERE vote = '3'")
            zx = mycursor.fetchall()
            for j in t:
                if (j[0] == Id and j[1]== Name):
                    flag_admin = 1
            if (flag_admin == 1):
                print(k)
                print(x,y)
                l=[x[0][0],y[0][0],z[0][0],zx[0][0]]
                tielist = l
                print(l)
                l.sort()
                tielist = []
                if(x[0][0]==l[-1]):
                    tielist.append("tippu")
                if (y[0][0] == l[-1]):
                    tielist.append("lokesh")
                if (z[0][0] == l[-1]):
                    tielist.append("chaithanya")
                if (zx[0][0] == l[-1]):
                    tielist.append("indu")
                #print(ma)
                return render_template("index.html", result=k,res1=x[0][0],res2=y[0][0],res3=z[0][0],res4=zx[0][0],res5 = l[-1],tie = tielist)
           # elif:
            #    return render_template('')
            else:
                return render_template("home.html",r = 0)
    else:
        return student()

@app.route('/contact',methods=['POST','GET'])
def contact():
    if "user" in session:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="test"
        )
        mycursor = mydb.cursor()
        mycursor.execute("select vote from se where id='%s'" %(session["user"]))
        pk=mycursor.fetchall()
        #print(pk)
        #print(session["user"])
        if request.method=='POST':
            if request.form['submit_button'] == 'tippu' and pk[0][0]=="":
                mycursor.execute("update se set vote = '0' where Id = '%s'" %(session["user"]))
                mydb.commit()
                mydb.close()
                return render_template("home.html")
            elif request.form['submit_button'] == 'lokesh' and pk[0][0]=="":
                mycursor.execute("update se set vote = '1' where Id = '%s'" % (session["user"]))
                mydb.commit()
                mydb.close()
                return render_template("home.html")
            elif request.form['submit_button'] == 'chaithanya' and pk[0][0]=="":
                mycursor.execute("update se set vote = '2' where Id = '%s'" % (session["user"]))
                mydb.commit()
                mydb.close()
                return render_template("home.html")
            elif request.form['submit_button'] == 'indu' and pk[0][0]=="":
                mycursor.execute("update se set vote = '3' where Id = '%s'" % (session["user"]))
                mydb.commit()
                mydb.close()
                return render_template("home.html")
            #elif request.form["submit_button"] == "logout":
            else:
                session.pop("user",None)
                return render_template("home.html",r = 1)

    else:
        return render_template("home.html")
app.run(debug=True)