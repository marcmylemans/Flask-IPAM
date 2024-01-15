from flask import Flask, request, render_template, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
import csv
from io import StringIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ipam.db'
db = SQLAlchemy(app)

class TopLevelSubnet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subnet = db.Column(db.String(18), unique=True, nullable=False)

    def __repr__(self):
        return f'<TopLevelSubnet {self.subnet}>'

class Subnet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    vlan = db.Column(db.Integer, nullable=False)
    subnet = db.Column(db.String(18), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('top_level_subnet.id'), nullable=False)
    parent = db.relationship('TopLevelSubnet', backref=db.backref('subnets', lazy=True))

    def __repr__(self):
        return f'<Subnet {self.name}, VLAN: {self.vlan}, Address: {self.subnet}>'

def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'top_level_subnet' in request.form:
            new_top_level_subnet = TopLevelSubnet(subnet=request.form['top_level_subnet'])
            db.session.add(new_top_level_subnet)
            db.session.commit()
        elif 'subnet_name' in request.form:
            new_subnet = Subnet(
                name=request.form['subnet_name'],
                vlan=request.form['vlan'],
                subnet=request.form['subnet_address'],
                parent_id=request.form['top_level_subnet_id']
            )
            db.session.add(new_subnet)
            db.session.commit()

    top_level_subnets = TopLevelSubnet.query.all()
    subnets = Subnet.query.all()
    return render_template('index.html', top_level_subnets=top_level_subnets, subnets=subnets)

@app.route('/delete_subnet/<int:id>')
def delete_subnet(id):
    subnet_to_delete = Subnet.query.get_or_404(id)
    db.session.delete(subnet_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_top_level_subnet/<int:id>')
def delete_top_level_subnet(id):
    top_level_subnet_to_delete = TopLevelSubnet.query.get_or_404(id)
    db.session.delete(top_level_subnet_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/export_csv')
def export_csv():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Subnet Name', 'Subnet Address', 'VLAN', 'Top Level Subnet'])

    subnets = Subnet.query.all()
    for subnet in subnets:
        top_level_subnet = TopLevelSubnet.query.get(subnet.parent_id)
        cw.writerow([subnet.name, subnet.subnet, subnet.vlan, top_level_subnet.subnet])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=subnets.csv"
    output.headers["Content-type"] = "text/csv"
    return output


if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)
