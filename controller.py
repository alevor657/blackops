"""
A big, fat module for handling all functionality
"""

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, scoped_session

# Importing the mapped tables
from materials import Materials
from workers import Workers

# Importing the workers classes
from chef import Chef
from staff import Staff
from manager import Manager

class Controller():
    """
    Gives control over data to app.py
    """
    def __init__(self):
        self.USERNAME = "admin"
        self.PASSWORD = "admin"

        # SQLAlchemy stuff
        self.engine = create_engine("sqlite:///db/blackops.sqlite")
        self.session = scoped_session(sessionmaker(bind=self.engine))

        self.materials = self.session.query(Materials).all()
        self.workers_all_headings = Workers.__table__.columns.keys()
        self.material_all_headings = Materials.__table__.columns.keys()


    def check_login_data(self, form):
        """
        Checks if login data is correct
        """
        ps = form['password']
        uname = form['username']

        if (ps == self.PASSWORD and uname == self.USERNAME):
            return form['username']
        else:
            return None

    def create_workers_table(self):
        """
        Returns html table
        """
        table = "<thead><tr>"

        for item in self.workers_all_headings:
            table += """
            <th>{}</th>
            """.format(item)

        table += "<th>Action</th></tr></thead><tbody>"
        workers = self.session.query(Workers).all()
        for item in workers:
            # print(item.name)
            table += """<tr>
                            <td>{id}</td>
                            <td>{name}</td>
                            <td>{occup}</td>
                            <td>{backpack}</td>
                            <td>{lvl}</td>
                            <td>
                                <a href='?del_per={id}'>delete</a>
                                <span>&nbsp;|&nbsp;</span>
                                <a href='?edit_per={id}'>edit</a>
                            </td>
                        </tr>""".format(
                            id=item.id,
                            name=item.name,
                            occup=item.occupation,
                            lvl=item.classlvl,
                            backpack=item.backpack
                            )
        table += "</tbody>"
        return table

    def create_material_table(self):
        """
        Returns html table
        """
        table = "<thead><tr>"

        for item in self.material_all_headings:
            table += """
            <th>{}</th>
            """.format(item)

        table += "<th>Action</th></tr></thead><tbody>"
        materials = self.session.query(Materials).all()
        for item in materials:
            # print(item.name)
            table += """<tr>
                            <td>{id}</td>
                            <td>{t}</td>
                            <td>{price}</td>
                            <td>{lvl}</td>
                            <td>{owned}</td>
                            <td>
                                <a href='?del_mat={id}'>delete</a>
                                <span>&nbsp;|&nbsp;</span>
                                <a href='?edit_mat={id}'>edit</a>
                            </td>
                        </tr>""".format(
                            id=item.id,
                            t=item.material_type,
                            price=item.price,
                            lvl=item.classlvl,
                            owned=item.owned
                            )
        table += "</tbody>"
        return table

    def delete_worker(self, person):
        """
        Deletes a worker
        """
        self.session.query(Workers).filter(Workers.id == person).delete()
        self.session.commit()

    def delete_material(self, material):
        """
        Deletes material
        """
        self.session.query(Materials).filter(Materials.id == material).delete()
        self.session.commit()

    def add_worker(self, form):
        """
        Adds a worker
        """
        level = int(form['classlvl'])
        worker = None

        backpack = ", "
        backpack = backpack.join(form.getlist('check'))

        if (level == 1):
            worker = Staff(
                name=form["name"],
                classlvl=form["classlvl"],
                backpack=backpack
            )
        elif (level == 2):
            worker = Manager(
                name=form["name"],
                classlvl=form["classlvl"],
                backpack=backpack
            )
        elif (level == 3):
            worker = Chef(
                name=form["name"],
                classlvl=form["classlvl"],
                backpack=backpack
            )

        for item in form.getlist('check'):
            self.own(self.get_material_by_type(item), form['name'])

        if not form.getlist('check'):
            for item in self.session.query(Materials).filter(Materials.owned == worker.name).all():
                self.deown(item)

        self.session.add(worker)
        self.session.commit()

    def add_material(self, form):
        """
        Deletes a material
        """
        material = Materials(
            material_type=form["type"],
            price=form["price"],
            classlvl=form["classlvl"]
        )

        self.session.add(material)
        self.session.commit()

    def get_worker(self, edit_id):
        """
        Returns a worker object
        """
        return self.session.query(Workers).filter(Workers.id == edit_id).first()

    def get_material(self, edit_id):
        """
        Returns a material object
        """
        return self.session.query(Materials).filter(Materials.id == edit_id).first()

    def edit_worker(self, worker, form):
        """
        Refreshes workers data
        """
        self.delete_worker(worker)
        self.add_worker(form)

    def edit_material(self, material, form):
        """
        Refreshes materials data
        """
        self.delete_material(material)
        self.add_material(form)

    def get_material_by_type(self, mat_type):
        """
        Returns a material obj by name
        """
        return self.session.query(Materials).filter(Materials.material_type == mat_type).first()

    def get_avaliable_material(self, edit_id):
        """
        Returns all avaliable materials for a current workers id
        """
        worker = self.get_worker(edit_id)

        if not worker:
            return None

        bpack = self.get_worker(worker.id).backpack.split(', ')
        all_materials = self.session.query(Materials)

        avaliable_materials = all_materials.filter(
            and_(Materials.classlvl <= worker.classlvl, ~Materials.material_type.in_(bpack))
        ).all()

        return avaliable_materials

    def own(self, item, owner):
        """
        Owns something
        """
        item.owned = owner
        self.session.commit()

    def deown(self, item):
        """
        Deowns something
        """
        item.owned = None
        self.session.commit()
