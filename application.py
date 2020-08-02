from flask import Flask, render_template, redirect, url_for
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length
from flask_bootstrap import Bootstrap
import requests
from bs4 import BeautifulSoup
import time
starttime = time.time()

application=app=Flask(__name__)
application.secret_key = "Secret_Key"
application.config['MYSQL_HOST'] = 'aws-new.c3kqx3hrswsn.us-east-2.rds.amazonaws.com'
application.config['MYSQL_USER'] = 'admin'
application.config['MYSQL_PASSWORD'] = 'Oracle1234'
application.config['MYSQL_DB'] = 'test1'
mysql = MySQL(application)
Bootstrap(application)

class InputForm(FlaskForm):
    flink = StringField('flink',validators=[InputRequired(), Length(min=4, max=65)])


def priceTracker(url):



    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    names = soup.find_all('div',{'class':'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'})[0].find('h1').text

    price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    try:
        con = mysql.connection.cursor()
        a = names
        b = price
        con.execute("INSERT INTO STOCK_NEW (NAMEC,PRICE,TNOW) values('" + a + "','" + b + "',CURRENT_TIMESTAMP)")
        mysql.connection.commit()

        print("value inserted successful")
    finally:
        print("sorry")





@application.route('/input', methods=['GET', 'POST'])
def input():
    form = InputForm()
    if form.validate_on_submit():
        while True:
            priceTracker(form.flink.data)  # amazon
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))

    return render_template('input.html', form=form)


@application.route("/")
def Index():
    conn = mysql.connection.cursor()

    conn.execute("select * from STOCK_NEW")
    data = conn.fetchall()
    return render_template("index.html", value=data)


if __name__ == "__main__":
    application.run(debug=True)
