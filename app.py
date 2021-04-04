from cassandra.auth import PlainTextAuthProvider
import config as cfg
from cassandra.query import BatchStatement, SimpleStatement
from prettytable import PrettyTable
import time
import ssl
import cassandra
from cassandra.cluster import Cluster
from cassandra.policies import *
from ssl import PROTOCOL_TLSv1_2, SSLContext, CERT_NONE
from requests.utils import DEFAULT_CA_BUNDLE_PATH
import datetime
import json, io
import urllib.request, urllib.response
import flask
from flask import Flask, request, jsonify
from flask.templating import render_template
import hashlib
import hmac
app = Flask(__name__, template_folder='Templates')

def PrintTable(rows):
    t=[]
    for r in rows:
        t.append(r)
    return t


def pwd_to_hash(pwd_str):
    ''' create a string with the hash value from a password string '''
    sha256 = hmac.new(pwd_str.encode('UTF-8'), digestmod=hashlib.sha256)
    hash_value = sha256.hexdigest()
    return hash_value

@app.route('/', methods=['GET'])
def index():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('index.html')), 200


@app.route('/studentLogin/', methods=['GET', 'POST'])
def studentLogin():
    ''' Render the html and authentification method'''

    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('studentLogin.html')), 200
    
    if flask.request.method == 'POST':
        u_id = flask.request.form['uid']
        # pwd is a string with hash value that is checked against stored hash value in the DB
        pwd = pwd_to_hash(flask.request.form['pwd'])
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        # Connect to Cassandra DB
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        #</authenticateAndConnect>
        rows = session.execute("SELECT * FROM miniproj.students WHERE student_id=" + u_id + " AND password='" + pwd + "' ALLOW FILTERING")
        
        # Verify user's credentials
        if len(rows.current_rows) == 0:
            result = 'Wrong Username or Password'
        else:
            result = 'Login Successful'
            for t in rows:
                year = t.year
            rows = session.execute("SELECT subject_name, time FROM miniproj.subjects WHERE year='" + str(year) + "' ALLOW FILTERING")
            cluster.shutdown()
            # Print student's data if Login successful
            result = PrintTable(rows)
        cluster.shutdown()
        return flask.render_template('studentLogin.html', result = result), 200

@app.route('/adminLogin/', methods=['GET', 'POST'])
def adminLogin():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('adminLogin.html')), 200
    
    if flask.request.method == 'POST':
        u_id = flask.request.form['uid']
        # pwd is a string with hash value that is checked against stored hash value in the DB
        pwd = pwd_to_hash(flask.request.form['pwd'])
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        #</authenticateAndConnect>
        rows = session.execute("SELECT * FROM miniproj.admins WHERE admin_id=" + u_id + " AND password='" + pwd + "' ALLOW FILTERING")
        cluster.shutdown()
        if len(rows.current_rows) == 0:
            result = 'Wrong Username or Password'
        else:
            result = 'Login Successful'
        return flask.render_template('adminLogin.html', result = result), 200

@app.route('/teacherLogin/', methods=['GET', 'POST'])
def teacherLogin():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('teacherLogin.html')), 200
    
    if flask.request.method == 'POST':
        u_id = flask.request.form['uid']
        # pwd is a string with hash value that is checked against stored hash value in the DB
        pwd = pwd_to_hash(flask.request.form['pwd'])
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        #</authenticateAndConnect>
        rows = session.execute("SELECT * FROM miniproj.teachers WHERE teacher_id=" + u_id + " AND password='" + pwd + "' ALLOW FILTERING")
        
        # Verify teacher's credentials
        if len(rows.current_rows) == 0:
            result = 'Wrong Username or Password'
        else:
            result = 'Login Successful'
            for t in rows:
                subid = t.subject_id
            rows = session.execute("SELECT * FROM miniproj.subjects WHERE subject_id=" + str(subid) + " ALLOW FILTERING")
            for t in rows:
                year = t.year
            rows = session.execute("SELECT student_id,student_name FROM miniproj.students WHERE year='" + str(year) + "' ALLOW FILTERING")
            cluster.shutdown()
            # Print students's data list
            result = PrintTable(rows)
        return flask.render_template('teacherLogin.html', result = result), 200

