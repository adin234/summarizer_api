# Import global context
from flask import request

# Import flask dependencies
from flask import Blueprint

from lib.response import Response

from textteaser.parser import Parser
from goose import Goose
from textteaser import TextTeaser

# Import app-based dependencies
# from app import article

# Define the blueprint: 'article', set its url prefix: app.url/article
mod_article = Blueprint('article', __name__)

# Declare all the routes
@mod_article.route('/', methods=['GET'])
def get_article():
    parser = Parser()
    res = Response()
    g = Goose();
    tt = TextTeaser();

    url = request.args.get('url')
    article = g.extract(url=url);
    sentences = parser.splitSentences(article.cleaned_text)

    num_sentences = len(sentences)/10

    if num_sentences < 5:
        num_sentences = 5

    if request.args.get('num_sentences'):
        num_sentences = int(request.args.get('num_sentences'))

    params = {
        'title'         : article.title,
        'summarized'    : tt.summarize(article.title, article.cleaned_text, "Undefined", "Undefined", num_sentences)
    }

    return res.send(params)
