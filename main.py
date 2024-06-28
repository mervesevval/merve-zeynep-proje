from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "yxrh2691"

@app.route("/") 
def anasayfa():

    if "isim" in session: 
        return render_template("index.html")
    else:
        return render_template("giris_yap.html")

@app.route("/cikis") 
def cikis():
    session["isim"] = None
    session["sifre"] = None
    return redirect("/giris")

@app.route("/giris") 
def giris_yap():
    return render_template("giris_yap.html")

@app.route("/bilgiler", methods=["POST"])
def kayit():
    isim = request.form["isim"]
    email = request.form["email"]
    sifre = request.form["sifre"]

    db = sqlite3.connect("database.db")
    querry = f"SELECT * FROM kullanicilar WHERE ad = '{isim}'"
    cursor = db.cursor()
    cursor.execute(querry)
    results = cursor.fetchall() 
    db.commit()

    if len(results) == 0:
        querry = f"INSERT INTO kullanicilar VALUES('{isim}', '{email}', '{sifre}')"
        cursor.execute(querry)
        db.commit()
        return render_template('index.html')
    else:
        return render_template('kaydol.html', hata = "Bu kullanıcı zaten kayıtlı.")

@app.route("/girisbilgileri", methods=["POST"])
def giris_kontrol():
    isim = request.form["isim"]
    sifre = request.form["sifre"]

    db = sqlite3.connect("database.db")
    querry = f"SELECT * FROM admin WHERE username = '{isim}' AND password = '{sifre}'"
    cursor = db.cursor()
    cursor.execute(querry)
    results = cursor.fetchall() 

    if len(results) == 0:
        return render_template("giris_yap.html", hata = "Kullanıcı bilgileri hatalı!")
    else:
        session["isim"] = isim
        session["sifre"] = sifre
        return redirect("/")

@app.route("/personel")
def personel():

    if "isim" in session and session["isim"] != None:
        db = sqlite3.connect("database.db")
            
        querry = "SELECT * FROM personel"
        cursor = db.cursor()
        cursor.execute(querry)
        results = cursor.fetchall()
        print(results)
        db.commit()
        db.close()
        return render_template("personel.html", personel=results)
    else:
        return redirect("/giris")

@app.route("/personel/dok")
def personel_dok():
    if "isim" in session and session["isim"] != None:
        db = sqlite3.connect("database.db")
            
        querry = "SELECT * FROM personel"
        cursor = db.cursor()
        cursor.execute(querry)
        results = cursor.fetchall()
        print(results)
        db.commit()
        db.close()
        return render_template("personel_liste.html", personel=results)
    else:
        return redirect("/giris")

@app.route("/personel/sil/<personelid>")
def personel_sil(personelid):

    if "isim" in session and session["isim"] != None:
        db = sqlite3.connect("database.db")  
        querry = f"DELETE FROM personel WHERE id={int(personelid)}"
        cursor = db.cursor()
        cursor.execute(querry)
        db.commit()
        db.close()
        return redirect("/personel")
    else:
        return redirect("/giris")

@app.route("/personel/guncelle/<personelid>")
def personel_guncelle(personelid):
    if "isim" in session and session["isim"] != None:
        db = sqlite3.connect("database.db")
            
        querry = f"SELECT * FROM personel WHERE id = {int(personelid)}"
        cursor = db.cursor()
        cursor.execute(querry)
        kayit = cursor.fetchone()
        db.close()
        return render_template("personel_guncelle.html", personel=kayit)
    else:
        return redirect("/giris")

@app.route("/personel/guncelle", methods=["POST"])
def personel_kaydet():
    if "isim" in session and session["isim"] != None:
        id = request.form["id"]
        personel_isim = request.form["personel-isim"]
        personel_soyisim = request.form["personel-soyisim"]
        personel_gorev = request.form["personel-gorev"]
        personel_ise_baslangic = request.form["personel-ise-baslangic"]
        personel_saatlik_yevmiye = request.form["personel-saatlik-yevmiye"]

        db = sqlite3.connect("database.db")
        querry = f"UPDATE personel SET personel_isim='{personel_isim}', personel_soyisim='{personel_soyisim}', personel_gorev='{personel_gorev}', personel_ise_baslangic='{personel_ise_baslangic}', personel_saatlik_yevmiye='{personel_saatlik_yevmiye}' WHERE id = {int(id)}"
        cursor = db.cursor()
        cursor.execute(querry)
        kayit = cursor.fetchone()
        db.commit()
        db.close()
        return redirect("/personel")
    else:
        return redirect("/giris")

