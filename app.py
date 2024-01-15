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
    usable_range = db.Column(db.String(100), nullable=False)
    vlan_id = db.Column(db.Integer, nullable=True)
    top_level_subnet_id = db.Column(db.Integer, db.ForeignKey('top_level_subnet.id'), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Add top-level subnet logic
        pass

    top_level_subnets = TopLevelSubnet.query.all()
    return render_template('index.html', top_level_subnets=top_level_subnets)

def divide_subnet(top_subnet, division_size):
    network = ipaddress.ip_network(top_subnet)
    subnets = list(network.subnets(new_prefix=division_size))
    return [(subnet.network_address, subnet.broadcast_address, subnet) for subnet in subnets]

@app.route('/divide_subnet', methods=['POST'])
def divide():
    # Logic to divide subnet
    pass

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
