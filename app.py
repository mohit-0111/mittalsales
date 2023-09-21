from flask import Flask,render_template,request,redirect
import sqlite3
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
import urllib.parse

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1011'
app.config['MYSQL_DB'] = 'mittalsales'
msql=MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addvoltas',methods=['GET','POST'])
def addvoltas():
    if request.method=='POST':
        
        item=request.form['item']
        quantity=request.form['qty']
        dp=request.form['dp']
        retail=request.form['rtl']
        
        sql='INSERT INTO sales (item,quantity,dp,retail) VALUES (%s,%s,%s,%s)'
        val=(item,quantity,dp,retail)
        cursor = msql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql,val)
        msql.connection.commit()
    return render_template('addvoltas.html')

@app.route('/voltasdetail')
def voltasdetail():
    quer='select * from sales'
    cursor = msql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(quer)
    acc=cursor.fetchall()
    msql.connection.commit()

    return render_template('voldetail.html',acc=acc)

@app.route("/volupdate/<int:id>",methods=['get','POST'])
def volupdate(id):
    todo=f'select * from sales where id={id}'
    cursor = msql.connection.cursor(MySQLdb.cursors.Cursor)
    cursor.execute(todo)
    r=cursor.fetchall()
    
    x=[(a) for a in r]
    print(x)
    if request.method=='POST':
        
        itemm=request.form['item']
        quantity=request.form['qty']
        dp=request.form['dp']
        retail=request.form['rtl']
        
        q=f'update sales set item="{itemm}",quantity="{quantity}",dp="{dp}",retail="{retail}" where id={id}'
        cursor.execute(q)
        msql.connection.commit()
        return redirect('/voltasdetail')
    return render_template('volupdate.html',x=x,id=id)

if __name__=='__main__':        
    app.run(host="0.0.0.0", port=5000, debug=True)