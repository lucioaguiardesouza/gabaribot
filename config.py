class Config:
    SECRET_KEY = 'minha_chave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./eduscan.db'  # <-- Note o ./ antes do nome
    SQLALCHEMY_TRACK_MODIFICATIONS = False