import os
import requests


url= 'https://raw.githubusercontent.com/Madlhawa/Web-Scrape/db7f94b9936be83a2782ac30c1c48e375238ca8c/LankaTronics/LankaTronics/middlewares.py'

r= requests.get(url)

f = open("F:/ab.py" ,"w")
f.write('r.content')
print(r.content)

    