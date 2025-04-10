from flask import Flask, request, render_template

from lib.v1.lib_mongo import log_access, get_users
from lib.v1.lib_supab import query_usage
from lib.v1.lib_utils import html_db_data

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def root():
    if request.method == "POST":
        c_user = request.form.get('c_user')
        c_days = request.form.get('c_days')
        log_access({'email': c_user})
        users = get_users()
        if c_user.lower() in users:
            r_temp = html_db_data(render_template('/v1/index.html'), query_usage(int(c_days)), c_user.lower(), c_days)
            return r_temp
    return render_template('/v1/login.html')

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5001, debug = False)
