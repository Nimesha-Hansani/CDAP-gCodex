import os
import requests


url= 'https://raw.githubusercontent.com/laveesha/Data-Minin-App/10d33bfb6dbe15579946459b7861dad56c681910/ShinyApp/www/google-analytics.js'

r= requests.get(url)

print(r.content)

    