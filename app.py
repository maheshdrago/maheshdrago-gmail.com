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

            if country.lower() == 'us' or country.lower()=='america':
                country = 'usa'
        else:
            country = 'india'

        my_link = requests.get('https://www.worldometers.info/coronavirus/#countries')
        soup = BeautifulSoup(my_link.text,'html.parser')
        table = soup.find('tbody')
        rows = table.find_all('tr')
        d = []
        for i in rows:
            data = i.find_all('td')
            temp = []
            for j in data:
                temp.append(j.text)
            d.append(temp)
        flag = False
        for i in d:
            if i[0].upper()==country.upper():
                country = i[0]
                total = i[1]
                active = i[6]
                deaths = i[3]
                cured = i[5]
                flag =True
                break
        if flag:
            return render_template('base.html',total=total,deaths=deaths,cured=cured,active=active,country=country.capitalize())

        else:
            flash("Sorry data does not exist for this country right now please try again later...")
            return redirect(url_for('change'))

    except:
        flash("Sorry data does not exist for this country right now please try again later...")
        return redirect(url_for('change'))




if __name__ == '__main__':
    app.run(debug=True)
