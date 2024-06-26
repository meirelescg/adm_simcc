from pydantic import UUID4, BaseModel


class Student(BaseModel):
    student_id: UUID4
    name: str
    lattes_id: int
    institution_id: UUID4
    graduate_program_id: UUID4
    year: int


class ListStudent(BaseModel):
    student_list: list[Student]
