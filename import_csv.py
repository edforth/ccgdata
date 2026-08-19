import psycopg
from psycopg.types.json import Jsonb
import csv
import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()


import_csvs = [
    'import/rage_items.csv'
]

import_csv_path = 'import/rage_items.csv'

def is_valid_uuid(potential_uuid):
    try:
        uuid.UUID(str(potential_uuid))
        return True
    except ValueError:
        return False

def import_game_items(import_csv_path, database_url):
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
                attributes_dict = json.loads(row['attributes']) 
                images_dict = json.loads(row['images']) 
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
                    "INSERT INTO gameitems_item ("
                    "id, name, attributes, images, source_notes, "
                    "functional_name, item_name_slug, imaged, "
                    "documented, game_id, set_id, source) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    "ON CONFLICT (id) DO UPDATE SET "
                    "name=EXCLUDED.name, attributes=EXCLUDED.attributes, images=EXCLUDED.images, source_notes=EXCLUDED.source_notes, "
                    "functional_name=EXCLUDED.functional_name, item_name_slug=EXCLUDED.item_name_slug, imaged=EXCLUDED.imaged, "
                    "documented=EXCLUDED.documented, game_id=EXCLUDED.game_id, set_id=EXCLUDED.set_id, source=EXCLUDED.source",
                    (row_id, row['item_name'], Jsonb(attributes_dict), Jsonb(images_dict), Jsonb(source_notes_dict)
                    , row['functional_name'], row['game_set_item_slug'], row['imaged']
                    , row['documented'], row['game_id'], row['set_id'], row['source'])
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
    for import_csv_path in import_csvs:
        import_game_items(import_csv_path, database_url)

if __name__ == "__main__":
    main()