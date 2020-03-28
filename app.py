from flask import Flask,render_template,request,redirect,url_for,flash
import requests
from bs4 import BeautifulSoup




app = Flask(__name__)
app.config["SECRET_KEY"]='iwonttellyou'



@app.route('/',methods=['GET','POST'])
def change():
    try:
        if request.method== 'POST':
            country = request.form['country']

            if country.lower() == 'usa' or country.lower()=='america':
                country = 'us'
        else:
            country = 'india'

        my_link = requests.get('https://www.worldometers.info/coronavirus/country/'+country)
        soup = BeautifulSoup(my_link.text,'html.parser')


        deaths = soup.find_all('div',{'class':'maincounter-number'})

        active = soup.find_all('div',{'class':'number-table-main'})[0].text

        stats = []

        for i in deaths:
            stats.append(i.text.replace('\n','').replace(' ',''))
        total,deaths,cured = stats[0],stats[1],stats[2]
    except:
        flash("Sorry data does not exist for this country right now please try again later...")
        return redirect(url_for('change'))



    return render_template('base.html',total=total,deaths=deaths,cured=cured,active=active,country=country.capitalize())

if __name__ == '__main__':
    app.run(debug=True)
