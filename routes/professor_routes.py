from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Professor, Usuario
from decorators import login_required, admin_required

professor_bp = Blueprint('professor', __name__)

@professor_bp.route('/professores')
@login_required
def listar_professores():
    """
    Lista todos os professores cadastrados.
    Apenas usuários logados podem acessar.
    """
    professores = Professor.query.all()
    return render_template('professores.html', professores=professores)

@professor_bp.route('/professores/novo', methods=['GET', 'POST'])
@admin_required
def cadastrar_professor():
    """
    Cadastro de novo professor.
    Apenas administradores podem acessar.
    """
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        disciplina = request.form['disciplina']

        # Verifica se o e-mail já existe na tabela Usuario
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return render_template('cadastrar_professor.html')

        # Cria usuário e professor
        from werkzeug.security import generate_password_hash
        senha_hash = generate_password_hash(senha)
        usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash, tipo='professor')
        db.session.add(usuario)
        db.session.commit()

        professor = Professor(usuario_id=usuario.id, disciplina=disciplina)
        db.session.add(professor)
        db.session.commit()

        flash('Professor cadastrado com sucesso!', 'success')
        return redirect(url_for('professor.listar_professores'))

    return render_template('cadastrar_professor.html')

@professor_bp.route('/professores/editar/<int:professor_id>', methods=['GET', 'POST'])
@admin_required
def editar_professor(professor_id):
    """
    Edita os dados de um professor.
    Apenas administradores podem acessar.
    """
    professor = Professor.query.get_or_404(professor_id)
    usuario = Usuario.query.get_or_404(professor.usuario_id)

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        professor.disciplina = request.form['disciplina']
        db.session.commit()
        flash('Professor atualizado com sucesso!', 'success')
        return redirect(url_for('professor.listar_professores'))

    return render_template('editar_professor.html', professor=professor, usuario=usuario)

@professor_bp.route('/professores/excluir/<int:professor_id>', methods=['POST'])
@admin_required
def excluir_professor(professor_id):
    """
    Exclui um professor e seu usuário associado.
    Apenas administradores podem acessar.
    """
    professor = Professor.query.get_or_404(professor_id)
    usuario = Usuario.query.get_or_404(professor.usuario_id)
    db.session.delete(professor)
    db.session.delete(usuario)
    db.session.commit()
    flash('Professor excluído com sucesso!', 'success')
    return redirect(url_for('professor.listar_professores'))