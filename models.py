from database import db

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    data_agendada = db.Column(db.Date, nullable=False)
    servicos = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='Pendente')

    def __repr__(self):
        return f'<Agendamento {self.cliente} - {self.data_agendada}>'
