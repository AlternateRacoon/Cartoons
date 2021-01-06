from urllib.request import Request, urlopen
import re

url1 = "http://www.toonova.net/bobs-burgers?page=4"
url2 = url1 + "11"
url2 = int(re.findall("page=(.*?)11", url2)[0]) - 1
categ = url1 + str(url2)
print(categ.replace(str(url2),""))