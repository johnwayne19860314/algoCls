from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Step 1: Create a base class
Base = declarative_base()

# Step 2: Define a User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, age={self.age})>"

# Step 3: Create a SQLite database
engine = create_engine('sqlite:///users.db', echo=True)

# Step 4: Create the users table
Base.metadata.create_all(engine)

# Step 5: Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Step 6: Create and add new users
user1 = User(name='Alice', age=30)
user2 = User(name='Bob', age=25)

session.add(user1)
session.add(user2)
session.commit()

# Step 7: Query the database
users = session.query(User).all()
print(users)

# Step 8: Update a user's age
user_to_update = session.query(User).filter_by(name='Alice').first()
user_to_update.age = 31
session.commit()

# Step 9: Delete a user
user_to_delete = session.query(User).filter_by(name='Bob').first()
session.delete(user_to_delete)
session.commit()

# Close the session
session.close()
