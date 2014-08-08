from lxml import etree
from io import StringIO, BytesIO
import csv

def add_to_dict(val,dict):
	if val not in dict:
		dict[val] = 1
	else:
		dict[val] += 1

states_file = csv.writer(open("fcc_comments_by_state.csv","wb"))
cities_file = csv.writer(open("fcc_comments_by_city.csv","wb"))
zips_file = csv.writer(open("fcc_comments_by_zip.csv","wb"))

states_file.writerow(["State","Count"])
cities_file.writerow(["City","Count"])
zips_file.writerow(["Zip","Count"])

file_names = ["14-28-RAW-Solr-1.xml","14-28-RAW-Solr-2.xml","14-28-RAW-Solr-3a.xml","14-28-RAW-Solr-3b.xml","14-28-RAW-Solr-4.xml","14-28-RAW-Solr-5.xml"]



states = {}
cities = {}
zip_codes = {}

parser = etree.XMLParser(huge_tree=True)
for file_name in file_names:
	tree = etree.parse(file_name,parser)
	result = tree.xpath("/response/result")
	docs = result[0].xpath("doc")

	for doc in docs:
		try:
			state = doc.xpath("arr[@name='stateCd']/str")[0].text.encode("utf-8")
		except:
			state = "NONE"
		try:
			city = doc.xpath("arr[@name='city']/str")[0].text.encode("utf-8") + ", " + state
		except:
			city = "NONE" + ", " + state
		try:
			zip_code = doc.xpath("arr[@name='zip']/str")[0].text.encode("utf-8")
		except:
			zip_code = "NONE"
		add_to_dict(state,states)
		add_to_dict(city,cities)
		add_to_dict(zip_code,zip_codes)

for state in states:
	states_file.writerow([state,states[state]])
for city in cities:
	cities_file.writerow([city,cities[city]])
for zip_code in zip_codes:
	zips_file.writerow([zip_code,zip_codes[zip_code]])
