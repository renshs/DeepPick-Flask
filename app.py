from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate



app = Flask(__name__)

app.config.from_object('config')
app.secret_key = 'super secret key'
db = SQLAlchemy(app=app)
admin = Admin(app=app, name='Admin', url='/admin', template_mode='bootstrap3')
migrate = Migrate(app=app, db=db)

class Request(db.Model):
   __tablename__ = 'request'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   mail = db.Column(db.Text)
   theme = db.Column(db.Text)
   recipient = db.Column(db.String(255))
   theme_group = db.Column(db.String(255))
   status = db.Column(db.Boolean, unique =False)
   def __repr__(self) -> str:
        return "<Request({})>".format(self.theme)
   
admin.add_view(ModelView(Request, db.session))

predict = {"recipients": ["Минсдрав", "Минюст", "Автодор", "Жилупр"],
           "theme_groups": ["Здоровье", "Медицина", "Образование", "Логистика"],
           "themes": ["Сгорела крыша", "Съели голубя", "Ямы на дорогах", "Перегорели фонари"],
           "text": "",
           "entities": {"Локация": ["Пермь", "ул. Подлупка", "ул. Хоруса"], "Персона": ["Семенов", "Знаменская", "Ленин", "Сталин", "Байден", "Обама", "Троцкий", "Маркс", "Энгильс", "Морти", "Рик", "Семенов", "Знаменская", "Ленин", "Сталин", "Байден", "Обама", "Троцкий", "Маркс", "Энгильс", "Морти", "Рик"], "Организации": ["Кафе Приора"]}}

commit = []
@app.route("/", methods=["GET", "POST"])
def home():
   global commit
   if request.method == "POST":
      try:
         request.form['return']
         
         return render_template('index (3).html')
      except:
         pass
      try:
         predict["text"] = request.form["answer"]
      except:
         commit = [request.form["mail"], request.form["theme"], request.form["recipient"], request.form["theme_group"]]

         predict["text"] = ""
      if not predict["text"]:
         # return redirect(url_for("succesful"))
         request_comm = Request()
         [request_comm.mail, request_comm.theme, request_comm.recipient, request_comm.theme_group, request_comm.status] = commit + [False]
         db.session.add(request_comm)
         db.session.commit()
         commit = []
         return render_template('succesful.html')
      return render_template('index (3).html', answer=predict)
   return render_template('index (3).html')

# @app.route('/return')
# def confirm():
#    redirect(url_for("/"))

@app.route("/succesful")
def succesful():
   render_template("succesful.html")



if __name__ == "__main__":
   #app.run(host='0.0.0.0', port=7777)
   from waitress import serve
   serve(app, host='192.168.68.100', port=7777)