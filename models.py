from extensions import db
from datetime import datetime

# ---------------------------
# Modelo de Usuário do sistema
# ---------------------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # professor, aluno, admin

    # Relacionamento com histórico de provas (auditoria)
    historicos_prova = db.relationship('HistoricoProva', backref='usuario', lazy=True)

# ---------------------------
# Modelo de Aluno
# ---------------------------
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    turma = db.Column(db.String(50), nullable=True)
    # Relacionamento com Usuario
    usuario = db.relationship('Usuario', backref=db.backref('aluno', uselist=False))

# ---------------------------
# Modelo de Professor
# ---------------------------
class Professor(db.Model):
    """
    Classe que representa um professor.
    Relaciona-se com a tabela Usuario.
    """
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    disciplina = db.Column(db.String(100), nullable=True)
    # Relacionamento com Usuario
    usuario = db.relationship('Usuario', backref=db.backref('professor', uselist=False))

# ---------------------------
# Modelo de Prova
# ---------------------------
class Prova(db.Model):
    """
    Classe que representa uma prova criada por um professor.
    """
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    disciplina = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)
    numero_questoes = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    # Relacionamento com Professor
    professor = db.relationship('Professor', backref=db.backref('provas', lazy=True))

# ---------------------------
# Modelo de Questão
# ---------------------------
class Questao(db.Model):
    """
    Classe que representa uma questão de uma prova.
    """
    id = db.Column(db.Integer, primary_key=True)
    prova_id = db.Column(db.Integer, db.ForeignKey('prova.id'), nullable=False)
    enunciado = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # multipla_escolha, verdadeiro_falso
    alternativas = db.Column(db.Text, nullable=True)  # Armazena alternativas em texto (JSON ou separado por ';')
    peso = db.Column(db.Float, nullable=True)

# ---------------------------
# Modelo de Gabarito
# ---------------------------
class Gabarito(db.Model):
    """
    Classe que representa o gabarito de uma questão.
    """
    id = db.Column(db.Integer, primary_key=True)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=False)
    resposta_correta = db.Column(db.String(10), nullable=False)

# ---------------------------
# Modelo de Histórico de Provas (Auditoria)
# ---------------------------
class HistoricoProva(db.Model):
    """
    Classe para registrar ações de auditoria sobre provas (criação e exclusão).
    """
    id = db.Column(db.Integer, primary_key=True)
    prova_id = db.Column(db.Integer, nullable=False)  # ID da prova afetada
    acao = db.Column(db.String(20), nullable=False)   # 'criada' ou 'excluida'
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Quem fez a ação
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Quando ocorreu

    def __repr__(self):
        return f'<HistoricoProva {self.id} - Prova {self.prova_id} - {self.acao} por Usuário {self.usuario_id} em {self.timestamp}>'