from flask import Flask, render_template, request, redirect , url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)



# MYSQL Conection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2008'
app.config['MYSQL_DB'] = 'portafolio'
mysql = MySQL(app)

#settings

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/biografia')
def biografia():
    return render_template('biografia.html')

@app.route('/proyecto')
def proyecto():
    return render_template('proyecto.html')

@app.route('/contacto')
def contacto():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('contacto.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
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
def get_contact(ID):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE ID = %s', (ID,))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<ID>', methods=['POST'])
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
def delete_contact(ID):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE ID ={0}'.format(ID))
    mysql.connection.commit()
    flash('contacto removido satisfactoriamente')
    return redirect (url_for('contacto'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)

