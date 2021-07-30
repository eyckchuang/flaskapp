from flask import current_app as app
from flask import render_template


@app.route('/')
def index():
    # form = AdmissionForm()
    # return render_template("admission.html", form=form)
    return render_template("index.html")
