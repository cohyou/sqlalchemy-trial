import sqlalchemy

print(sqlalchemy.__version__)

engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)

# metadata = sqlalchemy.MetaData()

# users = sqlalchemy.Table('users', metadata, 
#     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column('name', sqlalchemy.String),
#     sqlalchemy.Column('fullname', sqlalchemy.String),
# )

# addresses = sqlalchemy.Table('addresses', metadata,
#     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column('user_id', None, sqlalchemy.ForeignKey('users.id')),
#     sqlalchemy.Column('email_address', sqlalchemy.String, nullable=False),
# )

# metadata.create_all(engine)

# ins = users.insert()
# ins = users.insert().values(name='jack', fullname='Jack Jones')
# print(str(ins))
# print(ins.compile().params)

# conn = engine.connect()
# print(conn)

# result = conn.execute(ins)
# print(result)

# ins.bind = engine
# print(str(ins))
# print(result.inserted_primary_key)

# ins = users.insert()
# conn.execute(ins, id=2, name='wendy', fullname='Wendy Williams')

# conn.execute(addresses.insert(), [
#     {'user_id': 1, 'email_address': 'jack@yahoo.com'},
#     {'user_id': 1, 'email_address': 'jack@msn.com'},
#     {'user_id': 2, 'email_address': 'www@www.org'},
#     {'user_id': 2, 'email_address': 'wendy@aol.com'},
# ])

# s = sqlalchemy.sql.select([users])
# result = conn.execute(s)

# for row in result:
#     print(row)

# result = conn.execute(s)
# row = result.fetchone()
# print("name:", row['name'], "; fullname:", row['fullname'])
# row = result.fetchone()
# print("name:", row[1], "; fullname:", row[2])

# for row in conn.execute(s):
#     print("name:", row[users.c.name], "; fullname:", row[users.c.fullname])

# result.close()

# s = sqlalchemy.sql.select([users.c.name, users.c.fullname])
# result = conn.execute(s)
# for row in result:
#     print(row)

# for row in conn.execute(sqlalchemy.sql.select([users, addresses])):
#     print(row)

# s = sqlalchemy.sql.select([users, addresses]).where(users.c.id == addresses.c.user_id)
# for row in conn.execute(s):
#     print(row)

# print(users.c.id == addresses.c.user_id)
# print(users.c.id == 7)
# print((users.c.id == 7).compile().params)
# print(users.c.name == None)
# print('fred' > users.c.name)
# print(users.c.id + addresses.c.id)
# print(users.c.name + users.c.fullname)
# # ModuleNotFoundError: No module named 'MySQLdb'
# # print((users.c.name + users.c.fullname).compile(bind=sqlalchemy.create_engine('mysql://')))
# print(users.c.name.op('tiddlywinks')('foo'))

# print(sqlalchemy.sql.and_(
#         users.c.name.like('j%'),
#         users.c.id == addresses.c.user_id,
#         sqlalchemy.sql.or_(
#             addresses.c.email_address == 'wendy@aol.com',
#             addresses.c.email_address == 'jack@yahoo.com'
#         ),
#         sqlalchemy.sql.not_(users.c.id > 5)
#     )
# )

# print(users.c.name.like('j%') & (users.c.id == addresses.c.user_id) &
#     (
#         (addresses.c.email_address == 'wendy@aol.com') | \
#         (addresses.c.email_address == 'jack@yahoo.com')
#     ) \
#     & ~(users.c.id > 5)
# )

# s = sqlalchemy.sql.select([
#         (users.c.fullname + "," + addresses.c.email_address)
#         .label('title')
#     ]).where(
#         sqlalchemy.sql.and_(
#             users.c.id == addresses.c.user_id,
#             users.c.name.between('m', 'z'),
#             sqlalchemy.sql.or_(
#                 addresses.c.email_address.like('%@aol.com'),
#                 addresses.c.email_address.like('%@msn.com')
#             )
#         )
#     )
# print(conn.execute(s).fetchall())

