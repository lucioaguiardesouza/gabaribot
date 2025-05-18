from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Aluno, Usuario
from decorators import login_required, professor_required

aluno_bp = Blueprint('aluno', __name__)

@aluno_bp.route('/alunos')
@login_required
def listar_alunos():
    """
    Lista todos os alunos cadastrados.
    Apenas usuários logados podem acessar.
    """
    alunos = Aluno.query.all()
    return render_template('alunos.html', alunos=alunos)

@aluno_bp.route('/alunos/novo', methods=['GET', 'POST'])
@professor_required
def cadastrar_aluno():
    """
    Cadastro de novo aluno.
    Apenas professores e administradores podem acessar.
    """
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        matricula = request.form['matricula']
        turma = request.form['turma']

        # Verifica se o e-mail já existe na tabela Usuario
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return render_template('cadastrar_aluno.html')

        # Cria usuário e aluno
        from werkzeug.security import generate_password_hash
        senha_hash = generate_password_hash(senha)
        usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash, tipo='aluno')
        db.session.add(usuario)
        db.session.commit()

        aluno = Aluno(usuario_id=usuario.id, matricula=matricula, turma=turma)
        db.session.add(aluno)
        db.session.commit()

        flash('Aluno cadastrado com sucesso!', 'success')
        return redirect(url_for('aluno.listar_alunos'))

    return render_template('cadastrar_aluno.html')

@aluno_bp.route('/alunos/editar/<int:aluno_id>', methods=['GET', 'POST'])
@professor_required
def editar_aluno(aluno_id):
    """
    Edita os dados de um aluno.
    Apenas professores e administradores podem acessar.
    """
    aluno = Aluno.query.get_or_404(aluno_id)
    usuario = Usuario.query.get_or_404(aluno.usuario_id)

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        aluno.matricula = request.form['matricula']
        aluno.turma = request.form['turma']
        db.session.commit()
        flash('Aluno atualizado com sucesso!', 'success')
        return redirect(url_for('aluno.listar_alunos'))

    return render_template('editar_aluno.html', aluno=aluno, usuario=usuario)

@aluno_bp.route('/alunos/excluir/<int:aluno_id>', methods=['POST'])
@professor_required
def excluir_aluno(aluno_id):
    """
    Exclui um aluno e seu usuário associado.
    Apenas professores e administradores podem acessar.
    """
    aluno = Aluno.query.get_or_404(aluno_id)
    usuario = Usuario.query.get_or_404(aluno.usuario_id)
    db.session.delete(aluno)
    db.session.delete(usuario)
    db.session.commit()
    flash('Aluno excluído com sucesso!', 'success')
    return redirect(url_for('aluno.listar_alunos'))