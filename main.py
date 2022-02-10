from flask import Flask

app=Flask('TraficMonitor')

@app.route('/')
def index():
  return {"code": "<!DOCTYPE html>\n<html>\n  <head><title>GG</title></head>\n  <body><h1>abobe</h1></body>\n</html>"}

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
