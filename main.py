from flask import Flask, jsonify, request
from storage import allArticles, liked_articles, not_liked_articles
from demo import output
from content import get_recommendations

app = Flask(__name__)

@app.route("/getArticle")
def getArticle():
    MovieData = {
        "url": allArticles[0][11],
        "title": allArticles[0][12],
        "text": allArticles[0][13],
        "lang": allArticles[0][14],
        "total_events": allArticles[0][15]
    }
    return jsonify({
        "data": MovieData,
        "status": "success"
    })

@app.route("/likedArticle", methods=["POST"])
def likedArticles():
    article = allArticles[0]
    liked_articles.append(article)
    allArticles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unlikedArticle", methods=["POST"])
def unlikedArticles():
    article = allArticles[0]
    not_liked_articles.append(article)
    allArticles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popularArticle")
def popularArticles():
    ArticleData = []
    for article in output:
        _d = {
            "url": article[0],
            "title": article[1],
            "text": article[2],
            "lang": article[3],
            "total_events": article[4]
        }
        ArticleData.append(_d)
    return jsonify({
        "data": ArticleData,
        "status": "success"
    }), 200

@app.route("/recommendedArticle")
def recommendedArticles():
    recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[4])
        for data in output:
            recommended.append(data)
    import itertools
    recommended.sort()
    recommended = list(recommended for recommended,_ in itertools.groupby(recommended))
    ArticleData = []
    for recommended in recommended:
        d = {
            "url": recommended[0],
            "title": recommended[1],
            "text": recommended[2],
            "lang": recommended[3],
            "total_events": recommended[4]
        }
        ArticleData.append(d)
    return jsonify({
        "data": ArticleData,
        "status": "success"
    }), 200

if __name__ == "__main__":
    app.run()