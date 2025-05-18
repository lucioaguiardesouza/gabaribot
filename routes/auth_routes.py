# Rotas de autenticação: cadastro, login, logout e exemplo de rota protegida

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """
    Rota para cadastro de novo usuário.
    """
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo = request.form['tipo']

        # Validação simples dos campos obrigatórios
        if not nome or not email or not senha or not tipo:
            flash('Todos os campos são obrigatórios!', 'danger')
            return render_template('cadastro.html')

        # Verifica se o e-mail já existe
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return render_template('cadastro.html')

        # Cria o usuário e salva no banco
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash, tipo=tipo)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota para login de usuário.
    """
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Busca o usuário pelo e-mail
        usuario = Usuario.query.filter_by(email=email).first()

        # Verifica se o usuário existe e a senha está correta
        if usuario and check_password_hash(usuario.senha_hash, senha):
            # Salva informações na sessão
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_tipo'] = usuario.tipo
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('E-mail ou senha inválidos!', 'danger')
            return render_template('login.html')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """
    Rota para logout do usuário.
    Remove os dados da sessão e redireciona para o login.
    """
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/pagina_protegida')
def pagina_protegida():
    """
    Exemplo de rota protegida: só acessa se estiver logado.
    """
    if 'usuario_id' not in session:
        flash('Faça login para acessar esta página.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('pagina_protegida.html')