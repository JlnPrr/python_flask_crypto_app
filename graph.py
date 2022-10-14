import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import base64

#En dessous de 992px
gains = pd.read_csv('data.csv')
df = pd.DataFrame(gains)
plt.figure(figsize=(14, 17)).set_facecolor('#100f0f')
plt.plot(gains.Date, gains.Montant, c='#1fc36c', lw=3)

plt.xticks(color='white')
plt.yticks(color='white')

ax = plt.gca()
ax.axes.xaxis.set_ticks([])
ax.set_facecolor('#171717')

plt.xlabel('Dates par 24h', fontsize=28, labelpad=14, color='white')
plt.ylabel('Montants en euros', fontsize=28, labelpad=14, color='white')
plt.title('Evolution des gains', fontweight='bold', fontsize=30, pad=24, color='white')

plt.savefig('static/images/gains.png')

data_uri = base64.b64encode(open('static/images/gains.png', 'rb').read()).decode('utf-8')
img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
print(img_tag)

#plt.show()


#A partir de 992px
gains = pd.read_csv('data.csv')
df = pd.DataFrame(gains)
plt.figure(figsize=(19, 13)).set_facecolor('#100f0f')
plt.plot(gains.Date, gains.Montant, c='#1fc36c', lw=3)

plt.xticks(color='white')
plt.yticks(color='white')

ax = plt.gca()
ax.axes.xaxis.set_ticks([])
ax.set_facecolor('#171717')

plt.xlabel('Dates par 24h', fontsize=19, labelpad=14, color='white')
plt.ylabel('Montants en euros', fontsize=19, labelpad=14, color='white')
plt.title('Evolution des gains', fontweight='bold', fontsize=22, pad=15, color='white')

plt.savefig('static/images/gains_large.png')

data_uri = base64.b64encode(open('static/images/gains_large.png', 'rb').read()).decode('utf-8')
img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
#print(img_tag)

#plt.show()