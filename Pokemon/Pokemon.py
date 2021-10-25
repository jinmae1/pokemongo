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
        # print(client.list_database_names());
        db = client['pokeapi']
        collection = db['pokemon']

        cnt = 0
        for i in range(151):
            res = requests.get(url + str(i + 1))
            if res.status_code == 200:
                res_dict = res.json()
                q = collection.find_one({'id' :  i + 1}, {'id': 1, 'name': 1})
                if q:
                    print(f'{q["id"]}. {q["name"]} already exists. Skipping')
                    continue
                x = collection.insert_one(res_dict)
                print(f'{res_dict["id"]}. {res_dict["name"]} inserted')
                cnt += 1
            else:
                print(f'status code: {res.status_code} for {url + str(i + 1)}')
    
        print(f'==== Total of {cnt} documents have been inserted ====')
