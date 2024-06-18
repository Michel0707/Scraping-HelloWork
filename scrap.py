from urllib.parse import urljoin
from bs4 import BeautifulSoup 
import requests 




# url pour la connexion à l'api
url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
# urls des offres d'emploi par ville
urls_cities = {
    "Bordeaux" : "https://candidat.francetravail.fr/offres/emploi/bordeaux/v9",
    "Rennes" : "https://candidat.francetravail.fr/offres/emploi/rennes/v11",
    "Paris" : "https://candidat.francetravail.fr/offres/recherche?lieux=75D&offresPartenaires=true&rayon=10&tri=0"
}

client_id=  "PAR_recruitmenttest_7c98cbc1f813ab2fa9cee3d9eec46ae081d7f7aef51cd148ca6d34204523c4df",
client_secret= "a97a1f8455a189da250660da4e24781b1fdd5bc4fe7eb0d40c48133b56c834b0",
scope= "api_offresdemploiv2"

# données de connexion
payload ={
        "grant_type": "client_credentials",
        "client_id" : client_id,
        "client_secret" : client_secret,
        "scope" : scope
        }



# fonction pour charger plus d'emploies plus d'offre sur la page
def charge_jobs_page(soup,url,headers,payload,page):
    
    new_url = "https://candidat.francetravail.fr/offres/emploi.rechercheoffre:afficherplusderesultats/"+str(page*20)+"-"+str((page*20)+19)+"/0?t:ac=bordeaux/v9"
    new_response = requests.post(new_url,data=payload)
    
    if new_response.status_code == 200:
        new_soup = BeautifulSoup(new_response.text, "lxml")
        return new_soup.find_all(class_="result")
    else:
        return []



def scrap_offers(city):
    # connexion à l'api
    results_jobs = []
    connection_resp = requests.post(url, data=payload)
            
    if connection_resp.status_code == 200:
        token_resp = connection_resp.json()
        access_token = token_resp.get("access_token") # creation d'un token
        url_city = urls_cities[city]

        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url_city, headers=headers)

        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, "lxml")
            jobs_boxes_list = soup.find_all(class_="result")
                        
            if jobs_boxes_list:
                for job_boxe in jobs_boxes_list:
                    parse= {}
                    if title := job_boxe.find("a").find("h2"):
                        parse["title"] = title.get_text(strip=True)

                    if url_job := job_boxe.find("a")["href"]:
                        parse["url"] = urljoin(url_city,url_job)
                        
                    response_job = requests.get(parse["url"], headers=headers)
                    
                    if response_job.status_code == 200:

                        soup_job = BeautifulSoup(response_job.text, "lxml")
                        job_body = soup_job.find_all("div",class_="modal-body")
                        
                        if description := job_body[1].find(class_="row").find("p"):
                            parse["description"]  = description.get_text(strip=True)
                            
                        if company := job_body[1].find(class_="media-body").find("h3"):
                            parse["company"]  = company.get_text(strip=True)
                            
                        if contrat := job_body[1].find(class_="row").find("dd"):
                            parse["contrat"]  = contrat.get_text(strip=True)
                        
                        parse["city"] = city
                    #if parse not in results_jobs:
                        results_jobs.append(parse)
                        #print(f'\n\n555555555555555555555µµµµµµµµµ\n\n {results_jobs[0]} µµµµµµµµµµµµµµµµPPPPPPPPPPPPPP\n\n')

            else:
                print("Element not found")
        else:
            print("Faild acces page")
    else:
        print("Failed create token")
    return results_jobs


















# page = urlopen(url)
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")

# print(html)"""

# id mots cles : """idmotsCles-selectized_input-description""""
# id Ville  :  " idlieux-selectized_input-description " "