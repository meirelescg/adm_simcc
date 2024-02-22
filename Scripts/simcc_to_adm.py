import sys
from os.path import dirname, abspath

PATH = dirname(dirname(abspath(__file__)))
sys.path.append(PATH)

from Dao import dbHandler
import pandas as pd


def get_actual_researchers():
    sql_script = """
        SELECT 
            r.name, 
            r.lattes_id,
            i.id as institution_id
        FROM
            researcher r
        JOIN
            institution i
        ON
            i.id = r.institution_id
        WHERE 
            i.acronym IN ('UESB', 'UFBA', 'UNEB', 'UESC')
        AND
            i.acronym IS NOT NULL;
        """
    registry = dbHandler.db_select(sql_script)

    data_frame = pd.DataFrame(registry, columns=["name", "lattes_id", "institution_id"])
    return data_frame


def build_script_sql(data_frame):

    insert_data = str()
    for Index, Data in data_frame.iterrows():

        name = Data["name"].replace("'", "''")
        lattes_id = Data["lattes_id"]
        code = Data["institution_id"]
        insert_data += f"('{name}', '{lattes_id}', '{code}'),"

    return f"""
        INSERT INTO researcher(
	    name, lattes_id, institution_id)
	    VALUES {insert_data[:-1]}
        """[
        :-1
    ]


if __name__ == "__main__":
    # simcc_ > adm_simcc
    data_frame = get_actual_researchers()

    script_sql = build_script_sql(data_frame)

    dbHandler.db_script(script_sql, database="adm_simcc")