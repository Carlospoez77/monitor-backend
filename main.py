import os
from flask import Flask, request

app = Flask(__name__)

USUARIO_VALIDO = "admin"
CONTRASEÑA_VALIDA = "miClave123"

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contraseña = request.form.get("contraseña")
        if usuario == USUARIO_VALIDO and contraseña == CONTRASEÑA_VALIDA:
            return "<h1>✅ ¡ENTRASTE CORRECTAMENTE!</h1>"
        else:
            return "<h1>❌ Credenciales incorrectas</h1>"
    return '''
<h2>Iniciar Sesión</h2>
<form method="POST">
Usuario <input name="usuario"><br><br>
Contraseña <input type="password" name="contraseña"><br><br>
<button type="submit">Entrar</button>
</form>
'''

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
