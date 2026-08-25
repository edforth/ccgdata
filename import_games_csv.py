import psycopg
from psycopg.types.json import Jsonb
import csv
import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()


import_csv_path = 'import/ccgdata_games.csv'

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
                publishers_list = json.loads(row['publishers']) 
                languages_list = json.loads(row['languages']) 
                tags_list = json.loads(row['tags']) 
                links_dict = json.loads(row['links']) 
                related_game_ids_list = json.loads(row['related_game_ids']) 

                try:
                    source_notes_dict = json.loads(row['source_notes'])
                except (json.JSONDecodeError, ValueError):
                    source_notes_dict = {}
                
                if 'id' in row and is_valid_uuid(row['id']) == True:
                    row_id = row['id']
                else:
                    row_id = uuid.uuid4()
                    # attempting to convert the above to an upsert
                cur.execute(
                    """
                    INSERT INTO gameitems_game (
                        id
                        , name
                        , published_name
                        , original_release_year
                        , original_release_month
                        , original_release_day
                        , publishers
                        , languages
                        , tags
                        , links
                        , related_game_ids
                        , is_independently_customized
                        , is_dead
                        , has_english_release
                        , in_scope
                        , source_notes
                        , comments
                        , game_name_slug
                        ) 
                    VALUES (%s, %s, %s, nullif(%s, '')::INTEGER, nullif(%s, '')::INTEGER, nullif(%s, '')::INTEGER, %s, %s, %s, %s, %s
                        , nullif(%s, '')::BOOL, nullif(%s, '')::BOOL, nullif(%s, '')::BOOL, nullif(%s, '')::BOOL, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET 
                        name=EXCLUDED.name
                        , published_name=EXCLUDED.published_name
                        , original_release_year=EXCLUDED.original_release_year
                        , original_release_month=EXCLUDED.original_release_month
                        , original_release_day=EXCLUDED.original_release_day
                        , publishers=EXCLUDED.publishers
                        , languages=EXCLUDED.languages
                        , tags=EXCLUDED.tags
                        , links=EXCLUDED.links
                        , related_game_ids=EXCLUDED.related_game_ids
                        , is_independently_customized=EXCLUDED.is_independently_customized
                        , is_dead=EXCLUDED.is_dead
                        , has_english_release=EXCLUDED.has_english_release
                        , in_scope=EXCLUDED.in_scope
                        , source_notes=EXCLUDED.source_notes
                        , comments=EXCLUDED.comments
                        , game_name_slug=EXCLUDED.game_name_slug
                    """,
                    (
                        row_id
                        , row['name']
                        , row['published_name']
                        , row['original_release_year']
                        , row['original_release_month']
                        , row['original_release_day']
                        , Jsonb(publishers_list)
                        , Jsonb(languages_list)
                        , Jsonb(tags_list)
                        , Jsonb(links_dict)
                        , Jsonb(related_game_ids_list)
                        , row['is_independently_customized']
                        , row['is_dead']
                        , row['has_english_release']
                        , row['in_scope']
                        , Jsonb(source_notes_dict)
                        , row['comments']
                        , row['game_name_slug']
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