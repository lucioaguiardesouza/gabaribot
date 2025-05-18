from flask import Flask, render_template
from config import Config
from extensions import db  # Importa o db do extensions.py

# Cria a aplicação Flask
app = Flask(__name__)

# Carrega as configurações do arquivo config.py
app.config.from_object(Config)

# Define a chave secreta da aplicação (usada para sessões e segurança)
app.secret_key = app.config['SECRET_KEY']

# Inicializa o banco de dados com a aplicação
db.init_app(app)

# Importa e registra o blueprint de autenticação
from routes.auth_routes import auth_bp
app.register_blueprint(auth_bp)

# Importa e registra o blueprint de alunos
from routes.aluno_routes import aluno_bp
app.register_blueprint(aluno_bp)

# Importa e registra o blueprint de professores
from routes.professor_routes import professor_bp
app.register_blueprint(professor_bp)

# Importa e registra o blueprint de provas
from routes.prova_routes import prova_bp
app.register_blueprint(prova_bp)

@app.route('/')
def index():
    return render_template('index.html')

# Rota About para o menu
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)