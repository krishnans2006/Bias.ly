from flask import Flask, request, g, redirect, url_for, render_template, jsonify
from data import get_data

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect(url_for("loading", news=request.form.get("news"), query=request.form.get("query")))
    return render_template("index.html")


@app.route("/loading/<string:news>/<string:query>")
def loading(news, query):
    return render_template("loading.html", news=news, query=query)


@app.route("/search/<string:news>/<string:query>")
def search(news, query):
    data = get_data(query, news)
    if not data:
        return render_template("search.html", expired=True)
    count = list(list(zip(*data))[1])
    sentiment = list(list(zip(*data))[0])
    # count = [21, 50, 50, 29, 34, 49, 40]
    # sentiment = [0.10730952380952383, 0.15153399999999995, 0.043225999999999994, -0.00440689655172415, -0.020402941176470596, 0.11016734693877547, 0.07317499999999999]
    print(count, sentiment)
    return render_template("search.html", query=query, count=count, sentiment=sentiment)  # add news


# @app.route("/data/<string:news>/<string:query>")
# def data(news, query):
#     return jsonify(get_data(news, query))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
