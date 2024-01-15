from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ipam.db'
db = SQLAlchemy(app)

class IPAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<IPAddress {self.address}>'

def create_tables():
    db.create_all()

@app.route('/')
def index():
    ips = IPAddress.query.all()
    return render_template('index.html', ips=ips)

@app.route('/add', methods=['POST'])
def add_ip():
    ip_address = request.form['ip_address']
    new_ip = IPAddress(address=ip_address)
    db.session.add(new_ip)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_ip(id):
    ip_to_delete = IPAddress.query.get_or_404(id)
    db.session.delete(ip_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        create_tables()  # Create tables within the application context
    app.run(debug=True)

