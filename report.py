import data_base as db


def repartition_contrat(contrats,collection):
    offers_by_contrat = {}
    for comp in contrats:
        offers_by_contrat[comp] = len(list(db.find_by_contrat(collection,comp)))
    return offers_by_contrat

def print_text(numbre_total_offers,numbre_offer_by_city,num_companies,offers_by_contrat):
    print('*************** RAPPORT ***************')
    print(f"{numbre_total_offers} documents ont été récupérés.")
    print(f'{num_companies} entreprises ont été récupérées')
    print(f'Voici comment se repartissent les differents types de contrat \n{offers_by_contrat}\n')
    

def report(collection):
    # le nombre total des documents recuperés
    numbre_offer_by_city = {}
    numbre_total_offers = len(list(db.find_all(collection)))
    for x in ["Bordeaux", "Rennes", "Paris"]:
        numbre_offer_by_city[x] = len(list(db.find_by_city(collection,x)))
    companies = db.get_companies(collection)
    num_companies = len(companies)
    contrats = db.get_contrats(collection)
    offers_by_contrat= repartition_contrat(contrats,collection)
    
    print_text(numbre_total_offers,numbre_offer_by_city,num_companies,offers_by_contrat)
    
    
    


