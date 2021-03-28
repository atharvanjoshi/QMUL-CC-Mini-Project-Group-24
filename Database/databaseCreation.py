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

def PrintTable(rows):
    t=[]
    for r in rows:
        print(r)

#<authenticateAndConnect>
ssl_context = SSLContext(PROTOCOL_TLSv1_2)
ssl_context.verify_mode = CERT_NONE
auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
session = cluster.connect()
#</authenticateAndConnect>

#<createKeyspace>
print ("\nCreating Keyspace")
session.execute('CREATE KEYSPACE IF NOT EXISTS miniproj WITH replication = {\'class\': \'NetworkTopologyStrategy\', \'datacenter\' : \'1\' }')
#</createKeyspace>

#<createTable>
print ("\nCreating Table")
session.execute('CREATE TABLE IF NOT EXISTS miniproj.students (student_id int PRIMARY KEY, student_name text, password text, year text)')
#</createTable>

#<insertData>
# the hash value below is for pwd = 'password'
session.execute("INSERT INTO  miniproj.students  (student_id, student_name , password, year) VALUES (%s,%s,%s,%s)", [1,'Lybkov','e56a207acd1e6714735487c199c6f095844b7cc8e5971d86c003a7b6f36ef51e', 'First'])
# the hash value below is for pwd = 'abcd1234'
session.execute("INSERT INTO  miniproj.students  (student_id, student_name , password, year) VALUES (%s,%s,%s,%s)", [2,'Doniv','7d70a26b834d9881cc14466eceac8d39188fc5ef5ffad9ab281a8327c2c0d093', 'Second'])
# the hash value below is for pwd = 'hello@123'
session.execute("INSERT INTO  miniproj.students  (student_id, student_name , password, year) VALUES (%s,%s,%s,%s)", [3,'Keviv','7da8de3e629c856691bd50d24e3a7544dcf5752b962e6e83e2892ea6b22f9c66', 'Final'])
# the hash value below is for pwd = 'qmul@789'
session.execute("INSERT INTO  miniproj.students  (student_id, student_name , password, year) VALUES (%s,%s,%s,%s)", [4,'Ehtevs','3a4b1da555a3c8bbdeee6d49a5543b04d2646148cebbeae9dca639f7d5c6d68f', 'First'])
# the hash value below is for pwd = 'hello@456'
session.execute("INSERT INTO  miniproj.students  (student_id, student_name , password, year) VALUES (%s,%s,%s,%s)", [5,'Dnivog','64a2fb9ebbefed820810cbf78c6976f5b20ec0acd79b8de9c01de528d4c2234e', 'Final'])
# the hash value below is for pwd = 'qmul@197!'
session.execute("INSERT INTO  miniproj.students  (student_id, student_name , password, year) VALUES (%s,%s,%s,%s)", [6,'Ateegk','9923aa6bf1bddf0d90b57fcc440e42f87f5eb159c4d7f68390db07ce828447bd, 'Second'])
# the hash value below is for pwd = 'password@123'
session.execute("INSERT INTO  miniproj.students  (student_id, student_name , password, year) VALUES (%s,%s,%s,%s)", [7,'KannabbuS','69033a81e0943e412774691be6f1ccf4aebb773328c550c231cb02edfcef3bab', 'Second'])
#</insertData>

print ("\nCreating Table")
session.execute('CREATE TABLE IF NOT EXISTS miniproj.teachers (teacher_id int PRIMARY KEY, teacher_name text, password text, subject_id int)')
#</createTable>

#<insertData>
# the hash value below is for pwd = 'teacher@123'
session.execute("INSERT INTO  miniproj.teachers  (teacher_id, teacher_name , password, subject_id) VALUES (%s,%s,%s,%s)", [100,'Lybkov','702bce3893aef6986a006e42de14665db327e14099b9be3f3d6a25082fec945d',1000])
# the hash value below is for pwd = 'newteacher@123'
session.execute("INSERT INTO  miniproj.teachers  (teacher_id, teacher_name , password, subject_id) VALUES (%s,%s,%s,%s)", [101,'Doniv','f84e4a21b574e9d410909ca72ffbff04d4a1790b61f5f09f77d1b8757abe1be0',1001])
# the hash value below is for pwd = 'oldteacher@123'
session.execute("INSERT INTO  miniproj.teachers  (teacher_id, teacher_name , password, subject_id) VALUES (%s,%s,%s,%s)", [102,'Keviv','172e8608a8cf84a42f60f4ccbd4fcb26551219df79bc8e9eaaca357623432d6c',1002])
#</insertData>
print ("\nCreating Table")
session.execute('CREATE TABLE IF NOT EXISTS miniproj.subjects (subject_id int PRIMARY KEY, subject_name text, year text, time text)')
#</createTable>

#<insertData>
session.execute("INSERT INTO  miniproj.subjects  (subject_id, subject_name , year, time) VALUES (%s,%s,%s,%s)", [1000,'Maths','First', '10 AM'])
session.execute("INSERT INTO  miniproj.subjects  (subject_id, subject_name , year, time) VALUES (%s,%s,%s,%s)", [1001,'Science','Second', '11 AM'])
session.execute("INSERT INTO  miniproj.subjects  (subject_id, subject_name , year, time) VALUES (%s,%s,%s,%s)", [1002,'History','Final', '12 PM'])


print ("\nCreating Table")
session.execute('CREATE TABLE IF NOT EXISTS miniproj.admins (admin_id int PRIMARY KEY, admin_name text, password text)')
#</createTable>

#<insertData>
# the hash value below is for pwd = 'admin@123'
session.execute("INSERT INTO  miniproj.admins  (admin_id, admin_name , password) VALUES (%s,%s,%s)", [10000,'Admin','5caefcf93fb6538f697241efb8734d3cb0bda3c44aab8f9fd3ee4d990dbe60bf'])
#</insertData>

#<queryAllItems>
print ("\nSelecting All")
rows = session.execute('SELECT * FROM miniproj.students')
PrintTable(rows)
#</queryAllItems>


#<queryAllItems>
print ("\nSelecting All")
rows = session.execute('SELECT * FROM miniproj.subjects')
PrintTable(rows)
#</queryAllItems>


#<queryAllItems>
print ("\nSelecting All")
rows = session.execute('SELECT * FROM miniproj.teachers')
PrintTable(rows)
#</queryAllItems>


#<queryAllItems>
print ("\nSelecting All")
rows = session.execute('SELECT * FROM miniproj.admins')
PrintTable(rows)
#</queryAllItems>

#<queryByID>
print ("\nSelecting Id=1")
rows = session.execute('SELECT * FROM miniproj.students where student_id=1')
PrintTable(rows)
#</queryByID>

cluster.shutdown()
