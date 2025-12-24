from flask import Flask, render_template, request, redirect, url_for, flash, session as flask_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from modelo import Agendamento, Base, Produtos, Espacos, Pacotes, Usuario
import os
from dotenv import load_dotenv
from functools import wraps

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Banco de dados SQL
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
print('criando tabela')
Base.metadata.create_all(engine)
print('tabela adicionada')
Session = sessionmaker(bind=engine)
session = Session()

#----------------- barrar acesso ----------------

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper

# -------------------- ROTAS --------------------

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/servicos')
def addServico():
    return render_template('addServico.html')
@app.route('/consultar')
@login_required
def consultar():
    return render_template('consultar.html')
@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        data = request.form['data']        # Vem como string 'YYYY-MM-DD'
        hora = request.form['hora']        # Vem como string 'HH:MM'
        servico = request.form['servico']
        jogadores = int(request.form['jogadores'])

        # Cria um novo objeto Agendamento
        novo_agendamento = Agendamento(
            nome=nome,
            data=data,
            hora=hora,
            servico=servico,
            jogadores=jogadores
        )

        # Salva no banco
        session.add(novo_agendamento)
        session.commit()

        # Redireciona para a página de agendamentos
        return redirect(url_for('mostrar_agendamentos'))

    # Se for GET, só renderiza a página do formulário
    return render_template('agendar.html')

@app.route('/agendamentos.html')
def mostrar_agendamentos():
    agendamentos = session.query(Agendamento).all()
    return render_template('agendamentos.html', agendamentos=agendamentos)

@app.route('/agendamento/editar/<int:id>', methods=['GET', 'POST'])
def editar_agendamento(id):
    ag = session.query(Agendamento).get(id)
    if request.method == 'POST':
        ag.nome = request.form['nome']
        ag.data = request.form['data']
        ag.hora = request.form['hora']
        ag.servico = request.form['servico']
        ag.jogadores = request.form['jogadores']
        session.commit()
        return redirect(url_for('mostrar_agendamentos'))
    return render_template('editar_agendamento.html', agendamento=ag)

# Deletar agendamento
@app.route('/agendamento/deletar/<int:id>')
def deletar_agendamento(id):
    ag = session.query(Agendamento).get(id)
    session.delete(ag)
    session.commit()
    return redirect(url_for('mostrar_agendamentos'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = Session()

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = db.query(Usuario).filter_by(email=email, senha=senha).first()

        if usuario:
            flask_session['usuario_id'] = usuario.id
            flask_session['usuario_nome'] = usuario.nome
            return redirect(url_for('index'))

        return render_template('login.html', mensagem='E-mail ou senha incorretos!')

    return render_template('login.html')



#------------------------------

#------------------------------

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    db = Session()  # IMPORTANTE: não usar session aqui!

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Verifica se já existe email
        existe = db.query(Usuario).filter_by(email=email).first()
        if existe:
            return render_template("cadastrarUser.html", mensagem="E-mail já cadastrado!")

        # Cria o usuário
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.add(novo_usuario)
        db.commit()

        # Redireciona corretamente
        return redirect(url_for('index'))

    return render_template('cadastrarUser.html')

@app.route('/usuarios')
def usuarios():
    db = Session()
    usuarios = db.query(Usuario).all()
    return render_template('usuarios.html', usuarios=usuarios)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/index')


# Rotas CRUD de Produtos
@app.route('/produto/add', methods=['GET','POST'])
def add_produto():
    nome = request.form['nome_produto']
    preco = float(request.form['preco'])
    novo = Produtos(nome_produto=nome, preco=preco)
    session.add(novo)
    session.commit()
    flash("Produto adicionado!", "success")
    return redirect(url_for('cadastro'))

# Rotas CRUD de Espaços
@app.route('/espaco/add', methods=['POST'])
def add_espaco():
    nome = request.form['nome_espaco']
    preco = float(request.form['preco_espaco'])
    local = request.form['localizacao']
    novo = Espacos(nome=nome, preco=preco, localizacao=local)
    session.add(novo)
    session.commit()
    flash("Espaço adicionado!", "success")
    return redirect(url_for('cadastro'))

# Rotas CRUD de Pacotes
@app.route('/pacote/add', methods=['POST'])
def add_pacote():
    nome = request.form['nome_pacote']
    preco_total = float(request.form['preco_total'])
    produto_id = int(request.form['produto_id'])
    espaco_id = int(request.form['espaco_id'])
    novo = Pacotes(nome_pacote=nome, preco_total=preco_total, produto_id=produto_id, espaco_id=espaco_id)
    session.add(novo)
    session.commit()
    flash("Pacote adicionado!", "success")
    return redirect(url_for('cadastro'))
    

if __name__ == '__main__':
    app.run(debug=True)