from flask import Flask, render_template, request

app = Flask(__name__)

USUARIO_VALIDO = "admin"
CONTRASEÑA_VALIDA = "miClave123"

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contraseña = request.form.get("contraseña")
        if usuario == USUARIO_VALIDO and contraseña == CONTRASEÑA_VALIDA:
            return render_template("Panel.html")
        else:
            return "Credenciales incorrectas"
    return '''
<form method="POST">
Usuario <input name="usuario"><br>
Contraseña <input type="password" name="contraseña"><br>
<button type="submit">Entrar</button>
</form>
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