@app.route("/personel/ekle", methods=['GET', 'POST'])
def personel_ekle():
    if "isim" in session and session["isim"] != None:

        if request.method == "POST":
            ad = request.form["ad"]
            soyad = request.form["soyad"]
            gorev = request.form["gorev"]
            tarih = request.form["tarih"]
            saatlik = request.form["saatlik"]

            db = sqlite3.connect("database.db")
            cursor = db.cursor()

            try:
                querry = f"INSERT INTO personel (personel_isim, personel_soyisim, personel_gorev, personel_ise_baslangic, personel_saatlik_yevmiye) VALUES ('{ad}', '{soyad}', '{gorev}', '{tarih}', '{saatlik}')"
                cursor.execute(querry)
                db.commit()
                db.close()
                return redirect("/personel")
            except sqlite3.IntegrityError:
                db.rollback()
                db.close()
                return render_template("personel_ekle.html", hata="Bu personel zaten kayıtlı.")
        else:
            return render_template("personel_ekle.html")
    else:
        return redirect("/giris")

@app.route("/personel/arama", methods=["POST"])
def personel_arama():
    if "isim" in session and session["isim"] != None:
        arama_metni = request.form.get("arama")
        db = sqlite3.connect("database.db")
        querry = f"SELECT * FROM personel WHERE personel_isim LIKE '%{arama_metni}%'"
        cursor = db.cursor()
        cursor.execute(querry)
        personel = cursor.fetchall()
        db.close()
        return render_template("personel.html", personel=personel)
    else:
        return redirect("/giris")

@app.route("/bordro/arama", methods=["POST"])
def bordro_arama():
    if "isim" in session and session["isim"] != None:
        arama_metni = request.form.get("arama")
        db = sqlite3.connect("database.db")
        querry = f"SELECT * FROM personel WHERE personel_isim LIKE '%{arama_metni}%'"
        cursor = db.cursor()
        cursor.execute(querry)
        personel = cursor.fetchall()
        db.close()
        return render_template("bordro.html", personel=personel)
    else:
        return redirect("/giris")

@app.route("/bordro")
def bordro():

    if "isim" in session and session["isim"] != None:
        db = sqlite3.connect("database.db")
            
        querry = "SELECT * FROM personel"
        cursor = db.cursor()
        cursor.execute(querry)
        results = cursor.fetchall()
        print(results)
        db.commit()
        db.close()
        return render_template("bordro.html", personel=results)
    else:
        return redirect("/giris")


