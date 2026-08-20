import psycopg
from psycopg.types.json import Jsonb
import csv
import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()


import_csv_path = 'import/ccgdata_sets.csv'

def is_valid_uuid(potential_uuid):
    try:
        uuid.UUID(str(potential_uuid))
        return True
    except ValueError:
        return False

def import_games_csv(import_csv_path, database_url):
    with open(import_csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        imported_csv = list(reader)
    #print(f"id ({type(imported_csv[0]['id'])}) = {imported_csv[0]['id']}\n")
    #print(f"attributes ({type(imported_csv[0]['attributes'])}) = {imported_csv[0]['attributes']}\n")
    #print(f"images ({type(imported_csv[0]['images'])}) = {imported_csv[0]['images']}\n")
    #print(f"source_notes ({type(imported_csv[0]['source_notes'])}) = {imported_csv[0]['source_notes']}\n")
    # Connect to an existing database
    with psycopg.connect(database_url) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            for row in imported_csv:
                print(row)

                try:
                    publishers_list = json.loads(row['publishers']) 
                except (json.JSONDecodeError, ValueError):
                    publishers_list = {}

                try:
                    source_notes_dict = json.loads(row['source_notes'])
                except (json.JSONDecodeError, ValueError):
                    source_notes_dict = {}

                if 'id' in row and is_valid_uuid(row['id']) == True:
                    row_id = row['id']
                else:
                    row_id = uuid.uuid4()
                
                cur.execute(
                    """
                    INSERT INTO gameitems_set (
                        id
                        , game_id
                        , name
                        , game_set_slug
                        , publishers
                        , released
                        , release_year
                        , release_month
                        , release_day
                        , expected_item_count
                        , source_notes
                        ) 
                    VALUES (
                        %s, %s, %s, %s, %s
                        , nullif(%s, '')::BOOL, nullif(%s, '')::INTEGER, nullif(%s, '')::INTEGER, nullif(%s, '')::INTEGER
                        , nullif(%s, '')::INTEGER, %s
                        )
                    ON CONFLICT (id) DO UPDATE SET 
                        game_id=EXCLUDED.game_id
                        , name=EXCLUDED.name
                        , game_set_slug=EXCLUDED.game_set_slug
                        , publishers=EXCLUDED.publishers
                        , released=EXCLUDED.released
                        , release_year=EXCLUDED.release_year
                        , release_month=EXCLUDED.release_month
                        , release_day=EXCLUDED.release_day
                        , expected_item_count=EXCLUDED.expected_item_count
                        , source_notes=EXCLUDED.source_notes
                    """,
                    (
                        row_id
                        , row['game_id']
                        , row['name']
                        , row['game_set_slug']
                        , Jsonb(publishers_list)
                        , row['released']
                        , row['release_year']
                        , row['release_month']
                        , row['release_day']
                        , row['expected_item_count']
                        , Jsonb(source_notes_dict)
                    )
                )   
                conn.commit()
    return True 

def main():
    database_url = (
        f"postgresql://"
        f"{os.getenv('CCGDATA_DATABASE_USER')}:"
        f"{os.getenv('CCGDATA_DATABASE_PASSWORD')}@"
        f"{os.getenv('CCGDATA_DATABASE_HOST')}:"
        f"{os.getenv('CCGDATA_DATABASE_PORT')}/"
        f"{os.getenv('CCGDATA_DATABASE_NAME')}"
    )
    import_games_csv(import_csv_path, database_url)

if __name__ == "__main__":
    main()