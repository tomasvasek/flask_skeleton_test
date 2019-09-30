"""
Logic for dashboard related routes
"""
from flask import Blueprint, render_template
from .forms import LogUserForm, secti,masoform,vstupnitestform
from ..data.database import db
from ..data.models import LogUser
blueprint = Blueprint('public', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('public/index.tmpl')

@blueprint.route('/loguserinput',methods=['GET', 'POST'])
def InsertLogUser():
    form = LogUserForm()
    if form.validate_on_submit():
        LogUser.create(**form.data)
    return render_template("public/LogUser.tmpl", form=form)

@blueprint.route('/loguserlist',methods=['GET'])
def ListuserLog():
    pole = db.session.query(LogUser).all()
    return render_template("public/listuser.tmpl",data = pole)

@blueprint.route('/secti', methods=['GET','POST'])
def scitani():
    form = secti()
    if form.validate_on_submit():
        return render_template('public/vystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/secti.tmpl', form=form)

@blueprint.route('/maso', methods=['GET','POST'])
def masof():
    form = masoform()
    if form.validate_on_submit():
        return render_template('public/masovystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/maso.tmpl', form=form)

@blueprint.route('/vstupni_test', methods=['GET','POST'])
def vstupnitest():
    from .forms import vstupnitestform
    from ..data.models.vysledky import Vysledky
    from sqlalchemy import func
    form = vstupnitestform()
    if form.validate_on_submit():
        vysledek=0
        if form.otazka1.data == 2:
            vysledek = vysledek+1
        if form.otazka2.data == 0:
            vysledek = vysledek +1
        if form.otazka3.data.upper() == "ELEPHANT":
            vysledek = vysledek + 1
            i = Vysledky(username=form.Jmeno.data,hodnoceni=vysledek)
            db.session.add(i)
            db.session.commit()
            dotaz = db.session.query(Vysledky.username,func.count(Vysledky.hodnoceni).
                                     label("suma")).group_by(Vysledky.username).all()
            return render_template('public/vysledekvystup.tmpl',data=dotaz)
    return render_template('public/vstupnitest.tmpl', form=form)

@blueprint.route('/vstupni_test', methods=['GET'])
def testvstupu():
    from ..data.models.vysledky import Vysledky
    from sqlalchemy import func

    dotaz = db.session.query(Vysledky.username, func.count(Vysledky.hodnoceni).label("suma")).group_by(
        Vysledky.jmeno).all()
    return render_template('public/vstupnitest.tmpl',data=dotaz)

@blueprint.route('/vystupuzivatele/<jmeno>', methods=['GET'])
def testvystupuuzivatel(jmeno):
    from ..data.models.vysledky import Vysledky
    dotaz = db.session.query(Vysledky.username,Vysledky.hodnoceni).\
         filter((Vysledky.username==jmeno).all())
    return render_template('public/vysledekvystupuzivatel.tmpl',data=dotaz,jmeno=jmeno)

@blueprint.route('/vystupjson', methods=['GET'])
def vystupjson():
    from flask import jsonify
    lastfm_user=["frnata","jirka","lukas"]
    payload = lastfm_user
    payload = {
    }

@blueprint.route('/nactenijson', methods=['GET','POST'])
def nactenijson():
    from flask import jsonify
    import requests, os
    os.environ['NO_PROXY'] = '127.0.0.1'
    proxies = {
        "http": None,
        "https": "http://192.168.1.1:800",
    }
    response = requests.get("http://192.168.10.1:5000/nactenijson", proxies = proxies)
    json_res = response.json()
    data = []
    for radek in json_res["list"]:
         data.append(radek["main"]["temp"])
        #return render_template("public/dataprint.tmpl",data=data)
    legend = 'Monthly Data'
    return render_template('public/chart.tmpl', values=data, labels=data, legend=legend)
    #return jsonify(json_res)


@blueprint.route("/graf_solo")
def chart():
    from ..data.models.vysledky import Vysledky
    data = []

    legend = 'Tak tady bude graf'
    labels = [Vysledky]
    values = ["1", "2", "3", "4", "5"]
    return render_template('public/chart_solo.tmpl', values=data, labels=labels, legend=legend)