@app.route("/bordro/dok/<personelid>")
def bordro_dok(personelid):
    if "isim" in session and session["isim"] != None:
        db = sqlite3.connect("database.db")
            
        querry = f"SELECT * FROM personel WHERE id = {int(personelid)}"
        cursor = db.cursor()
        cursor.execute(querry)
        kayit = cursor.fetchone()
        db.close()
        gunluk = int(kayit[5])*8
        aylik = int(kayit[5])*30*8
        sgk_kesintisi = round(aylik*0.14, 2)
        issizlik_kesintisi = round(aylik*0.01, 2)
        toplam_sgk_kesintisi=sgk_kesintisi+issizlik_kesintisi
        gelir_vergisi_istisnasi=(2550.32)
        gelir_vergisi_matrahi = round(aylik*0.85, 2)
        normal_gelir_vergisi=round(gelir_vergisi_matrahi*0.15, 2)
        gelir_vergisi = round((gelir_vergisi_matrahi*0.15)-2550.32, 2)
        damga_vergisi_istisnasi=20002.5
        damga_vergisi_matrahi= round(aylik - 20002.5, 2)
        normal_damga_vergisi=round(aylik*0.00759, 2)
        damga_vergisi= round(damga_vergisi_matrahi* 0.00759, 2)
        net=round(aylik-sgk_kesintisi-issizlik_kesintisi-gelir_vergisi-damga_vergisi, 2)
        toplam_kesinti=round(aylik-net, 2)
        listelenmis=list(kayit)
        listelenmis.append(gunluk)
        listelenmis.append(aylik)
        listelenmis.append(sgk_kesintisi)
        listelenmis.append(issizlik_kesintisi)
        listelenmis.append(toplam_sgk_kesintisi)
        listelenmis.append(gelir_vergisi_istisnasi)
        listelenmis.append(gelir_vergisi_matrahi)
        listelenmis.append(gelir_vergisi)
        listelenmis.append(damga_vergisi_istisnasi)
        listelenmis.append(damga_vergisi_matrahi)
        listelenmis.append(damga_vergisi)
        listelenmis.append(net)
        listelenmis.append(toplam_kesinti)
        listelenmis.append(normal_gelir_vergisi)
        listelenmis.append(normal_damga_vergisi)
        kayit=tuple(listelenmis)
        print(kayit)
        return render_template("bordro_dok.html", personel=kayit)
    else:
        return redirect("/giris")


@app.route("/puantaj/arama", methods=["POST"])
def puantaj_arama():
    if "isim" in session and session["isim"] != None:
        arama_metni = request.form.get("arama")
        db = sqlite3.connect("database.db")
        querry = f"SELECT * FROM personel WHERE personel_isim LIKE '%{arama_metni}%'"
        cursor = db.cursor()
        cursor.execute(querry)
        personel = cursor.fetchall()
        db.close()
        return render_template("puantaj.html", personel=personel)
    else:
        return redirect("/giris")
    
@app.route("/puantaj")
def puantaj():

    if "isim" in session and session["isim"] != None:
        db = sqlite3.connect("database.db")
            
        querry = "SELECT * FROM personel"
        cursor = db.cursor()
        cursor.execute(querry)
        results = cursor.fetchall()
        print(results)
        db.commit()
        db.close()
        return render_template("puantaj.html", personel=results)
    else:
        return redirect("/giris")

@app.route("/puantaj/goruntule/<personelid>")
def puantaj_goruntule(personelid):
    if "isim" in session and session["isim"] is not None:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()

        query = "SELECT * FROM giris_cikislar WHERE giris_cikislar_kullanici_id = ?"
        cursor.execute(query, (personelid,))
        results = cursor.fetchall()

        sorgu = "SELECT personel_isim, personel_soyisim FROM personel WHERE id = ?"
        cursor.execute(sorgu, (personelid,))
        sonuc = cursor.fetchone()
        name_surname = f"{sonuc[0]} {sonuc[1]}"

        # results listesindeki her öğeye name_surname ekle
        updated_results = [result + (name_surname,) for result in results]

        db.close()
        return render_template("sahis_puantaj.html", personel=updated_results)
    else:
        return redirect("/giris")


@app.route("/puantaj/olustur/<personelid>", methods=['GET', 'POST'])
def puantaj_olustur(personelid):
    if "isim" in session and session["isim"] is not None:
        if request.method == 'POST':
            tarih = request.form.get("ekle")
            db = sqlite3.connect("database.db")
            query = "INSERT INTO giris_cikislar (giris_cikislar_kullanici_id, giris_cikislar_tarih) VALUES (?, ?)"
            cursor = db.cursor()
            cursor.execute(query, (personelid, tarih))
            db.commit()
            cursor.close()
            db.close()
            hata = None
        else:
            hata = None

        # Personel bilgilerini veritabanından çekmek için bir sorgu
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM personel WHERE id = ?", (personelid,))
        personel = cursor.fetchone()
        cursor.close()
        db.close()

        return render_template("puantaj_duzenle.html", personel=personel, hata=hata)
    else:
        return redirect("/giris")


app.run(debug=True)