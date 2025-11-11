from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


def load_file(path):
    with open(path, "r") as fileobj:
        return json.load(fileobj)


@app.route('/')
def index():
    return render_template('index.html', posts=load_file("data_storage.json"))

@app.route("/add", methods =["GET", "POST"])
def add():
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        blogentries = load_file("data_storage.json")
        if len(blogentries) == 0:
            next_id = 1
        else:
            next_id = blogentries[-1]["id"] + 1

        new_data = {
            "id": next_id,
            "author":author,
            "title": title,
            "content":content
        }
        blogentries.append(new_data)

        with open("data_storage.json", "w") as fileobj:
            json.dump(blogentries, fileobj, indent= 2)
        return redirect(url_for('index'))
    return render_template("add.html")




@app.route("/delete/<int:post_id>")
def delete(post_id):
    blogentries = load_file("data_storage.json")
    blogentries = [entry for entry in blogentries if entry["id"] != post_id]
    with open("data_storage.json", "w") as fileobj:
        json.dump(blogentries, fileobj, indent=2)
    return redirect(url_for("index"))






if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

