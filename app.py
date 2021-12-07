import os
from flask import Flask, request, render_template, redirect, url_for
print(os.path)

from src.Search.SearchApp import SearchTerm

# creates the flask
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    query = request.form['query'].lower()
    if len(query) == 0:
        return render_template('index.html')

    print('querying', query)

    search_results = SearchTerm(query)
    total_results = len(search_results)
    page_no = 0

    return render_template('results.html', search_results=search_results, num_results=total_results, query=query, page_no=page_no, total_results=total_results)
