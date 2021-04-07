import json

def populate(db, models, providers):
    ArticleProvider = providers.article_provider.ArticleProvider
    provider = ArticleProvider()
    with open('data/articles.json') as file:
        data = json.load(file)
        for datum in data:
            provider.add(datum)