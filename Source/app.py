from flask import Flask, flash, redirect, render_template, request, session, url_for
# from flask_session import Session
app = Flask(__name__)

# if app.config["DEBUG"]:
#     @app.after_request
#     def after_request(response):
#         response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#         response.headers["Expires"] = 0
#         response.headers["Pragma"] = "no-cache"
#         return response

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
