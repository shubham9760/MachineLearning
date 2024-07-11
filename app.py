from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open(r"F:\Self Learning\Applied AI\Book Recommendation\popular.pkl", "rb"))
pt = pickle.load(open(r"F:\Self Learning\Applied AI\Book Recommendation\pt.pkl", "rb"))
books = pickle.load(open(r"F:\Self Learning\Applied AI\Book Recommendation\books.pkl", "rb"))
similarity_score = pickle.load(open(r"F:\Self Learning\Applied AI\Book Recommendation\similarity_score.pkl", "rb"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = popular_df["Book-Title"].values,
                           author = popular_df["Book-Author"].values,
                           image = popular_df["Image-URL-M"].values,
                           votes = popular_df["num_ratings"].values,
                           ratings = popular_df["avg_ratings"].values
                           )

@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html")

@app.route("/recommend_books", methods=["POST"])
def recommend():
    user_input = request.form.get("user_input")
    index = np.where(pt.index==user_input)[0][0]
    simmilar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
    data=[]
    for i in simmilar_items:
        item=[]
        temp_df = books[books["Book-Title"]==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))

        data.append(item)
    print(data)
    return render_template("recommend.html", data=data)