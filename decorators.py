from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Faça login para acessar esta página.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'usuario_id' not in session:
                flash('Faça login para acessar esta página.', 'danger')
                return redirect(url_for('auth.login'))
            if 'usuario_tipo' not in session or session['usuario_tipo'] not in roles:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return role_required('admin')(f)

def professor_required(f):
    return role_required('professor', 'admin')(f)

def aluno_required(f):
    return role_required('aluno', 'admin')(f)