@app.route('/insertStudent/', methods=['GET', 'POST'])
def insertStudent():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('insertStudent.html')), 200
    
    if flask.request.method == 'POST':
        name = flask.request.form['name']
        # pwd is a string with hash value that is checked against stored hash value in the DB
        pwd = pwd_to_hash(flask.request.form['pwd'])
        year = flask.request.form['year']
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        rows = session.execute("SELECT * FROM miniproj.students")
        next_id = 0
        for t in rows:
            if next_id < t.student_id:
                next_id = t.student_id
        next_id = int(next_id) + 1
        #</authenticateAndConnect>
        try:
            # Insert new student data
            rows = session.execute("INSERT INTO  miniproj.students  (student_id, student_name , password, year) VALUES (%s,%s,%s,%s)", [next_id,name,pwd, year])
            result = 'Inserted successfully. User ID of new record is '+ str(next_id)
        except:
            result = 'Failed to insert'
        cluster.shutdown()
        return flask.render_template('insertStudent.html', result = result), 201

@app.route('/insertAdmin/', methods=['GET', 'POST'])
def insertAdmin():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('insertAdmin.html')), 200
    
    if flask.request.method == 'POST':
        name = flask.request.form['name']
        # pwd is a string with hash value that is checked against stored hash value in the DB
        pwd = pwd_to_hash(flask.request.form['pwd'])
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        rows = session.execute("SELECT * FROM miniproj.admins")
        next_id = 0
        for t in rows:
            if next_id < t.admin_id:
                next_id = t.admin_id
        next_id = int(next_id) + 1
        #</authenticateAndConnect>
        try:
            # Insert new admin data
            rows = session.execute("INSERT INTO  miniproj.admins  (admin_id, admin_name , password) VALUES (%s,%s,%s)", [next_id,name,pwd])
            result = 'Inserted successfully. User ID of new record is '+ str(next_id)
        except:
            result = 'Failed to insert'
        cluster.shutdown()
        return flask.render_template('insertAdmin.html', result = result), 201


@app.route('/insertTeacher/', methods=['GET', 'POST'])
def insertTeacher():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('insertTeacher.html')), 200
    
    if flask.request.method == 'POST':
        name = flask.request.form['name']
        # pwd is a string with hash value that is checked against stored hash value in the DB
        pwd = pwd_to_hash(flask.request.form['pwd'])
        subid = flask.request.form['subid']
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        rows = session.execute("SELECT * FROM miniproj.subjects WHERE subject_id=" + subid + " ALLOW FILTERING")
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('insertTeacher.html', result = "Subject ID does not exist"), 400
        rows = session.execute("SELECT * FROM miniproj.teachers")
        next_id = 0
        for t in rows:
            if next_id < t.teacher_id:
                next_id = t.teacher_id
        next_id = int(next_id) + 1
        #</authenticateAndConnect>
        try:
            # Insert new teacher data
            rows = session.execute("INSERT INTO  miniproj.teachers  (teacher_id, teacher_name , password, subject_id) VALUES (%s,%s,%s,%s)", [next_id,name,pwd,int(subid)])
            result = 'Inserted successfully. User ID of new record is '+ str(next_id)
        except Exception as e:
            result = 'Failed to insert'
        cluster.shutdown()
        return flask.render_template('insertTeacher.html', result = result), 201


@app.route('/insertSubject/', methods=['GET', 'POST'])
def insertSubject():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('insertSubject.html')), 200
    
    if flask.request.method == 'POST':
        name = flask.request.form['name']
        time = flask.request.form['time']
        year = flask.request.form['year']
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with subjects and schedule from the DB
        rows = session.execute("SELECT * FROM miniproj.subjects WHERE year='" + year + "' AND time='" + time + "' ALLOW FILTERING")
        # Check for clashes between subjects
        if len(rows.current_rows) > 0:
            cluster.shutdown()
            return flask.render_template('insertSubject.html', result = 'Clash detected. Please enter a new time.'), 400
        rows = session.execute("SELECT * FROM miniproj.subjects")
        next_id = 0
        for t in rows:
            if next_id < t.subject_id:
                next_id = t.subject_id
        next_id = int(next_id) + 1
        #</authenticateAndConnect>
        try:
            # Insert new subject and return subject_id if successful
            rows = session.execute("INSERT INTO  miniproj.subjects  (subject_id, subject_name , time, year) VALUES (%s,%s,%s,%s)", [next_id,name,time, year])
            result = 'Inserted successfully. User ID of new record is '+ str(next_id)
        except Exception as e:
            result = 'Failed to insert'
        cluster.shutdown()
        return flask.render_template('insertSubject.html', result = result), 201

