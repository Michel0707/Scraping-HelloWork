import pymongo
import pymongo.errors

def connection_db():
    try:
        client = pymongo.MongoClient('mongodb+srv://kilangalangamichel:i4hrzF0GLUHQD7cO@cluster0.hnwotk7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        db = client['job_offers_db']
        collection = db['offers']
        return collection
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(f'Erreur de connexion {err}')

def insert_data(data,collection):
    return collection.insert_many(data)

def show_all_jobs(collection):
    for x in find_all(collection):
        print(x)
        
def find_all(collection):
    return collection.find({})

def find_by_city(collection,city):
    return collection.find({"city":city})

def get_companies(collection):
    return collection.distinct('company')

def get_contrats(collection):
    return collection.distinct('contrat')


def find_by_contrat(collection,contrat):
    return collection.find({"contrat":contrat})