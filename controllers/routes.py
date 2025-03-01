import urllib.request
import json
from flask import render_template

def get_champions():
    url = 'https://ddragon.leagueoflegends.com/cdn/13.19.1/data/pt_BR/champion.json'
    with urllib.request.urlopen(url) as res:
        data = json.loads(res.read())
    return data['data']

def init_app(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/champions')
    def champions():
        champs_data = get_champions()
        return render_template('champions.html', champions=champs_data)

    @app.route('/champion/<champion_name>')
    def champion_info(champion_name):
        champs_data = get_champions()
        champion = champs_data.get(champion_name)

        if not champion:
            return "Campeão não encontrado", 404
        
        return render_template('infochamp.html', champion=champion)