@app.route('/deleteSubject/', methods=['GET', 'POST'])
def deleteSubject():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('deleteSubject.html')), 200
    
    if flask.request.method == 'POST':
        subid = flask.request.form['subid']
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with subjects from the DB
        rows = session.execute("SELECT * FROM miniproj.subjects WHERE subject_id=" + subid)
        # Check if selected subject exists
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('deleteSubject.html', result = 'Invalid Subject ID'), 400
        #</authenticateAndConnect>
        try:
            # Delete selected subject from the DB
            rows = session.execute("DELETE FROM miniproj.subjects  WHERE subject_id = "+subid)
            result = 'Deleted Successfully'
        except Exception as e:
            result = 'Error deleting record'
        cluster.shutdown()
        return flask.render_template('deleteSubject.html', result = result), 200

@app.route('/deleteAdmin/', methods=['GET', 'POST'])
def deleteAdmin():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('deleteAdmin.html')), 200
    
    if flask.request.method == 'POST':
        subid = flask.request.form['subid']
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with existing admins from the DB
        rows = session.execute("SELECT * FROM miniproj.admins WHERE admin_id=" + subid)
        # Check if selected admin exists
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('deleteAdmin.html', result = 'Invalid Admin ID'), 400
        #</authenticateAndConnect>
        try:
            # Delete selected admin
            rows = session.execute("DELETE FROM miniproj.admins  WHERE admin_id = "+subid)
            result = 'Deleted Successfully'
        except Exception as e:
            result = 'Error deleting record'
        cluster.shutdown()
        return flask.render_template('deleteAdmin.html', result = result), 200

@app.route('/deleteTeacher/', methods=['GET', 'POST'])
def deleteTeacher():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('deleteTeacher.html')), 200
    
    if flask.request.method == 'POST':
        subid = flask.request.form['subid']
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with existing teachers from the DB
        rows = session.execute("SELECT * FROM miniproj.teachers WHERE teacher_id=" + subid)
        # Check if selected teacher exists
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('deleteTeacher.html', result = 'Invalid Teacher ID'), 400
        #</authenticateAndConnect>
        try:
            # Delete seleted teacher
            rows = session.execute("DELETE FROM miniproj.teachers  WHERE teacher_id = "+subid)
            result = 'Deleted Successfully'
        except Exception as e:
            result = 'Error deleting record'
        cluster.shutdown()
        return flask.render_template('deleteTeacher.html', result = result), 200

@app.route('/deleteStudent/', methods=['GET', 'POST'])
def deleteStudent():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('deleteStudent.html')), 200
    
    if flask.request.method == 'POST':
        subid = flask.request.form['subid']
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with existing students from the DB
        rows = session.execute("SELECT * FROM miniproj.students WHERE student_id=" + subid)
        # Check if selected student exists
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('deleteStudent.html', result = 'Invalid Student ID'), 400
        #</authenticateAndConnect>
        try:
            # Delete selected student
            rows = session.execute("DELETE FROM miniproj.students  WHERE student_id = "+subid)
            result = 'Deleted Successfully'
        except Exception as e:
            result = 'Error deleting record'
        cluster.shutdown()
        return flask.render_template('deleteStudent.html', result = result), 200

@app.route('/updateStudent/', methods=['GET', 'POST'])
def updateStudent():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('updateStudent.html')), 200
    
    if flask.request.method == 'POST':
        subid = flask.request.form['subid']
        name = flask.request.form['name']
        year = flask.request.form['year']
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with existing students from the DB
        rows = session.execute("SELECT * FROM miniproj.students WHERE student_id=" + subid)
        # Check if selected student exists
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('updateStudent.html', result = 'Invalid Student ID'), 400
        #</authenticateAndConnect>
        try:
            # Update selected student's information (studnet's name, year)
            rows = session.execute("UPDATE miniproj.students SET student_name='"+name+"', year='"+year+"' WHERE student_id = "+subid)
            result = 'Updated Successfully'
        except Exception as e:
            result = 'Error updating record'
        cluster.shutdown()
        return flask.render_template('updateStudent.html', result = result), 200

