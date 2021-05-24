def create_classes(db):
    class Customer(db.Model):
        __tablename__ = 'customer'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64))
        customer_id=db.Column(db.VARCHAR)
        gender=db.Column(db.String)
        age=db.Column(db.Integer)
        income=db.Column(db.Float)
        offer=db.Column(db.VARCHAR(32))
        membership_date=db.Column(db.VARCHAR)


        def __repr__(self):
            return '<Customer %r>' % (self.name)
    return Customer