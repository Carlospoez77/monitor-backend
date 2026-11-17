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
            return '''
            <h1 style="color:green">✅ PANEL DE MONITOREO</h1>
            <p>Plataforma de vigilancia y control de tus agentes y servicios</p>
            <hr>
            <h3>📊 Secciones disponibles</h3>
            <ul>
                <li>Estado de agentes activos</li>
                <li>Registro de actividades</li>
                <li>Consumo de créditos</li>
                <li>Logs y alertas</li>
            </ul>
            '''
        else:
            return "<h1 style='color:red'>❌ Credenciales incorrectas</h1>"
    return '''
    <h2>Iniciar Sesión — Panel de Monitoreo</h2>
    <form method="POST">
    Usuario: <input name="usuario" value="admin"><br><br>
    Contraseña: <input type="password" name="contraseña"><br><br>
    <button type="submit">Entrar</button>
    </form>
    '''

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
