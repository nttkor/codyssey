from flask import Flask
app = Flask(__name__)   
@app.route('/')
def hello_world():
    return "Hello, DevOps!" 
# app.run(debug=False,host='0.0.0.0', port=80)  # This will run the Flask application not in debug mode 
app.run(debug=True,host='0.0.0.0',port=80)  # This will run the Flask application in debug mode on
