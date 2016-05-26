# Download polish counties data from WikiData using its API
import urllib2, urllib, json, csv, cStringIO, re

def extract(i,k):
  if i.has_key(k):
    return i[k].get('value').encode('utf-8')
  return None

api_url = 'https://query.wikidata.org/sparql?query=%s&format=json'
point = re.compile('Point\(([.0-9]+)\s+([.0-9]+)\)')

# Query in SPARQL
#   Select 
query = """
SELECT DISTINCT ?item ?itemLabel ?_coat_of_arms_image ?_coordinate_location WHERE {
  { ?item wdt:P31 wd:Q925381. }
  UNION
  { ?item wdt:P31 wd:Q247073. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "pl". }
  OPTIONAL { ?item wdt:P94 ?_coat_of_arms_image. }
  OPTIONAL { ?item wdt:P625 ?_coordinate_location. }
}
"""

resp = json.load(urllib2.urlopen(api_url % urllib.quote(query)))

out = cStringIO.StringIO()
w = csv.writer(out)

for item in resp['results']['bindings']:
  pos = extract(item, '_coordinate_location')
  if not pos:
    continue
  pos = point.match(pos)
  
  w.writerow([
    extract(item, 'item').split('/')[-1], 
    extract(item, 'itemLabel'),
    extract(item,'_coat_of_arms_image'),
    pos.group(1),
    pos.group(2)
  ])
  
print out.getvalue()


