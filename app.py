from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import ipaddress

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ipam.db'
db = SQLAlchemy(app)

class TopLevelSubnet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subnet = db.Column(db.String(50), nullable=False)
    divisions = db.relationship('SubnetDivision', backref='top_level_subnet', lazy=True)

class SubnetDivision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    network_address = db.Column(db.String(50), nullable=False)
    broadcast_address = db.Column(db.String(50), nullable=False)
    vlan_id = db.Column(db.Integer, nullable=True)
    top_level_subnet_id = db.Column(db.Integer, db.ForeignKey('top_level_subnet.id'), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_subnet = TopLevelSubnet(subnet=request.form['top_level_subnet'])
        db.session.add(new_subnet)
        db.session.commit()
        return redirect(url_for('index'))

    top_level_subnets = TopLevelSubnet.query.all()
    return render_template('index.html', top_level_subnets=top_level_subnets)

def divide_subnet(top_subnet, division_size):
    network = ipaddress.ip_network(top_subnet.subnet)
    subnets = list(network.subnets(new_prefix=division_size))
    return [(str(subnet.network_address), str(subnet.broadcast_address)) for subnet in subnets]

@app.route('/divide_subnet/<int:subnet_id>', methods=['POST'])
def divide(subnet_id):
    division_size = int(request.form['division_size'])
    top_subnet = TopLevelSubnet.query.get_or_404(subnet_id)
    divided_subnets = divide_subnet(top_subnet, division_size)
    
    for network_address, broadcast_address in divided_subnets:
        new_division = SubnetDivision(network_address=network_address, broadcast_address=broadcast_address, top_level_subnet_id=subnet_id)
        db.session.add(new_division)
    
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()  # Create tables before running the application
    app.run(debug=True)

