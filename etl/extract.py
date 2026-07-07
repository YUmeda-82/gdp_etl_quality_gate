import requests

def fetch_gdp_per_capita() -> list[dict]:
    """
    Extracts raw data from the world bank api.
    Returns a list of python dictionaries with LatAm countries and indicator data.
    """

    url = (
        "https://api.worldbank.org/v2/country/"
        "BR;AR;CL;CO;PE;UY;PY;BO;EC;VE;GY;SR"
        "/indicator/NY.GDP.PCAP.CD?format=json&per_page=1000")
    
    response = requests.get(url) #sending HTTP GET request to api
    response.raise_for_status() #raising exception if response status = error

    data = response.json() #converts raw http response to py dict
    
    return data[1] #data[0] pagination metada, actual records start at data[1]