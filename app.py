from flask import Flask, render_template, request, redirect , url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)



# MYSQL Conection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2008'
app.config['MYSQL_DB'] = 'portafolio'
mysql = MySQL(app)



#settings

app.secret_key = 'mysecretkey'




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Debes iniciar sesión para acceder a esta página')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM habilidades')
    data = cur.fetchall()
    return render_template('index.html', habilidades=data)

@app.route('/')
def index2():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM habilidades')
    data = cur.fetchall()
    return render_template('index2.html', habilidades=data)


@app.route('/add_habilidad', methods=['POST'])
@login_required
def add_habilidad():
    if request.method == 'POST':
        NOMBRE = request.form['NOMBRE']
        DESCRIPCION = request.form['DESCRIPCION']
        TECNOLOGIAS = request.form['TECNOLOGIAS']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO habilidades (NOMBRE, DESCRIPCION, TECNOLOGIAS) VALUES (%s, %s, %s)',
                    (NOMBRE, DESCRIPCION, TECNOLOGIAS))
        mysql.connection.commit()
        flash('habilidad añadida satisfactoriamente')
        return redirect(url_for('index'))

@app.route('/edit_habilidad/<ID>')
@login_required
def get_habilidad(ID):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM habilidades WHERE ID = %s', (ID,))
    data = cur.fetchall()
    return render_template('edit-habilidades.html', habilidad = data[0])

@app.route('/update_habilidad/<ID>', methods=['POST'])
@login_required
def update_habilidad(ID):
    if request.method == 'POST':
        NOMBRE = request.form['NOMBRE']
        DESCRIPCION = request.form['DESCRIPCION']
        TECNOLOGIAS = request.form['TECNOLOGIAS']
    cur=mysql.connection.cursor()
    cur.execute("""
     UPDATE habilidades
    SET NOMBRE = %s,
        DESCRIPCION = %s,
        TECNOLOGIAS = %s
    WHERE ID = %s                     
    """, (NOMBRE, DESCRIPCION, TECNOLOGIAS, ID))
    mysql.connection.commit()
    flash('habilidad actualizada satisfactoriamente')
    return redirect(url_for('index'))

@app.route('/delete_habilidad/<ID>')
@login_required
def delete_habilidad(ID):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM habilidades WHERE ID ={0}'.format(ID))
    mysql.connection.commit()
    flash('habilidad removida satisfactoriamente')
    return redirect (url_for('index'))
















@app.route('/biografia')
@login_required
def biografia():
    return render_template('biografia.html')

@app.route('/proyecto')
@login_required
def proyecto():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proyectos')
    data = cur.fetchall()
    return render_template('proyecto.html', proyectos = data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user[2], password):  # user[2] es el password
            session['logged_in'] = True
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['id_rol'] = user[5]

            if session['id_rol']== 1:
                flash('Inicio de sesión exitoso')
                return render_template('index2.html')
            elif session['id_rol']== 2:
                flash('Inicio de sesión exitoso')
                return redirect(url_for('contacto'))
        else:
            flash('Usuario o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # Hash de la contraseña
        hashed_password = generate_password_hash(password)
        
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO usuarios (username, password, email) VALUES (%s, %s, %s)',
                       (username, hashed_password, email))
            mysql.connection.commit()
            cur.close()
            flash('Registro exitoso. Ahora puedes iniciar sesión')
            return redirect(url_for('login'))
        except:
            flash('El usuario ya existe')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente')
    return redirect(url_for('index'))

@app.route('/add_proyecto', methods=['POST'])
@login_required
def add_proyecto():
    if request.method == 'POST':
        NOMBRE = request.form['NOMBRE']
        DESCRIPCION = request.form['DESCRIPCION']
        TECNOLOGIAS = request.form['TECNOLOGIAS']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO proyectos (NOMBRE, DESCRIPCION, TECNOLOGIAS) VALUES (%s, %s, %s)',
                    (NOMBRE, DESCRIPCION, TECNOLOGIAS))
        mysql.connection.commit()
        flash('Proyecto añadido satisfactoriamente')
        return redirect(url_for('proyecto'))

@app.route('/edit_proyecto/<ID>')
@login_required
def get_proyecto(ID):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proyectos WHERE ID = %s', (ID,))
    data = cur.fetchall()
    return render_template('edit-proyecto.html', proyecto = data[0])

@app.route('/update_proyecto/<ID>', methods=['POST'])
@login_required
def update_proyecto(ID):
    if request.method == 'POST':
        NOMBRE = request.form['NOMBRE']
        DESCRIPCION = request.form['DESCRIPCION']
        TECNOLOGIAS = request.form['TECNOLOGIAS']
    cur=mysql.connection.cursor()
    cur.execute("""
     UPDATE proyectos
    SET NOMBRE = %s,
        DESCRIPCION = %s,
        TECNOLOGIAS = %s
    WHERE ID = %s                     
    """, (NOMBRE, DESCRIPCION, TECNOLOGIAS, ID))
    mysql.connection.commit()
    flash('Proyecto actualizado satisfactoriamente')
    return redirect(url_for('proyecto'))

@app.route('/delete_proyecto/<ID>')
@login_required
def delete_proyecto(ID):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM proyectos WHERE ID ={0}'.format(ID))
    mysql.connection.commit()
    flash('Proyecto removido satisfactoriamente')
    return redirect (url_for('proyecto'))

@app.route('/contacto')
@login_required
def contacto():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('contacto.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
@login_required
def add_contact():
    if request.method == 'POST':
        NOMBRES = request.form['NOMBRES']
        CONTACTO = request.form['CONTACTO']
        EMAIL = request.form['EMAIL']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO CONTACTS (NOMBRES, CONTACTOS, EMAIL) VALUES (%s, %s, %s)',
                    (NOMBRES,CONTACTO,EMAIL))
        mysql.connection.commit()
        flash('conctato añadido satisfactoriamente')
        return redirect(url_for('contacto'))


@app.route('/edit/<ID>')
@login_required
def get_contact(ID):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE ID = %s', (ID,))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<ID>', methods=['POST'])
@login_required
def update_contact(ID):
    if request.method == 'POST':
        NOMBRES = request.form['NOMBRES']
        CONTACTO = request.form['CONTACTO']
        EMAIL = request.form['EMAIL']
    cur=mysql.connection.cursor()
    cur.execute("""
     UPDATE contacts
    SET NOMBRES = %s,
        EMAIL = %s,
        CONTACTOS = %s
    WHERE ID = %s                     
    """, (NOMBRES, EMAIL, CONTACTO, ID))
    mysql.connection.commit()
    flash('contacto actualizado satisfactoriamente')
    return redirect(url_for('contacto'))


@app.route('/delete/<ID>')
@login_required
def delete_contact(ID):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE ID ={0}'.format(ID))
    mysql.connection.commit()
    flash('contacto removido satisfactoriamente')
    return redirect (url_for('contacto'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)