# s = sqlalchemy.sql.select([
#         (users.c.fullname + "," + addresses.c.email_address)
#         .label('title')
#     ]).where(users.c.id == addresses.c.user_id).where(
#         users.c.name.between('m', 'z')).where(
#             sqlalchemy.sql.or_(
#                 addresses.c.email_address.like('%@aol.com'),
#                 addresses.c.email_address.like('%@msn.com')
#             )
#         )
# print(conn.execute(s).fetchall())

# print(users.join(addresses))

# print(users.join(
#         addresses,
#         addresses.c.email_address.like(users.c.name + '%')
#     )
# )

# s = sqlalchemy.sql.select([users.c.fullname]).select_from(
#     users.join(addresses, addresses.c.email_address.like(users.c.name + '%'))
# )
# print(conn.execute(s).fetchall())

# s = sqlalchemy.sql.select([users.c.fullname]).select_from(users.outerjoin(addresses))
# print(s)


## the ORM

# declare a mapping

import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    fullname = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname
        )
print(User.__table__)

Base.metadata.create_all(engine)
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
print(ed_user.name)
print(ed_user.nickname)
print(str(ed_user.id))

import sqlalchemy.orm
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

# adding and updating objects
ed_user = User(name='ed', fullname='Ed Jones', nickname='ednickname')
session.add(ed_user)
our_user = session.query(User).filter_by(name='ed').first()
print(our_user)
print(ed_user is our_user)

session.add_all([
    User(name='wendy', fullname='Wendy Williams', nickname='windy'),
    User(name='mary', fullname='Mary Contrary', nickname='mary'),
    User(name='fred', fullname='Fred Flintstone', nickname='freddy')
])
print(session.new)

ed_user.nickname = 'eddie'
print(session.dirty)

session.commit()

print(ed_user.id)

# querying
for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)

for row in session.query(User.name.label('name_label')).all():
    print(row.name_label)

for name, in session.query(User.name).filter_by(fullname='Ed Jones'):
    print(name)

for user in session.query(User).filter(User.name == 'ed').filter(User.fullname == 'Ed Jones'):
    print(user)

class Address(Base):
    __tablename__ = 'addresses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    email_address = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))

    user = sqlalchemy.orm.relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

User.addresses = sqlalchemy.orm.relationship("Address", order_by=Address.id, back_populates="user")

Base.metadata.create_all(engine)

# working with related objects
jack = User(name='jack', fullname='Jack Bean', nickname='gjffdd')
print(jack.addresses)

jack.addresses = [
    Address(email_address='jack@google.com'),
    Address(email_address='j25@yahoo.com')
]

print(jack.addresses[1])

print(jack.addresses[1].user)

session.add(jack)
session.commit()

jack = session.query(User).filter_by(name='jack').one()
print(jack)
print(jack.addresses)

# querying with joins
for u, a in session.query(User, Address)\
    .filter(User.id == Address.user_id)\
    .filter(Address.email_address == 'jack@google.com')\
    .all():
    print(u)
    print(a)

r = session.query(User).join(Address)\
    .filter(Address.email_address == 'jack@google.com')\
    .all()
print(r)

## eager loading

# selectin load
jack = session.query(User)\
    .options(sqlalchemy.orm.selectinload(User.addresses))\
    .filter_by(name='jack').one()
print(jack)
print(jack.addresses)

# joined load
jack = session.query(User)\
    .options(sqlalchemy.orm.joinedload(User.addresses))\
    .filter_by(name='jack').one()
print(jack)
print(jack.addresses)

## building many to many relationship

# association table
post_keywords = sqlalchemy.Table('post_keywords', Base.metadata,
    sqlalchemy.Column('post_id', ForeignKey('posts.id'), primary_key=True),
    sqlalchemy.Column('keyword_id', ForeignKey('keywords.id'), primary_key=True),
)

class BlogPost(Base):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('users.id'))
    headline = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    body = sqlalchemy.Column(Text)

    # many to many BlogPost<->Keyword
    keywords = sqlalchemy.orm.relationship('Keyword', secondary=post_keywords, back_populates='posts')

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body
    
    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)


class Keyword(Base):
    __tablename__ = 'keywords'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    keyword = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, unique=True)
    posts = sqlalchemy.orm.relationship('BlogPost',
        secondary=post_keywords,
        back_populates='keywords'
    )

    def __init__(self, keyword):
        self.keyword = keyword
    
