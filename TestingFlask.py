from flask import Flask , render_template
app = Flask (__name__)

@app.route("/")
@app.route("/MainHome")


def MainHome():
    return render_template("MainHome.html")
  


if __name__ == "__main__":

    app.run()
    