from flask import Flask, render_template, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(300))
    price = db.Column(db.String(300))
    in_stock = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Product{self.id}. {self.prod_name} - {self.price}'


@app.route('/')
def main():
    products = Product.query.all()
    return render_template('index.html', products_list=products)


@app.route('/in_stock/<product_id>', methods=['PATCH'])
def modify_product(product_id):
    product = Product.query.get(product_id)
    product.in_stock = request.json['in_stock']
    db.session.commit()


@app.route('/add', methods=['POST'])
def add_product():
    data = request.json 
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return 'OK'

        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)