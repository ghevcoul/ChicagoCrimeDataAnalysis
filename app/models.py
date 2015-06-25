from app import db

class Chicago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(16))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    block = db.Column(db.String(100))
    iucr = db.Column(db.String(4))
    primary_type = db.Column(db.String(35))
    description = db.Column(db.String(65))
    location_description = db.Column(db.String(100))
    arrest = db.Column(db.Boolean)
    domestic = db.Column(db.Boolean)
    beat = db.Column(db.Integer)
    district = db.Column(db.Integer)
    ward = db.Column(db.Integer)
    community_area = db.Column(db.Integer)
    year = db.Column(db.Integer)
    updated_on = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    weekday = db.Column(db.String(10))

    #def __repr__(self):
    #    return "<Chicago {}>".format(self.id)
