import os, flask, threading, base64, datetime
from flask import Flask, render_template, make_response, redirect, request

app=Flask(__name__)
comming_soon=redirect("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4g2xq07HFCVAo-jnoY1LNpQQ5IsX__ko94MQP4inESCott-gizRUHJm5_m0y5e-n6K-o&usqp=CAU", 307)

def log(text):
  text = str(text)
  try:
    prev_log = open("logs.log","r").read()
  except:
    prev_log = "LOGS WAS CLEARED"
  time=datetime.datetime.utcnow() + datetime.timedelta(hours = 3)
  open("logs.log", "w").write(prev_log + f"""\n
[{time.strftime("%d/%m/%Y %H:%M:%S")}]:  {text}
""")

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

@app.route("/api/folders", methods=["POST"])
def create_folder():
  if not request.json or not "password" in request.json:
    log("Некоректный запрос post api/folders")
    return flask.abort(400)
  id=1
  for fid in os.listdir("folders"):
    try:
      if int(fid) >= id:
        id = int(fid)+1
    except:
      pass
  os.mkdir(f"folders/{id}")
  open(f"folders/{id}/.password.txt","w").write(request.json["password"].strip())
  log(f"Создана папка id: {id}, пароль: {request.json['password'].strip()}")
  return make_response({"id": id}, 201)

@app.route("/api/folders/<string:folderid>", methods = ["PATCH", "DELETE", "GET"])
def folder(folderid):
  try:
    if request.method == "GET":
      try:
        resp=os.listdir(f"folders/{folderid}")
        resp.remove(".password.txt")
        psw=open(f"folders/{folderid}/.password.txt","r").read().strip()
        if not request.json or not "password" in request.json or str(request.json["password"]).strip() != psw:
          resp=make_response("Invalid password", 401)
      except:
        resp=flask.abort(404)
      log(f"Запрошена информация о папке {folderid}")
      return resp
    elif request.method == "PATCH":
      if not request.json:
        return flask.abort(400)
      req_json=request.json
      try:
        psw=open(f"folders/{folderid}/.password.txt","r").read().strip()
      except:
        return flask.abort(404)
      if not "password" in req_json or str(req_json["password"]).strip() != psw:
        return make_response("Invalid password", 401)
      del req_json["password"]
      updated=""
      for fn in req_json:
        if fn != ".password.txt":
          updated+=f"\n{fn}"
          if req_json[fn]:
            open(f"folders/{folderid}/{fn}","wb").write(base64.b64decode(bytes(req_json[fn])))
          else:
            os.remove(f"folders/{folderid}/{fn}")
      log(f"Обновлена папка {folderid}, обновленые файлы: {updated}")
      return flask.abort(201)
    elif request.method == "DELETE":
      req_json=request.json
      try:
        psw=open(f"folders/{folderid}/.password.txt","r").read().strip()
      except:
        return flask.abort(404)
      if not "password" in req_json or str(req_json["password"]).strip() != psw:
        return make_response("Invalid password", 401)
      files=os.listdir(f"folder/{folderid}")
      files.remove(".password.txt")
      files=str(files)[2:-2].replace('" ,', ' ,')
      os.system(f"rm folder/{folderid} -r")
      log(f"Удалена папка {folderid}, содержала {files}")
      return flask.abort(202)
  except:
    flask.abort(404)

@app.route("/cdn/<string:filename>")
def cdn_file(filename):
  try:
    resp = make_response(open(f"cdn/{filename}", "rb").read(), 200)
    if filename.endswith(".js"):
      resp.headers['Content-Type'] = 'text/javascript'
    if filename.endswith(".css"):
      resp.headers['Content-Type'] = 'text/css'
  except:
    resp = flask.abort(404)
  return resp

@app.route("/admin/<string:password>/<string:cmd>", methods = ["GET", "POST", "PUT"])
def admin_exec(password, cmd):
  if password != os.getenv("admin_password"):
    return flask.abort(403)
  if not cmd:
    return flask.abort(400)
  if cmd in ["logs", "view logs", "view_logs", "log"]:
    log("АДМИН: запрос логов")
    try:
      logs=open("logs.log", "r").read()
    except:
      logs="NO LOGS"
    return logs
  code=base64.b64decode(cmd).decode().strip()
  threading.Thread(target=exec, args=(code, {**globals(), **locals()})).start()
  log(f"АДМИН: выполнить {code}")
  return make_response("Code has been launched", 202)

def run():
  app.run(host="0.0.0.0", port=2288)

if __name__ == "__main__":
  run()
#  threading.Thread(target=run).start()
