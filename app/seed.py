from app.db import SessionLocal
from app.models import Workflow


def seed():
    db = SessionLocal()
    try:
        if db.query(Workflow).first() is not None:
            return
        db.add(Workflow(name="Sample Workflow", description="Initial seed workflow"))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    from app.models import Base
    from app.db import engine

    Base.metadata.create_all(bind=engine)
    seed()
    print("Seed done.")
