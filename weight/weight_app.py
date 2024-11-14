from flask import Flask

app = Flask(__name__)

@app.get("/health")
def is_healthy():
    return "OK", 200

@app.get("/weight")
def get_weight():
    return "In Process", 200

if __name__=="__main__":
    app.run()