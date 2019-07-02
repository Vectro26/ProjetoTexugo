import requests,json 


def TechnologyIdentification(URL):

    URLConcat="https://whatcms.org/APIEndpoint/Technology?key=2422ea8d5453897e9a1f689b32b3e125da8e6305d1a887b8078389a1d9fb8b437b50fe&url="+URL
   
    results = requests.get(URLConcat, headers = { 'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330'})
    if results.status_code == 200:
            dataload = json.loads(results.content)

            return dataload['results']
    else:
            return "None"
