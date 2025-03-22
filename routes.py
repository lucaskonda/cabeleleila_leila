from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from database import db
from models import Agendamento

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        cliente = request.form['cliente']
        data_str = request.form['data_agendada']
        servicos = request.form['servicos']
        data_agendada = datetime.strptime(data_str, '%Y-%m-%d').date()

        inicio_semana = data_agendada - timedelta(days=data_agendada.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        agendamento_semana = Agendamento.query.filter(
            Agendamento.cliente == cliente,
            Agendamento.data_agendada.between(inicio_semana, fim_semana)
        ).first()

        if agendamento_semana:
            flash(f'Cliente já possui agendamento na semana. Deseja manter? Se não, altere a data.', 'warning')
            return redirect(url_for('app_routes.agendar'))

        novo_agendamento = Agendamento(cliente=cliente, data_agendada=data_agendada, servicos=servicos)
        db.session.add(novo_agendamento)
        db.session.commit()
        flash('Agendamento realizado com sucesso!', 'success')
        return redirect(url_for('app_routes.agendar'))

    return render_template('agendar.html')


@app_routes.route('/historico', methods=['GET', 'POST'])
def historico():
    agendamentos = []
    if request.method == 'POST':
        inicio = datetime.strptime(request.form['inicio'], '%Y-%m-%d').date()
        fim = datetime.strptime(request.form['fim'], '%Y-%m-%d').date()
        agendamentos = Agendamento.query.filter(Agendamento.data_agendada.between(inicio, fim)).all()

    return render_template('historico.html', agendamentos=agendamentos)


@app_routes.route('/operacional')
def operacional():
    agendamentos = Agendamento.query.all()
    return render_template('operacional.html', agendamentos=agendamentos)


@app_routes.route('/alterar/<int:agendamento_id>', methods=['GET', 'POST'])
def alterar(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    if request.method == 'POST':
        nova_data_str = request.form['data_agendada']
        nova_data = datetime.strptime(nova_data_str, '%Y-%m-%d').date()
        novos_servicos = request.form['servicos']

        if (agendamento.data_agendada - datetime.today().date()).days >= 2:
            agendamento.data_agendada = nova_data
            agendamento.servicos = novos_servicos
            db.session.commit()
            flash('Agendamento alterado com sucesso!', 'success')
            return redirect(url_for('app_routes.operacional'))
        else:
            flash('Alteração não permitida: menos de 2 dias para o agendamento.', 'error')
            return redirect(url_for('app_routes.operacional'))

    return render_template('alterar.html', agendamento=agendamento)


@app_routes.route('/confirmar/<int:agendamento_id>')
def confirmar(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    agendamento.status = 'Confirmado'
    db.session.commit()
    flash('Agendamento confirmado!', 'success')
    return redirect(url_for('app_routes.operacional'))


@app_routes.route('/relatorio')
def relatorio():
    hoje = datetime.today().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    agendamentos_semana = Agendamento.query.filter(
        Agendamento.data_agendada.between(inicio_semana, fim_semana)
    ).all()
    total = len(agendamentos_semana)

    return render_template('relatorio.html', inicio_semana=inicio_semana, fim_semana=fim_semana, total=total)
