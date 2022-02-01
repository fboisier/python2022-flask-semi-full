from flask import Flask, render_template, request , redirect , session, flash
from settings import Config, connectToMySQL
from utils import lg

app = Flask(__name__)    # Crea una nueva instancia de la clase Flask llamada "app"
app.secret_key = Config.SECRET_KEY

@app.route('/inicio')
def inicio():

    if 'usuario' not in session:
        flash('NO estas logeado. Tienes que ingresar tu contraseña','error')
        return redirect("/login")

    return render_template('inicio.html')

@app.route('/login')
def login():

    if 'usuario' in session:
        flash('Ya estas logeado. Para salir deber ir al boton salir.','error')
        return redirect("/")

    return render_template('login.html')

@app.route('/')
def index():
    return redirect('/inicio')


@app.route('/login_procesar', methods=['POST'])
def login_procesar():
    lg("POST: ", request.form)
    
    if request.form['password'] != '1234':
        flash('Contraseña Mala. No es 1234','error')
        return redirect('/login')


    session['usuario'] = request.form['email']
    flash('Logeado Correctamente.','success')
    return redirect('/inicio')

@app.route('/logout')
def logout():

    if 'usuario' in session:
        session.pop('usuario')

    return redirect('/inicio')


@app.route('/basedato')
def basedato():
    
    if 'usuario' not in session:
        flash('NO estas logeado. Tienes que ingresar tu contraseña','error')
        return redirect("/login")

    mysql = connectToMySQL('first_flask')	        # call the function, passing in the name of our db
    friends = mysql.query_db('SELECT * FROM friends;')  # call the query_db function, pass in the query as a string
    print(friends)

    flash("Conectado a la base exitosamente. Ver LOG", "info")
    return render_template('amigos.html', all_friends = friends)
    

if __name__=="__main__":   # Asegúrese de que este archivo se ejecute directamente y no desde un módulo diferente
    app.run(debug=Config.DEBUG,port=Config.PORT)