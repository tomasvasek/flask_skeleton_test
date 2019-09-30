from flask_login import UserMixin
from sqlalchemy.schema import Column
from sqlalchemy.types import Boolean, Integer, String,Float

from ..database import db
from ..mixins import CRUDModel
from ..util import generate_random_token
from ...settings import app_config
from ...extensions import bcrypt

class Vysledky(CRUDModel):
    __tablename__ = 'vysledky'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True, index=True, doc="The user's username.")
    hodnoceni = Column(Float)

    # Use custom constructor
    # pylint: disable=W0231
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
