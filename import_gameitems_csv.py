import psycopg
from psycopg.types.json import Jsonb
import csv
import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()


import_csvs = [
    #'import/ccgdata_gameitems_altered.csv'
    #, 'import/ccgdata_gameitems_anime-madness.csv'
    #, 'import/ccgdata_gameitems_argent-saga.csv'
    #, 'import/ccgdata_gameitems_austin-powers.csv'
    #, 'import/ccgdata_gameitems_banemaster.csv'
    #, 'import/ccgdata_gameitems_dice-masters.csv'
    #, 'import/ccgdata_gameitems_doomtown-reloaded.csv'
    #, 'import/ccgdata_gameitems_dragon-ball-z-trading-card-game-(2014).csv'
    #, 'import/ccgdata_gameitems_echelons-of-fire.csv'
    #, 'import/ccgdata_gameitems_echelons-of-fury.csv'
    #, 'import/ccgdata_gameitems_flights-of-fantasy.csv'
    #, 'import/ccgdata_gameitems_guardians.csv'
    #, 
    'import/ccgdata_gameitems_gridiron.csv'
    #, 'import/ccgdata_gameitems_hecatomb.csv'
    #, 'import/ccgdata_gameitems_highlander.csv'
    #, 'import/ccgdata_gameitems_hyborian-gates.csv'
    #, 'import/ccgdata_gameitems_kult.csv'
    #, 'import/ccgdata_gameitems_lol-surprise.csv'
    #, 'import/ccgdata_gameitems_magi-nation-duel.csv'
    #, 'import/ccgdata_gameitems_marvel-recharge.csv'
    #, 'import/ccgdata_gameitems_marvel-superheroes-collectors-club.csv'
    #, 'import/ccgdata_gameitems_metazoo-2021.csv'
    #, 'import/ccgdata_gameitems_monster-magic.csv'
    #, 'import/ccgdata_gameitems_monty-python.csv'
    #, 'import/ccgdata_gameitems_on-the-edge.csv'
    #, 'import/ccgdata_gameitems_ophidian-2350.csv'
    #, 'import/ccgdata_gameitems_overpower.csv'
    #, 'import/ccgdata_gameitems_powercardz.csv'
    #, 'import/ccgdata_gameitems_racing-challenge.csv'
    #, 'import/ccgdata_gameitems_rage.csv'
    #, 'import/ccgdata_gameitems_redemption.csv'
    #, 'import/ccgdata_gameitems_sand-land.csv'
    #, 'import/ccgdata_gameitems_simcity.csv'
    #, 'import/ccgdata_gameitems_star-trek-ccg.csv'
    #, 'import/ccgdata_gameitems_star-wars-ccg.csv'
    #, 'import/ccgdata_gameitems_tempest-of-the-gods.csv'
    #, 'import/ccgdata_gameitems_the-crow.csv'
    #, 'import/ccgdata_gameitems_the-nightmare-before-christmas.csv'
    #, 'import/ccgdata_gameitems_the-spoils.csv'
    #, 'import/ccgdata_gameitems_the-super-mario-bros-movie.csv'
    #, 'import/ccgdata_gameitems_tomb-raider.csv'
    #, 'import/ccgdata_gameitems_tops-attax.csv'
    #, 'import/ccgdata_gameitems_towers-in-time.csv'
    #, 'import/ccgdata_gameitems_vampire-the-masquerade-rivals.csv'
    #, 'import/ccgdata_gameitems_wars.csv'
    #, 'import/ccgdata_gameitems_world-of-warriors.csv'
    #, 'import/ccgdata_gameitems_wwe-raw-deal.csv'
    #, 'import/ccgdata_gameitems_xena.csv'
    #, 'import/ccgdata_gameitems_xxxenophile.csv'    


     
    # 'import/ccgdata_gameitems_.csv'
    # 'import/ccgdata_gameitems_.csv'
    # 'import/ccgdata_gameitems_.csv'

]


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
                print(row)
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
                if 'imaged' in row and row['imaged'] == "1":
                    imaged_bool = True 
                else: 
                    imaged_bool = False
                if 'documented' in row and row['documented'] == "1":
                    documented_bool = True 
                else: 
                    documented_bool = False
                cur.execute(
                    """
                    INSERT INTO gameitems_item (
                        id, name, attributes, images, source_notes, 
                        functional_name, item_name_slug, imaged, 
                        documented, game_id, set_id, source
                        ) 
                    VALUES (
                        %s --$1 id (unique uuid)
                        , %s --$2 name (text)
                        , %s --$3 attributes (dict)
                        , %s --$4 images (list)
                        , %s --$5 source_notes (dict)
                        , %s --$6 functional_name (text)
                        , %s --$7 item_name_slug (unique text)
                        , %s --$8 imaged (bool)
                        , %s --$9 documented (bool)
                        , %s --$10 game_id (uuid, foreign key)
                        , %s --$11 set_id (uuid, foreign key)
                        , %s --$12 source (text)
                        )
                    ON CONFLICT (id) DO UPDATE SET 
                        name=EXCLUDED.name
                        , attributes=EXCLUDED.attributes
                        , images=EXCLUDED.images
                        , source_notes=EXCLUDED.source_notes
                        , functional_name=EXCLUDED.functional_name
                        , item_name_slug=EXCLUDED.item_name_slug
                        , imaged=EXCLUDED.imaged
                        , documented=EXCLUDED.documented
                        , game_id=EXCLUDED.game_id
                        , set_id=EXCLUDED.set_id
                        , source=EXCLUDED.source
                    """,
                    (
                        row_id, row['item_name']
                        , Jsonb(attributes_dict)
                        , Jsonb(images_dict)
                        , Jsonb(source_notes_dict)
                        , row['functional_name']
                        , row['game_set_item_slug']
                        , imaged_bool
                        , documented_bool
                        , row['game_id']
                        , row['set_id']
                        , row['source']
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
    for import_csv_path in import_csvs:
        import_game_items(import_csv_path, database_url)

if __name__ == "__main__":
    main()