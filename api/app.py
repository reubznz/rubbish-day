from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route("/", methods=['GET'])
def rubbish_day():
    import sys
    import json
    import requests
    import ssl
    import urllib3
    from datetime import datetime
    from bs4 import BeautifulSoup

    class CustomHttpAdapter (requests.adapters.HTTPAdapter):
        # "Transport adapter" that allows us to use custom ssl_context.

        def __init__(self, ssl_context=None, **kwargs):
            self.ssl_context = ssl_context
            super().__init__(**kwargs)

        def init_poolmanager(self, connections, maxsize, block=False):
            self.poolmanager = urllib3.poolmanager.PoolManager(
                num_pools=connections, maxsize=maxsize,
                block=block, ssl_context=self.ssl_context)

    def get_legacy_session():
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        session = requests.session()
        session.mount('https://', CustomHttpAdapter(ctx))
        return session

    # Suppress only the single warning from urllib3 needed.
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    # For debug output
    from pathlib import Path
    scriptName = str(Path(__file__).name)
    debugmode = False

    # Initialise strings to prevent errors later
    # addressId = '12344871009'
    addressId = request.args.get('addressid')
    baseUrl = 'https://www.aucklandcouncil.govt.nz'

    thisUrl = '/rubbish-recycling/rubbish-recycling-collections/Pages/collection-day-detail.aspx?an='+addressId
    url = baseUrl+thisUrl
    if debugmode :
        sys.stderr.write(scriptName+': Requesting page from '+thisUrl+'\n')
    try:
        # response = requests.get(url), verify=False)
        response = get_legacy_session().get(url)
        if debugmode :
            sys.stderr.write(scriptName+': > requests.get response code is '+str(response.status_code)+'\n')
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        sys.stderr.write(scriptName+': > Page GET says '+str(err)+'\n')
        sys.stderr.write(scriptName+': > Error is fatal, exiting with no output\n')
        exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')
    addressBlock = soup.find_all(attrs={'class': 'm-b-2'})
    cardBlock = soup.find_all(attrs={'class': 'card-block'})
    householdBlock = None
    for block in cardBlock :
        try :
            blockId = block['id']
            if 'HouseholdBlock' in blockId :
                householdBlock = block
        except KeyError :
            pass
    if householdBlock :
        if debugmode :
            sys.stderr.write(scriptName+': > Found collection information\n')
    else :
        sys.stderr.write(scriptName+': > Could not find collection information, exiting with no output\n')
        exit(1)

    output = {}

    if debugmode :
        sys.stderr.write(scriptName+': Straining information from soup\n')
    links = householdBlock.find_all(attrs={'class': 'links'})

    # Current collection cycle
    output['value'] = links[0].find(attrs={'class':'m-r-1'}).string
    
    # Address details
    output['address'] = addressBlock[0].string
    
    # Create a timestamp from the date, assume 7am and NZT
    output['datetime'] = datetime.strptime(output['value']+datetime.now().astimezone().strftime(' 07 %Y %z'), '%A %d %B %H %Y %z').strftime('%Y-%m-%dT%H:%M:%S%z')
    recycleBlock = links[0].find(attrs={'class':'icon-recycle'})
    if recycleBlock :
        output['collection_type'] = 'Recycle'
        output['icon'] = 'mdi:recycle'
    else :
        output['collection_type'] = 'Rubbish'
        output['icon'] = 'mdi:trash-can'

    # Next collection cycle
    recycleBlock = None
    output['next_collection_date'] = links[1].find(attrs={'class':'m-r-1'}).string
    output['next_collection_datetime'] = datetime.strptime(output['next_collection_date']+datetime.now().astimezone().strftime(' 07 %Y %z'), '%A %d %B %H %Y %z').strftime('%Y-%m-%dT%H:%M:%S%z')
    recycleBlock = links[1].find(attrs={'class':'icon-recycle'})
    if recycleBlock :
        output['next_collection_type'] = 'Recycle'
        output['next_collection_icon'] = 'mdi:recycle'
    else :
        output['next_collection_type'] = 'Rubbish'
        output['next_collection_icon'] = 'mdi:trash-can'

    # print(json.dumps(output))
    return json.dumps(output)
