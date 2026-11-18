from sqlmodel import Field, SQLModel

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    password: str


class Pandi(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    gender: str
    favorite_program: str
    coding_level: str
    current_year_level: str
    least_favorite_course: str
    current_academic_year: str
    TOTGA_program: str
    dream_career: str