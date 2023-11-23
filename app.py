from flask import Flask, request, render_template



app = Flask(__name__)

@app.route("/")
def home():
   return render_template('index.html')


if __name__ == "__main__":
#    app.run(host='192.168.68.100', port=7777)
   from waitress import serve
   serve(app, host='192.168.68.100', port=7777)