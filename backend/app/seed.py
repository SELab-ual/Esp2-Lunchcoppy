from .db import engine
from .models import Restaurant, User, SQLModel
from .auth import hash_password
from sqlmodel import Session, select

def seed():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        count = session.exec(select(Restaurant)).first()
        if not count:
            restaurants = [
                Restaurant(name="Casa Sol", description="Cozy local food", average_price=12, type="Spanish", latitude=36.840, longitude=-2.467),
                Restaurant(name="Bistro Verde", description="Healthy salads and bowls", average_price=10, type="Healthy", latitude=36.842, longitude=-2.465),
                Restaurant(name="Pasta Bella", description="Italian classics", average_price=15, type="Italian", latitude=36.839, longitude=-2.468),
            ]
            session.add_all(restaurants)
            session.commit()
        # create a test user
        user = session.exec(select(User).where(User.username == "tester")).first()
        if not user:
            u = User(username="tester", email="tester@example.com", hashed_password=hash_password("password"))
            session.add(u)
            session.commit()