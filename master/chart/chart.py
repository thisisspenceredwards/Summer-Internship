from flask import Flask, render_template, jsonify, request, g


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
