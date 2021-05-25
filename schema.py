def create_classes(db):
    class Customer(db.Model):
        __tablename__ = 'customer'

        id = db.Column(db.Integer, primary_key=True)
        customer_id = db.Column(db.VARCHAR)
        gender=db.Column(db.String)
        income=db.Column(db.Float)
        membership_date=db.Column(db.VARCHAR)
        


        def __repr__(self):
            return '<Customer %r>' % (self.name)
    return Customer