from flask import Flask
from flask_restx import Api, Namespace, Resource, fields
from flask_sqlalchemy import SQLAlchemy

# создание приложения
app = Flask(__name__)
api = Api(app, version='1.0', title='CarMVC API', description='A simple TodoMVC API')
ns = Namespace('cars', description="all cars", path='')
api.add_namespace(ns, path="/api/v1")

# база данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# форма
car = ns.model('Car', {
    'id': fields.Integer(readonly=True, description='The car unique identifier'),
    'category': fields.String(required=True, description='car category'),
    'name': fields.String(required=True, description='name category')
})

# парсинг данных
my_car_parser = ns.parser()
my_car_parser.add_argument('category', type=str, default='', required=True)
my_car_parser.add_argument('name', type=str, default='', required=True)


# модель для работы с бд
class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    name = db.Column(db.String)


# простой функционал
@ns.route('/cars')
class CarList(Resource):
    @ns.doc('car_list')
    @ns.marshal_list_with(car)
    def get(self):
        result = Car.query.all()
        return result

    @ns.doc('create_car')
    @ns.expect(my_car_parser)
    # @ns.marshal_with(car, code=201)
    def post(self):
        args = my_car_parser.parse_args(strict=True)
        start_car = Car(category=args["category"], name=args["name"])
        db.session.add(start_car)
        db.session.commit()
        return "Done", 201


if __name__ == '__main__':
    app.run(debug=True)
