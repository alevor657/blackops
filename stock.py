from workers import Workers
from materials import Materials

from sqlalchemy import Column, Float, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from workers import Base


# backpack_table = Table('backpack', Base.metadata,
#     Column('owner', String, ForeignKey('workers.id')),
#     Column('item', String, ForeignKey('materials.id'))
# )

class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True)
    owner_id = Column('owner', String, ForeignKey('workers.id'))
    # owner_name = Column('owner_name', String, ForeignKey('workers.name'))

    items_id = Column('items', String, ForeignKey('materials.id'))
    # items_type = Column('items_type', String, ForeignKey('materials.material_type'))
    # items_quantity = Column('items_quantity', Integer, ForeignKey('materials.quantity'))

    # owner = Column('owner', String, ForeignKey('Workers.workers.id'))
    # items = Column('item', String, ForeignKey('Materials.materials.id'))
