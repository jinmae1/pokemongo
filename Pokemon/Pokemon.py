import pymongo
import dotenv
import requests

if __name__ == '__main__':
    url = 'https://pokeapi.co/api/v2/pokemon/'

    try:
        env = dotenv.dotenv_values('.env')
        HOST = env['host']
        PORT = env['port']
    except KeyError as ke:
        print(f'KeyError: {ke} does not exist')
        exit()
    except FileNotFoundError:
        print('.env file does not exist')
        exit()

    client = pymongo.MongoClient(f'mongodb://{HOST}:{PORT}/')
    db = client['pokeapi']
    collection = db['pokemon']
    # db.pokemon.createIndex( { id: 1 }, { unique: true } )
    collection.create_index('id', unique=True)

    cnt = 0
    range_end = 151
    for i in range(0, range_end):
        res = requests.get(url + str(i + 1))
        if res.status_code == 200:
            res_dict = res.json()
            try:
                x = collection.insert_one(res_dict)
                print(f'{res_dict["id"]}. {res_dict["name"]} inserted')
                cnt += 1
            except pymongo.errors.DuplicateKeyError:
                print(f'{res_dict["id"]}. {res_dict["name"]} already exists')
            except Exception as e:
                print(e)
        else:
            print(f'status code: {res.status_code} for {url + str(i + 1)}')

    print(f'==== Total of {cnt} documents have been inserted ====')
    print(f'And {range_end - cnt} failed')
