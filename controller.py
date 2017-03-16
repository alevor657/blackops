from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from materials import Materials
from workers import Workers

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
            print(item)
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
                            <td>{lvl}</td>
                            <td><a href='?del_per={id}'>delete</a></td>
                        </tr>""".format(
                            id=item.id,
                            name=item.name,
                            occup=item.occupation,
                            lvl=item.classlvl
                            )
        table += "</tbody>"
        return table

    def create_material_table(self):
        table = "<thead><tr>"

        for item in self.workers_all_headings:
            print(item)
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
                            <td><a href='?del_mat={id}'>delete</a></td>
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
        worker = Workers(
            name=form["name"],
            occupation=form["occupation"],
            classlvl=form["classlvl"]
        )

        self.session.add(worker)
        self.session.commit()

    def add_material(self, form):
        material = Materials(
            material_type=form["type"],
            price=form["price"],
            classlvl=form["classlvl"]
        )

        self.session.add(material)
        self.session.commit()
