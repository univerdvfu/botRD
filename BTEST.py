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

# c.execute('INSERT INTO info VALUES("Допольнительне баллы зв достижения","Спортивные достижения, олимпиады и документ об образовании с отличием могут увеличить твой шанс на поступление 🔥 Смотри на пикче, за какие индивидуальные достижения дают дополнительные быллы❗️Максимальное количество — 10 баллов. Суммируй различные достижения [например, значок ГТО и статус призера олимпиады], либо приложи к документам аттестат или диплом о СПО с отличием/удостоверение мастера спорта или мастера спорта международного класса","1","img/photo_2023-04-05_12-31-01.jpg")')
# c.execute('INSERT INTO infoCampus VALUES("Дорогое такси?","Не дороже личного верблюда","0","")')
c.execute('UPDATE infoCampus SET URL_img = "img/IMG_7755-3.jpg" WHERE name_ID = "Есть ли кто-то кроме лисов на кампусе"')
c.execute(' SELECT * FROM infoCampus ')

print( c.fetchall())

db.commit()
db.close()