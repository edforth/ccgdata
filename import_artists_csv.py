import psycopg
from psycopg.types.json import Jsonb
import csv
import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()


import_csv_path = 'import/ccgdata_artists.csv'

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
                    printed_aliases_list = json.loads(row['printed_aliases']) 
                except (json.JSONDecodeError, ValueError):
                    printed_aliases_list = {}

                try:
                    tags_list = json.loads(row['tags']) 
                except (json.JSONDecodeError, ValueError):
                    tags_list = {}

                try:
                    links_dict = json.loads(row['links'])
                except (json.JSONDecodeError, ValueError):
                    links_dict = {}

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
                    INSERT INTO gameitems_artist (
                        id
                        , name
                        , first_name
                        , last_name
                        , artist_name_slug
                        , printed_aliases
                        , tags
                        , links
                        , source_notes
                        ) 
                    VALUES (
                        %s --id
                        , %s --name
                        , %s --first_name
                        , %s --last_name
                        , %s --artist_name_slug
                        , %s --printed_aliases
                        , %s --tags
                        , %s --links
                        , %s --source_notes
                        )
                    ON CONFLICT (id) DO UPDATE SET 
                        name=EXCLUDED.name
                        , first_name=EXCLUDED.first_name
                        , last_name=EXCLUDED.last_name
                        , artist_name_slug=EXCLUDED.artist_name_slug
                        , printed_aliases=EXCLUDED.printed_aliases
                        , tags=EXCLUDED.tags
                        , links=EXCLUDED.links
                        , source_notes=EXCLUDED.source_notes
                    """,
                    (
                        row_id
                        , row['name']
                        , row['first_name']
                        , row['last_name']
                        , row['artist_name_slug']
                        , Jsonb(printed_aliases_list)
                        , Jsonb(tags_list)
                        , Jsonb(links_dict)
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