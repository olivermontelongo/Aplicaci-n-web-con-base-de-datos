import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Base de datos interna rápida
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    detalle = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    todos = Registro.query.all()
    return render_template('index.html', registros=todos)

@app.route('/agregar', methods=['POST'])
def agregar():
    nuevo = Registro(nombre=request.form['nombre'], detalle=request.form['detalle'])
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    reg = Registro.query.get(id)
    return render_template('editar.html', r=reg)

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    reg = Registro.query.get(id)
    reg.nombre = request.form['nombre']
    reg.detalle = request.form['detalle']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    reg = Registro.query.get(id)
    db.session.delete(reg)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
