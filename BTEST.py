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
c.execute('INSERT INTO info VALUES("Какие документы нужны","Для подачи нужно: Аттестал/Диплом с приложением, СНИЛС, ПАСПОРТ, ЗАЯВЛЕНИЕ и СОГЛАСИЕ ОПД","0","")')
# c.execute('INSERT INTO info VALUES("dat23eI","Реально жить можно","")')
c.execute('SELECT * FROM info')
print(c.fetchall())
db.commit()
db.close()