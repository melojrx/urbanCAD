from ..database import db

class DeteccaoVeicular(db.Model):
    __tablename__ = 'tb_deteccao_dec'
    __table_args__ = {"schema":"maleta"}
    
    id = db.Column('id_deteccao_dec', db.Integer, autoincrement=True, primary_key=True)
    code = db.Column('code', db.String(50))
    gps_data_lat = db.Column('gps_data_lat', db.String(20), nullable=False)
    gps_data_long = db.Column('gps_data_long', db.String(20), nullable=False)
    gps_data_timestamp = db.Column('gps_data_timestamp', db.DateTime, nullable=True)
    plate = db.Column('plate', db.String(7))
    image = db.Column('image', db.LargeBinary)

    fileBase64 = None

    def __init__(self, code, gps_data_lat, gps_data_long, gps_data_timestamp, plate, image):
        self.code = code
        self.gps_data_lat = gps_data_lat
        self.gps_data_long = gps_data_long
        self.gps_data_timestamp = gps_data_timestamp
        self.plate = plate
        self.image = image