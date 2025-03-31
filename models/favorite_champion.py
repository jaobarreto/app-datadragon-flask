from models.database import db

class FavoriteChampion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        """Retorna um dicionário representando o campeão favorito"""
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title
        }
