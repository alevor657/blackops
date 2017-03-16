from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.workers = self.session.query(Workers).all()
        self.materials = self.session.query(Materials).all()
        self.workers_all_headings = Workers.__table__.columns.keys()


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

        # counter = 0
        # count_columns = len([a for a in dir(self.workers) if not a.startswith('__')])
        # print("count cols:", count_columns)
        # print([a for a in dir(self.workers) if not a.startswith('__')])

        for item in self.workers_all_headings:
            print(item)
            table += """
            <th>{}</th>
            """.format(item)

        table += "<th>Action</th></tr></thead><tbody>"
        for item in self.workers:
            # print(item.name)
            table += """<tr>
                            <td>{id}</td>
                            <td>{name}</td>
                            <td>{occup}</td>
                            <td>{lvl}</td>
                            <td><a href='?del={id}'>delete</a></td>
                        </tr>""".format(
                            id=item.id,
                            name=item.name,
                            occup=item.occupation,
                            lvl=item.classlvl
                            )
        table += "</tbody>"
        return table
