from flask import Flask, render_template, request
import requests
import smtplib
import os

response = requests.get('https://api.npoint.io/88c2c1f644ef334058be')
response.raise_for_status()
raw_data = response.json()

Email = os.environ.get('email')
Password = os.environ.get('password')

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def get_all_posts(data=raw_data):
    return render_template("index.html", data=data)


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact_page():
    if request.method == 'GET':
        return render_template('contact.html', text="Contact Me")
    else:
        data = request.form
        send_email(data['Name'], data['Email'], data['Number'], data['Message'])
        return render_template('contact.html', text="Successfully Sent Your Message")


@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for post in raw_data:
        if post['id'] == index:
            requested_post = post
    return render_template('post.html', post=requested_post)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(Email, Password)
        connection.sendmail(Email, Password, email_message)


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5001)
