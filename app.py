import hashlib

from sqlmodel import Session

from database import create_db_and_tables, engine
from models import Users, Pandi


def main():
    create_db_and_tables()

    demo = Users(name="demo", password=hashlib.sha256(b"demo123").hexdigest())
    sample = Pandi(
        name="Sample Student", age=19, gender="Female",
        favorite_program="BSIT", coding_level="Beginner",
        current_year_level="1st Year", least_favorite_course="Math",
        current_academic_year="2026-2027", TOTGA_program="Web Dev",
        dream_career="Software Engineer",
    )

    with Session(engine) as session:
        session.add(demo)
        session.add(sample)
        session.commit()


if __name__ == "__main__":
    main()