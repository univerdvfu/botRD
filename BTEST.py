import sqlite3

db = sqlite3.connect('rdInfoForPK.db')

c = db.cursor()

# c.execute("""
# CREATE TABLE info(
# name_ID text,
# text_info text,
# flag BLOB,
# URL_img text
# )
# """
# )

# c.execute("""
# CREATE TABLE infoCampus(
# name_ID text,
# text_info text,
# flag BLOB,
# URL_img text
# )
# """
# )
# c.execute("""
# CREATE TABLE infoDirection(
# name_ID text,
# text_info text,
# flag BLOB,
# URL_img text
# )
# """
# )

c.execute("INSERT INTO infoDirection VALUES('Прикладная информатика в компьютерном дизайне','Научишься делать красивое: игры, оболочку мобильных и веб-приложений, а ещё анимации и 3D-модели для роликов и даже фильмов! И всё это благодаря полученным знаниям в области:\n -моделирования систем;\n-объектно-ориентированного анализа и проектирования;\n- математических основ компьютерной графики;\n - мультимедийных технологий;\n- 3D-прототипирования;\n- и других инструментов\n P.S.: фотошоп принимать в микродозах ','0','')")
# c.execute('INSERT INTO infoCampus VALUES("Дорогое такси?","Не дороже личного верблюда","0","")')
# c.execute('UPDATE infoCampus SET URL_img = "img/IMG_7755-3.jpg" WHERE name_ID = "Есть ли кто-то кроме лисов на кампусе"')
c.execute(' SELECT * FROM infoCampus ')
print(5//5)
print( len(c.fetchall()))

db.commit()
db.close()