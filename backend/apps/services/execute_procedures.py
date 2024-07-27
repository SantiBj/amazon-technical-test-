from django.db import connection

def execute_procedure(sentence:str) -> int:
    with connection.cursor() as cursor:
        cursor.execute(sentence)
        return cursor.fetchone()[0]
        