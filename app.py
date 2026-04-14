from flask import Flask, request, redirect, make_response

app = Flask(__name__)

def parse_profile(cookie):
    data = {}

    try:
        pairs = cookie.split("&")
        for pair in pairs:
            key, value = pair.split("=", 1)
            data[key] = value
    except:
        data = {"username": "guest", "role": "user"}

    return data

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "guest")

        profile = f"username={username}&role=user"

        response = make_response(redirect("/dashboard"))
        response.set_cookie("isAdmin", "false")
        response.set_cookie("profile", profile)

        return response

    return """
    <html>
    <head>
        <title>Cookie Confusion</title>
    </head>
    <body>
        <h2>Employee Login</h2>
        <form method="POST">
            <input name="username" placeholder="Username"><br><br>
            <input name="password" type="password" placeholder="Password"><br><br>
            <button type="submit">Login</button>
        </form>
        <!-- Not every cookie is equally important -->
    </body>
    </html>
    """

@app.route("/dashboard")
def dashboard():
    profile_cookie = request.cookies.get("profile", "")
    profile = parse_profile(profile_cookie)

    return f"""
    <html>
    <head>
        <title>Dashboard</title>
    </head>
    <body>
        <h2>Welcome, {profile.get("username")}</h2>
        <p>Role: {profile.get("role")}</p>
        <p><a href="/admin">Go to Admin Panel</a></p>
    </body>
    </html>
    """

@app.route("/admin")
def admin():
    profile_cookie = request.cookies.get("profile", "")
    profile = parse_profile(profile_cookie)

    if profile.get("role") == "admin":
        return """
        <html>
        <head>
            <title>Admin Panel</title>
        </head>
        <body>
            <h1>Access Granted</h1>
            <p>FLAG{cookie_tampering_success}</p>
        </body>
        </html>
        """

    return """
    <html>
    <head>
        <title>Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>You must be an admin to access this page.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
