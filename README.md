# Rest API for the Cloud Computing mini-project

You can have access https://qmul-cc-miniproj-group24.azurewebsites.net/

# QMUL-CC-Mini-Project-Group-24
Cloud Computing Mini Project done by Group 24 at Queen Mary University of London

# External Secure Database
The project has two main parts, namely the secure database and the flask application that provides a front-end to a user and communicates with the database. The centerpiece of the application is a secure database that has information about students, teachers, admin, subjects. The Database has been developed in Cassandra Cosmos DB and is hosted on Azure.

# Role Based Access policies
The database itself is secured using Role Based Access Policies. There are multiple access levels that allows/restricts access to the database and operations with it on a user's role in the organization.

# User Accounts and Access Management
User Access Management (UAM), also known as identity and access management (IAM), is the administration of giving individual users within a system access to the tools they need at the right time. In our Project we have 3 types of user accounts, namely: admin, teacher and student. Firstly the Admin account is one who has the access to edit Subjects, Teachers and Students but also Admin can have access to the data of these types of user accounts. Then we have the Teacher as a user account who can only edit the subjects that they are teaching and they can see their time-table and the Holiday calendar through the external API.

# HTTPS
All communications between a client and our application is encrypted communications using Transport Layer Security (TLS). We have deployed our app on Azure Web App Service since it has inbuilt SSL certification and provides 1.2 version of Transport Layer Security. It automatically redirects all traffic to HTTPS.

# Hash-based authentication
To secure passwords stored stored in the database we have implemented the hash-based authentication using the following python libraries: HMAC, hashlib. HMAC is a framework to create hash-based message authentication code (MAC), while hashlib is a library that provides implementation of different hashing algorithms. Our implementation uses SHA-256 hashing algorithm. Upon creation of a new user, our implementation creates a hash-value from the provided password keyword and stores this value in the database, further when authentificating users the application again creates a hash-value from a password keyword and compares it against the hash-value stored in the database.

# This Rest API was created under the framework of the Cloud Computing module, from the Queen Mary, University of London.

To use the API, username and password or token based authentication is required.

This is a Flask app with an API layer. It has the following properties:

    It has the following relational entities:
        - Student
        - Teacher
        - Subject
        - Administrator
    
__Student Login:__ Only registered Students can have access to a list of their subjects (time table) by pressing the Student Login button if they are not registered to the Database will print login unsuccessful.
 
__Teacher Login:__ Only registered Teachers can have access to a list of students by pressing the Teachers Login button if they are not registered to the Database will print login unsuccessful.
 
__Administrator Login:__
 
**Insert Students:** In this page the user can register a new Student by inserting their full name, password and choosing the year of studies.

__Insert teachers:__ In this page the user can register a new Teacher by inserting their full name, password and choosing the subject ID that of the subject that they teach.

__Insert Admins:__ In this page the user can register a new Admin by inserting their full name and password.

__Delete Students:__ In this page the user can delete a Student entry by submiting their ID.

__Delete Teacher:__ In this page the user can delete a Teacher entry by submiting their ID.

__Delete Admin:__ In this page the user can delete an Admin entry by submiting their ID.

__Delete Subject:__ In this page the user can delete a Subject entry by submiting their ID.

__Update Students (not password):__ This page can Update Students details by insert their ID.

__Update Teachers (not password):__ This page can Update Teachers details by insert their ID.

__Update Admins (not password):__ This page can Update Admins details by insert their ID.

__Update Subjects:__ This page can Update Subjects details by insert their ID.

__Reset Password of Student:__ This page can reset the student password by entering their ID.

__Reset Password of Teacher:__ This page can reset the Teacher password by entering their ID.

__Reset Password of Admins:__ This page can reset the Admins pasword by entering their ID.

__Holiday List:__ Is an external an external REST service to complement its functionality with the existing REST API. The main function is to display the Holiday Calendar for the United Kingdom.


