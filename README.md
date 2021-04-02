# Rest API for the Cloud Computing mini-project

This Rest API was created under the framework of the Cloud Computing module, from the Queen Mary, University of London.

To use the API, username and password or token based authentication is required.

This is a Flask app with an API layer. It has the following properties:

    It has the following relational entities:
        Student
        Teacher
        Subject
        Administrator
    
Student Login: Only registered Students can have access to a list of their subjects (time table) by pressing the Student Login button if they are not registered to the Database will print login unsuccessful.
 
Teacher Login: Only registered Teachers can have access to a list of students by pressing the Teachers Login button if they are not registered to the Database will print login unsuccessful.
 
Administrator Login:
 
Insert Students: In this page the user can register a new Student by inserting their full name, password and choosing the year of studies.

Insert teachers: In this page the user can register a new Teacher by inserting their full name, password and choosing the subject ID that of the subject that they teach.

Insert Admins: In this page the user can register a new Admin by inserting their full name and password.

Delete Students: In this page the user can delete a Student entry by submiting their ID.

Delete Teacher: In this page the user can delete a Teacher entry by submiting their ID.

Delete Admin: In this page the user can delete an Admin entry by submiting their ID.

Delete Subject: In this page the user can delete a Subject entry by submiting their ID.

Update Students (not password): This page can Update Students details by insert their ID.

Update Teachers (not password): This page can Update Teachers details by insert their ID.

Update Admins (not password): This page can Update Admins details by insert their ID.

Update Subjects: This page can Update Subjects details by insert their ID.

Reset Password of Student: This page can reset the student password by entering their ID.

Reset Password of Teacher: This page can reset the Teacher password by entering their ID.

Reset Password of Admins: This page can reset the Admins pasword by entering their ID.

Holiday List: Is an external an external REST service to complement its functionality with the existing REST API. The main function is to display the Holiday Calendar for the United Kingdom.


For the hash-based authentication we have used the following python libraries: HMAC, hashlib. HMAC is a framework to create hash-based message authentication code (MAC), while hashlib is a library that provides implementation of different hashing algorithms.  Our implementation uses SHA-256 hashing algorithm. Upon creation of a new user, our implementation creates a hash-value from the provided password keyword and stores this value in the database, further when authentificating users the application again creates a hash-value from a password keyword and compares it against the hash-value stored in the database.
