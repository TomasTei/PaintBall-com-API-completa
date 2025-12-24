# TrabalhoAPentball
1) criar venv
python -m venv venv
venv\Scripts\activate   (Windows)  ou  source venv/bin/activate

2) instalar dependências
pip install -r requirements.txt

3) configurar .env (copiar .env.example para .env) e ajustar DATABASE_URL

4) rodar seed (gera admin e dados)
python seed.py

5) iniciar app
python app.py

6) acessar
http://127.0.0.1:5000

admin: adm@gmail.com / 123456  (seed cria admin; também há atalho hardcoded)
