from sqlalchemy import create_engine
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
                            <td>
                                <a href='?del_mat={id}'>delete</a>
                                <span>&nbsp;|&nbsp;</span>
                                <a href='?edit_mat={id}'>edit</a>
                            </td>
                        </tr>""".format(
                            id=item.id,
                            t=item.material_type,
                            price=item.price,
                            lvl=item.classlvl
                            )
        table += "</tbody>"
        return table

    def delete_worker(self, person):
        self.session.query(Workers).filter(Workers.id == person).delete()
        self.session.commit()

    def delete_material(self, material):
        self.session.query(Materials).filter(Materials.id == material).delete()
        self.session.commit()

    def add_worker(self, form):
        level = int(form['classlvl'])
        worker = None
        backpack = ", "
        backpack = backpack.join(form.getlist('check'))

        # Delete materials from database
        for item in form.getlist('check'):
            self.delete_material(self.get_material_by_type(item).id)

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

        self.session.add(worker)
        self.session.commit()

    def add_material(self, form):
        print(form)
        material = Materials(
            material_type=form["type"],
            price=form["price"],
            classlvl=form["classlvl"]
        )

        self.session.add(material)
        self.session.commit()

    def get_worker(self, edit_id):
        return self.session.query(Workers).filter(Workers.id == edit_id).first()

    def get_material(self, edit_id):
        return self.session.query(Materials).filter(Materials.id == edit_id).first()

    def edit_worker(self, worker, form):
        self.delete_worker(worker)
        self.add_worker(form)

    def edit_material(self, material, form):
        self.delete_material(material)
        self.add_material(form)

    def get_material_by_type(self, mat_type):
        return self.session.query(Materials).filter(Materials.material_type == mat_type).first()

    def get_avaliable_material(self, edit_id):
        worker = self.get_worker(edit_id)

        if not worker:
            return None

        avaliable_materials = self.session.query(Materials).filter(Materials.classlvl <= worker.classlvl).all()
        return avaliable_materials
