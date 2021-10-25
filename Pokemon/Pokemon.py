import pymongo
import json
import requests

if __name__ == '__main__':
    url = 'https://pokeapi.co/api/v2/pokemon/'
    with open('./mongodb.json') as json_file:
        json_data = json.load(json_file)

        print(json_data)
        host = json_data['host']
        port = json_data['port']


        client = pymongo.MongoClient(f'mongodb://{host}:{port}/')
        print(client.list_database_names());
        db = client['pokeapi']
        collection = db['pokemon']

        for i in range(151):
            res = requests.get(url + str(i + 1))
            if res.status_code == 200:
                res_dict = res.json()
                x = collection.insert_one(res_dict)
                print(f'Inserted {str(i + 1)}')
    
        print('Insertion finished')
