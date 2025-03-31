import urllib.request
import json
from flask import render_template, request, jsonify, redirect, url_for
from models.favorite_champion import FavoriteChampion
from models.database import db

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

    @app.route('/favorites', methods=['POST'])
    def add_favorite():
        data = request.json
        if not data or 'name' not in data or 'title' not in data:
            return jsonify({"error": "Nome e título são obrigatórios"}), 400

        # Verifica se o campeão já está salvo
        if FavoriteChampion.query.filter_by(name=data['name']).first():
            return jsonify({"error": "Campeão já favoritado"}), 409

        new_champion = FavoriteChampion(name=data['name'], title=data['title'])
        db.session.add(new_champion)
        db.session.commit()
        return jsonify({"message": "Campeão favoritado!", "champion": new_champion.to_dict()}), 201

    @app.route('/favorites', methods=['GET'])
    def get_favorites():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)  # padrão de 5 por página

        paginated_favorites = FavoriteChampion.query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('list_favorites.html', 
                               favorites=paginated_favorites.items, 
                               total=paginated_favorites.total, 
                               pages=paginated_favorites.pages, 
                               current_page=paginated_favorites.page)

    @app.route('/favorites/add', methods=['GET', 'POST'])
    def add_favorite_view():
        if request.method == 'POST':
            name = request.form['name']
            title = request.form['title']
            new_favorite = FavoriteChampion(name=name, title=title)
            db.session.add(new_favorite)
            db.session.commit()
            return redirect(url_for('get_favorites'))  # redireciona para a lista de favoritos
        return render_template('add_favorite.html')

    @app.route('/favorites/<int:id>/edit', methods=['GET', 'POST'])
    def edit_favorite(id):
        favorite = FavoriteChampion.query.get_or_404(id)
        if request.method == 'POST':
            favorite.name = request.form['name']
            favorite.title = request.form['title']
            db.session.commit()
            return redirect(url_for('get_favorites'))  # redireciona para a lista de favoritos
        return render_template('edit_favorite.html', champion=favorite)

    @app.route('/favorites/<int:id>/delete', methods=['GET', 'POST'])
    def delete_favorite(id):
        favorite = FavoriteChampion.query.get_or_404(id)
        
        if request.method == 'POST':
            db.session.delete(favorite)
            db.session.commit()
            
            return render_template('delete_favorite.html', champion=favorite, deleted=True)

        return render_template('delete_favorite.html', champion=favorite, deleted=False)

    @app.route('/favorites/<int:champion_id>', methods=['PUT'])
    def update_favorite(champion_id):
        champion = FavoriteChampion.query.get_or_404(champion_id)
        data = request.json

        if "name" in data:
            champion.name = data["name"]
        if "title" in data:
            champion.title = data["title"]

        db.session.commit()
        return jsonify({"message": "Campeão atualizado!", "champion": champion.to_dict()})

    @app.route('/favorites/<int:champion_id>', methods=['DELETE'])
    def delete_favorite_api(champion_id):
        champion = FavoriteChampion.query.get_or_404(champion_id)
        db.session.delete(champion)
        db.session.commit()
        return jsonify({"message": "Campeão removido dos favoritos!"})
