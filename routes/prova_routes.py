from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from models import Prova, Professor, Usuario, HistoricoProva
from datetime import datetime

prova_bp = Blueprint('prova', __name__)

@prova_bp.route('/provas')
def listar_provas():
    """
    Lista todas as provas cadastradas.
    Apenas usuários logados podem acessar.
    """
    if 'usuario_id' not in session:
        flash('Faça login para acessar esta página.', 'danger')
        return redirect(url_for('auth.login'))
    provas = Prova.query.all()
    return render_template('provas.html', provas=provas)

@prova_bp.route('/provas/nova', methods=['GET', 'POST'])
def cadastrar_prova():
    """
    Cadastro de nova prova.
    Apenas professores podem cadastrar provas.
    Registra no histórico quem criou a prova.
    """
    if 'usuario_id' not in session:
        flash('Faça login para acessar esta página.', 'danger')
        return redirect(url_for('auth.login'))

    # Só professores podem cadastrar provas
    usuario = Usuario.query.get(session['usuario_id'])
    if usuario.tipo != 'professor':
        flash('Apenas professores podem cadastrar provas.', 'danger')
        return redirect(url_for('prova.listar_provas'))

    professor = Professor.query.filter_by(usuario_id=usuario.id).first()
    if not professor:
        flash('Seu usuário não está vinculado a um cadastro de professor. Solicite ao administrador.', 'danger')
        return redirect(url_for('prova.listar_provas'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        disciplina = request.form['disciplina']
        data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        numero_questoes = int(request.form['numero_questoes'])
        valor_total = float(request.form['valor_total'])

        # Cria a prova
        prova = Prova(
            titulo=titulo,
            disciplina=disciplina,
            data=data,
            numero_questoes=numero_questoes,
            valor_total=valor_total,
            professor_id=professor.id
        )
        db.session.add(prova)
        db.session.commit()

        # Registra no histórico a criação da prova
        historico = HistoricoProva(
            prova_id=prova.id,
            acao='criada',
            usuario_id=usuario.id
        )
        db.session.add(historico)
        db.session.commit()

        flash('Prova cadastrada com sucesso!', 'success')
        return redirect(url_for('prova.listar_provas'))

    return render_template('cadastrar_prova.html')

@prova_bp.route('/provas/editar/<int:prova_id>', methods=['GET', 'POST'])
def editar_prova(prova_id):
    """
    Edita os dados de uma prova.
    Apenas usuários logados podem acessar.
    """
    if 'usuario_id' not in session:
        flash('Faça login para acessar esta página.', 'danger')
        return redirect(url_for('auth.login'))

    prova = Prova.query.get_or_404(prova_id)

    if request.method == 'POST':
        prova.titulo = request.form['titulo']
        prova.disciplina = request.form['disciplina']
        prova.data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        prova.numero_questoes = int(request.form['numero_questoes'])
        prova.valor_total = float(request.form['valor_total'])
        db.session.commit()
        flash('Prova atualizada com sucesso!', 'success')
        return redirect(url_for('prova.listar_provas'))

    return render_template('editar_prova.html', prova=prova)

@prova_bp.route('/provas/excluir/<int:prova_id>', methods=['POST'])
def excluir_prova(prova_id):
    """
    Exclui uma prova.
    Apenas professores podem excluir provas.
    Registra no histórico quem excluiu a prova.
    """
    if 'usuario_id' not in session:
        flash('Faça login para acessar esta página.', 'danger')
        return redirect(url_for('auth.login'))

    usuario = Usuario.query.get(session['usuario_id'])
    if usuario.tipo != 'professor':
        flash('Apenas professores podem excluir provas.', 'danger')
        return redirect(url_for('prova.listar_provas'))

    prova = Prova.query.get_or_404(prova_id)

    # Registra no histórico a exclusão da prova
    historico = HistoricoProva(
        prova_id=prova.id,
        acao='excluida',
        usuario_id=usuario.id
    )
    db.session.add(historico)
    db.session.delete(prova)
    db.session.commit()
    flash('Prova excluída com sucesso!', 'success')
    return redirect(url_for('prova.listar_provas'))

@prova_bp.route('/provas/historico')
def historico_provas():
    """
    Lista o histórico de criação e exclusão de provas para auditoria.
    Apenas usuários logados podem acessar.
    """
    if 'usuario_id' not in session:
        flash('Faça login para acessar esta página.', 'danger')
        return redirect(url_for('auth.login'))

    historicos = HistoricoProva.query.order_by(HistoricoProva.timestamp.desc()).all()
    return render_template('historico_provas.html', historicos=historicos)