from flask import Flask, request, render_template

from lib.v1.lib_mongo import log_access, get_users

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def root():
    # users = get_users()
    # print(f'{users = }')
    if request.method == "POST":
        c_user = request.form.get('c_user')
        log_access({'email': c_user})
        users = get_users()
        # print(f'{c_user = }, {users = }')
        if c_user.lower() in users:
            return render_template('/v1/index.html')
    return render_template('/v1/login.html')

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5001, debug = True)
