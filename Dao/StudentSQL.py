import sys

import pandas as pd

from Dao import dbHandler
from Model import Student


def insert(student: Student):
    script_sql = f"""
        INSERT INTO researcher (researcher_id, name, lattes_id, institution_id, type_)
        VALUES ('{student.student_id}', '{student.name}', '{student.lattes_id}', '{student.institution_id}', 'DISCENTE')
        """
    dbHandler.db_script(script_sql=script_sql)

    script_sql = f"""
        INSERT INTO graduate_program_researcher (graduate_program_id, researcher_id, year, type_)
        VALUES ('{student.graduate_program_id}', '{student.student_id}', '{student.year}', 'DISCENTE')
        """
    dbHandler.db_script(script_sql=script_sql)


def query(graduate_program_id: str = None, institution_id: str = None):
    if graduate_program_id:
        filter_graduate_program = (
            f"AND gpr.graduate_program_id = '{graduate_program_id}'"
        )
    else:
        filter_graduate_program = str()
    if institution_id:
        filter_institution = f"AND r.institution_id = '{institution_id}'"
    else:
        filter_institution = str()

    script_sql = f"""
        SELECT 
            r.name,
            r.lattes_id,
            gpr.type_
        FROM 
            graduate_program_researcher gpr
        JOIN researcher r ON 
        r.researcher_id = gpr.researcher_id
        WHERE 
            r.type_ = 'DISCENTE'
            {filter_graduate_program}
            {filter_institution}

    """
    registry = dbHandler.db_select(script_sql)

    data_frame = pd.DataFrame(
        registry,
        columns=[
            "name",
            "lattes_id",
            "type_",
        ],
    )

    return data_frame.to_dict(orient="records")


def delete(student_id):
    script_sql = f"""
    DELETE FROM graduate_program_researcher WHERE researcher_id = '{student_id}';
    DELETE FROM researcher WHERE researcher_id = '{student_id}';
    """
    dbHandler.db_script(script_sql)


def update(student: Student):
    script_sql = f"""
        UPDATE public.researcher
        SET 
            researcher_id = {student.researcher_id}, 
            name={student.name}, 
            lattes_id={student.lattes_id}, 
            institution_id={student.institution_id}, 
            type_={student.type_}
        WHERE researcher_id = {student.researcher_id};
        """
    dbHandler.db_script(script_sql)