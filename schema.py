def create_classes(db):
    class Customer(db.Model):
        __tablename__ = 'customer'

        id = db.Column(db.Integer, primary_key=True)
        offer_id = db.Column(db.VARCHAR)
        reward=db.Column(db.Integer)
        channels=db.Column(db.String)
        difficulty=db.Column(db.Integer)
        duration=db.Column(db.Integer)
        offer_type=db.Column(db.String)
        offer_completed=db.Column(db.String)


        def __repr__(self):
            return '<Customer %r>' % (self.name)
    return Customer