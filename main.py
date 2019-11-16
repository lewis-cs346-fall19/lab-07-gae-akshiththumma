import webapp2
import MySQLdb
import passwords
import json
import random
import cgi
import cgitb

class MainPage(webapp2.RequestHandler):
     def get(self):
          self.response.headers["Content-Type"]="text/html"
          self.response.write("Hello world1")
          conn = MySQLdb.connect(unix_socket=passwords.SQL_HOST,
                                 user=passwords.SQL_USER,
                                 passwd=passwords.SQL_PASSWD,
                                 db="personDetails")
          cursor1 = conn.cursor()
          cursor1.execute("SELECT * FROM Details")
          res = cursor1.fetchall()
          obj = []
          for i in res:
              obj.append({'ID':i[0],'Name':i[1]})
          obj = json.dumps(obj,indent=2)
         # self.response.write(res)
          cursor1.close()
         # print(obj)
         # return obj
          cookie = self.request.cookies.get("cookie_1")
          #self.response.write(cookie)
          if cookie is None:
              id = "%032x" % random.getrandbits(128)
              self.response.set_cookie("cookie_1", id , max_age=1800)
              self.response.write(cookie)
              cursor2 = conn.cursor()
              cursor2.execute("INSERT INTO sessions (ID,USERNAME) VALUES(%s,%s);", (id,""))
              #self.response.write("<html><p>YES<p></html>")
              self.response.write('''<html>
                    <body>              
                            <form action="https://gaelab-258117.appspot.com/" method="get">
                                        <input type="text" name=USERNAME value="">
                                        <br>
                                        <input type=submit>
                                        <br/>
                    </body>
                                </html>''')
              cursor3 = conn.cursor()
              USERNAME = self.request.get("USERNAME")
              cursor3.execute("UPDATE sessions SET USERNAME=%s WHERE ID=%s;",(USERNAME,id))
              self.response.write(USERNAME)
              cursor3.close()
              conn.commit()
              conn.close()
          else:
              self.response.write(cookie)
          self.response.write('''<html><a href = "https://gaelab-258117.appspot.com/">Increment</a></html>''')
          
app = webapp2.WSGIApplication([
    ("/", MainPage),
], debug=True)