@app.route('/updateSubject/', methods=['GET', 'POST'])
def updateSubject():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('updateSubject.html')), 200
    
    if flask.request.method == 'POST':
        subid = flask.request.form['subid']
        name = flask.request.form['name']
        year = flask.request.form['year']
        time = flask.request.form['time']
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with existing subjects from the DB
        rows = session.execute("SELECT * FROM miniproj.subjects WHERE subject_id=" + subid)
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('updateSubject.html', result = 'Invalid Subject ID'), 400
        # Retreive data with existing subjects and schedule from the DB
        rows = session.execute("SELECT * FROM miniproj.subjects WHERE year='" + year + "' AND time='" + time + "' ALLOW FILTERING")
        # Check for clashes between subjects
        if len(rows.current_rows) > 0:
            cluster.shutdown()
            return flask.render_template('insertSubject.html', result = 'Clash detected. Please enter a new time.'), 400
        #</authenticateAndConnect>
        try:
            # Edit selected subject information (name, year, time, subject id)
            rows = session.execute("UPDATE miniproj.subjects SET subject_name='"+name+"', year='"+year+"', time='"+time+"' WHERE subject_id = "+subid)
            result = 'Updated Successfully'
        except Exception as e:
            result = 'Error updating record'
        cluster.shutdown()
        return flask.render_template('updateStudent.html', result = result), 200

@app.route('/updateAdmin/', methods=['GET', 'POST'])
def updateAdmin():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('updateAdmin.html')), 200
    
    if flask.request.method == 'POST':
        subid = flask.request.form['subid']
        name = flask.request.form['name']
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with existing admins from the DB
        rows = session.execute("SELECT * FROM miniproj.admins WHERE admin_id=" + subid)
        # Check if selected admin exists
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('updateAdmin.html', result = 'Invalid Admin ID'), 400
        #</authenticateAndConnect>
        try:
            # Edit selected admin's information (name, admin id)
            rows = session.execute("UPDATE miniproj.admins SET admin_name='"+name+"' WHERE admin_id = "+subid)
            result = 'Updated Successfully'
        except Exception as e:
            result = 'Error updating record'
        cluster.shutdown()
        return flask.render_template('updateAdmin.html', result = result), 200

@app.route('/updateTeacher/', methods=['GET', 'POST'])
def updateTeacher():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('updateTeacher.html')), 200
    
    if flask.request.method == 'POST':
        subid = flask.request.form['subid']
        name = flask.request.form['name']
        subjectid = flask.request.form['subjectid']
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with selected teacher from the DB
        rows = session.execute("SELECT * FROM miniproj.teachers WHERE teacher_id=" + subid)
        # Check if teacher exists
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('updateTeacher.html', result = 'Invalid Teacher ID'), 400
        # Retreive data with selected subject for selected teacher from the DB
        rows = session.execute("SELECT * FROM miniproj.subjects WHERE subject_id=" + subjectid + " ALLOW FILTERING")
        # Check if selected subject exists
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('updateTeacher.html', result = "Subject ID does not exist"), 400
        #</authenticateAndConnect>
        try:
            # Edit selected teacher's information (name, subject id, teacher id)
            rows = session.execute("UPDATE miniproj.teachers SET teacher_name='"+name+"', subject_id="+subjectid+" WHERE teacher_id = "+subid)
            result = 'Updated Successfully'
        except Exception as e:
            result = 'Error updating record'
        cluster.shutdown()
        return flask.render_template('updateTeacher.html', result = result), 200

@app.route('/resetTeacherPassword/', methods=['GET', 'POST'])
def resetTeacherPassword():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('resetTeacherPassword.html')), 200
    
    if flask.request.method == 'POST':
        subid = flask.request.form['subid']
        # pwd is a string with hash value that is checked against stored hash value in the DB
        pwd = pwd_to_hash(flask.request.form['pwd'])
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with selected teacher from the DB
        rows = session.execute("SELECT * FROM miniproj.teachers WHERE teacher_id=" + subid)
        # Check if teacher exists
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('resetTeacherPassword.html', result = 'Invalid Teacher ID'), 400
        #</authenticateAndConnect>
        try:
            # Edit password for the selected teacher
            rows = session.execute("UPDATE miniproj.teachers SET password='"+pwd+"' WHERE teacher_id = "+subid)
            result = 'Resetted Successfully'
        except Exception as e:
            result = 'Error resetting record'
        cluster.shutdown()
        return flask.render_template('resetTeacherPassword.html', result = result), 200

