import os, flask, threading, base64, datetime
from flask import Flask, render_template, make_response, redirect, request

app=Flask(__name__)
comming_soon=redirect("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4g2xq07HFCVAo-jnoY1LNpQQ5IsX__ko94MQP4inESCott-gizRUHJm5_m0y5e-n6K-o&usqp=CAU", 307)

def log(text):
  text = str(text)
  try:
    prev_log = open("logs.log","r").read()
    if prev_log == "":
      prev_log = "[???]: LOGS WAS CLEARED"
  except:
    prev_log = "[???]: LOGS WAS CLEARED"
  time=datetime.datetime.utcnow() + datetime.timedelta(hours = 3)
  open("logs.log", "w").write(prev_log + f"""
    <br>
    [{time.strftime("%d/%m/%Y %H:%M:%S")}]:  {text}
    <br>""")

@app.route('/')
def index():
  log("Кто-то зашел на главную страницу")
  return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
  return open("favicon.ico","rb").read()

@app.route("/uptime")
def uptime():
  return "1"

@app.route("/download")
def download_redirect():
  return redirect("/#download", 301)

@app.route("/download/<string:filetype>")
def downloader(filetype):
  return comming_soon

def run():
  app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
  run()
#  threading.Thread(target=run).start()
