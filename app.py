from flask import Flask, render_template, redirect, url_for, request
from GPTData.main.gptsql import gpts

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("website.html")


@app.route("/process_form", methods=['POST'])
def process_form():
    if request.method == 'POST':
        filename = request.form.get('filename')
        if filename:
            return redirect(url_for('analysis'))
    return "Error: Invalid form submission or missing filename"


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

@app.route("/process_query", methods=["POST"])
def process_query():
    if request.method == "POST":
        query = request.form.get('query')
        print("ba")
        gpt = gpts()
        ra = gpt.do(query)
        print(ra)
        if query:
            return render_template('analysis.html', query=query, answer=ra)
    return("Error: Missing query")

@app.route("/info")
def info():
    return render_template("info.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
