from flask import Flask
app = Flask(__name__)   
@app.route('/')
def hello_world():
    return "Hello, DevOps!" 
app.run(debug=True,port=80)  # This will run the Flask application in debug mode