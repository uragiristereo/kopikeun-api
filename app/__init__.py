from app.core import app, db
from app.controllers import *
from app.database import *

db.create_all()
print(db.engine.table_names())