@app.route('/resetStudentPassword/', methods=['GET', 'POST'])
def resetStudentPassword():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('resetStudentPassword.html')), 200
    
    if flask.request.method == 'POST':
        subid = flask.request.form['subid']
        # pwd is a string with hash value that is checked against stored hash value in the DB
        pwd = pwd_to_hash(flask.request.form['pwd'])
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with selected student from the DB
        rows = session.execute("SELECT * FROM miniproj.students WHERE student_id=" + subid)
        # Check if the student exists
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('resetStudentPassword.html', result = 'Invalid Student ID'), 400
        #</authenticateAndConnect>
        try:
            # Edit password for the selected student
            rows = session.execute("UPDATE miniproj.students SET password='"+pwd+"' WHERE student_id = "+subid)
            result = 'Updated Successfully'
        except Exception as e:
            result = 'Error updating record'
        cluster.shutdown()
        return flask.render_template('resetStudentPassword.html', result = result), 200

@app.route('/resetAdminPassword/', methods=['GET', 'POST'])
def resetAdminPassword():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('resetAdminPassword.html')), 200
    
    if flask.request.method == 'POST':
        subid = flask.request.form['subid']
        # pwd is a string with hash value that is checked against stored hash value in the DB
        pwd = pwd_to_hash(flask.request.form['pwd'])
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE
        auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
        cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
        session = cluster.connect()
        # Retreive data with selected admin from the DB
        rows = session.execute("SELECT * FROM miniproj.admins WHERE admin_id=" + subid)
        # Check if selected admin exists
        if len(rows.current_rows) == 0:
            cluster.shutdown()
            return flask.render_template('resetAdminPassword.html', result = 'Invalid Admin ID'), 400
        #</authenticateAndConnect>
        try:
            # Edit password for the selected admin
            rows = session.execute("UPDATE miniproj.admins SET password='"+pwd+"' WHERE admin_id = "+subid)
            result = 'Updated Successfully'
        except Exception as e:
            result = 'Error updating record'
        cluster.shutdown()
        return flask.render_template('resetAdminPassword.html', result = result), 200




# @app.route('/', methods=['GET'])
# def initial_screen():
#     response = {}
#     response["MESSAGE"] = f"Please go to the following links: https://qmul-cloud-computing-mini-proj.herokuapp.com/getallstudents/ \n https://qmul-cloud-computing-mini-proj.herokuapp.com/getallsubjects/ \n https://qmul-cloud-computing-mini-proj.herokuapp.com/getallteachers/ \n https://qmul-cloud-computing-mini-proj.herokuapp.com/getalladmins/ \n https://qmul-cloud-computing-mini-proj.herokuapp.com/getholidays/"
#     return jsonify(response)


@app.route('/getholidays/', methods=['GET'])
def getHolidays():
    # Retreive information on public holiday's from the external api
    url = 'https://date.nager.at/api/v2/publicholidays/' + str((datetime.datetime.now()).year) + '/GB'
    with urllib.request.urlopen(url) as response:
        return json.JSONEncoder().encode(json.load(response)), 200

@app.route('/getallstudents/', methods=['GET'])
def getStudents():
    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    ssl_context.verify_mode = CERT_NONE
    auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
    cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
    session = cluster.connect()
    #</authenticateAndConnect>
    # Retreive data with all students from the DB
    rows = session.execute('SELECT * FROM miniproj.students')
    cluster.shutdown()
    # Return the response in json format
    return jsonify(PrintTable(rows)), 200


@app.route('/getallteachers/', methods=['GET'])
def getTeachers():
    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    ssl_context.verify_mode = CERT_NONE
    auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
    cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
    session = cluster.connect()
    #</authenticateAndConnect>
    # Retreive data with all teachers from the DB
    rows = session.execute('SELECT * FROM miniproj.teachers')
    cluster.shutdown()
    # Return the response in json format
    return jsonify(PrintTable(rows)), 200



@app.route('/getallsubjects/', methods=['GET'])
def getSubjects():
    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    ssl_context.verify_mode = CERT_NONE
    auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
    cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
    session = cluster.connect()
    #</authenticateAndConnect>
    # Retreive data with all subjects from the DB
    rows = session.execute('SELECT * FROM miniproj.subjects')
    cluster.shutdown()
    # Return the response in json format
    return jsonify(PrintTable(rows)), 200



@app.route('/getalladmins/', methods=['GET'])
def getAdmins():
    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    ssl_context.verify_mode = CERT_NONE
    auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
    cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
    session = cluster.connect()
    #</authenticateAndConnect>
    # Retreive data with all admins from the DB
    rows = session.execute('SELECT * FROM miniproj.admins')
    cluster.shutdown()
    # Return the response in json format
    return jsonify(PrintTable(rows)), 200

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
