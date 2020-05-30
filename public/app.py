from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'images/icon.ico')
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/developer")
def dev():
    return render_template("developer.html")