import sqlalchemy

print(sqlalchemy.__version__)

engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table('users', metadata, 
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('fullname', sqlalchemy.String),
)

addresses = sqlalchemy.Table('addresses', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('user_id', None, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('email_address', sqlalchemy.String, nullable=False),
)

metadata.create_all(engine)

ins = users.insert()
ins = users.insert().values(name='jack', fullname='Jack Jones')
print(str(ins))
print(ins.compile().params)

conn = engine.connect()
print(conn)

result = conn.execute(ins)
print(result)

ins.bind = engine
print(str(ins))
print(result.inserted_primary_key)

ins = users.insert()
conn.execute(ins, id=2, name='wendy', fullname='Wendy Williams')

conn.execute(addresses.insert(), [
    {'user_id': 1, 'email_address': 'jack@yahoo.com'},
    {'user_id': 1, 'email_address': 'jack@msn.com'},
    {'user_id': 2, 'email_address': 'www@www.org'},
    {'user_id': 2, 'email_address': 'wendy@aol.com'},
])

s = sqlalchemy.sql.select([users])
result = conn.execute(s)

for row in result:
    print(row)

result = conn.execute(s)
row = result.fetchone()
print("name:", row['name'], "; fullname:", row['fullname'])
row = result.fetchone()
print("name:", row[1], "; fullname:", row[2])

for row in conn.execute(s):
    print("name:", row[users.c.name], "; fullname:", row[users.c.fullname])

result.close()

s = sqlalchemy.sql.select([users.c.name, users.c.fullname])
result = conn.execute(s)
for row in result:
    print(row)

for row in conn.execute(sqlalchemy.sql.select([users, addresses])):
    print(row)

s = sqlalchemy.sql.select([users, addresses]).where(users.c.id == addresses.c.user_id)
for row in conn.execute(s):
    print(row)

print(users.c.id == addresses.c.user_id)
print(users.c.id == 7)
print((users.c.id == 7).compile().params)
print(users.c.name == None)
print('fred' > users.c.name)
print(users.c.id + addresses.c.id)
print(users.c.name + users.c.fullname)
# ModuleNotFoundError: No module named 'MySQLdb'
# print((users.c.name + users.c.fullname).compile(bind=sqlalchemy.create_engine('mysql://')))
print(users.c.name.op('tiddlywinks')('foo'))

print(sqlalchemy.sql.and_(
        users.c.name.like('j%'),
        users.c.id == addresses.c.user_id,
        sqlalchemy.sql.or_(
            addresses.c.email_address == 'wendy@aol.com',
            addresses.c.email_address == 'jack@yahoo.com'
        ),
        sqlalchemy.sql.not_(users.c.id > 5)
    )
)

print(users.c.name.like('j%') & (users.c.id == addresses.c.user_id) &
    (
        (addresses.c.email_address == 'wendy@aol.com') | \
        (addresses.c.email_address == 'jack@yahoo.com')
    ) \
    & ~(users.c.id > 5)
)

s = sqlalchemy.sql.select([
        (users.c.fullname + "," + addresses.c.email_address)
        .label('title')
    ]).where(
        sqlalchemy.sql.and_(
            users.c.id == addresses.c.user_id,
            users.c.name.between('m', 'z'),
            sqlalchemy.sql.or_(
                addresses.c.email_address.like('%@aol.com'),
                addresses.c.email_address.like('%@msn.com')
            )
        )
    )
print(conn.execute(s).fetchall())

s = sqlalchemy.sql.select([
        (users.c.fullname + "," + addresses.c.email_address)
        .label('title')
    ]).where(users.c.id == addresses.c.user_id).where(
        users.c.name.between('m', 'z')).where(
            sqlalchemy.sql.or_(
                addresses.c.email_address.like('%@aol.com'),
                addresses.c.email_address.like('%@msn.com')
            )
        )
print(conn.execute(s).fetchall())

print(users.join(addresses))

print(users.join(
        addresses,
        addresses.c.email_address.like(users.c.name + '%')
    )
)

s = sqlalchemy.sql.select([users.c.fullname]).select_from(
    users.join(addresses, addresses.c.email_address.like(users.c.name + '%'))
)
print(conn.execute(s).fetchall())

s = sqlalchemy.sql.select([users.c.fullname]).select_from(users.outerjoin(addresses))
print(s)