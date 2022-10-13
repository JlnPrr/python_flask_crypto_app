import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import base64


gains = pd.read_csv('data.csv')
df = pd.DataFrame(gains)
plt.figure(figsize=(19, 8))
plt.plot(gains.Date, gains.Montant, c='#1fc36c')

plt.xlabel('Dates par 24h', fontsize=13)
plt.ylabel('Montants en euros', fontsize=13)
plt.title('Evolution des gains', fontweight='bold', fontsize=18)
plt.savefig('static/images/gains.png')

data_uri = base64.b64encode(open('static/images/gains.png', 'rb').read()).decode('utf-8')
img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
print(img_tag)

#plt.show()