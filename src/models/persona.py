import sqlalchemy as sa

from src.models import Model


class Persona(Model):

    BLOOD_TYPES = ('0+', '0-', 'A+', 'A-',
                   'B+', 'B-', 'AB+', 'AB-'
                   )
    SEX = ('M', 'F')

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(255))
    name = sa.Column(sa.String(255))
    mail = sa.Column(sa.String(255))
    birthdate = sa.Column(sa.Date)
    blood_group = sa.Column(sa.Enum(*BLOOD_TYPES))
    sex = sa.Column(sa.Enum(*SEX))
    ssn = sa.Column(sa.String(255))
    address = sa.Column(sa.String(255))
    residence = sa.Column(sa.String(255))
    company = sa.Column(sa.String(255))
    job = sa.Column(sa.String(255))
    current_location = sa.Column(sa.String(255))
    website = sa.Column(sa.Text)

    __tablename__ = 'persona'

