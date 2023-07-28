#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

max_erbfolge = 6
startjahr = -500
endjahr = 0

personendatenbank = sqlite3.connect("personen.db")
personenzeiger = personendatenbank.cursor()

personenzeiger.execute("SELECT COUNT(*) from personen")
print("Gesamt: ",personenzeiger.fetchone())
personenzeiger.execute("SELECT COUNT(*) from personen WHERE erbfolge < ?",(max_erbfolge,))
print("Berücksichtigte: ",personenzeiger.fetchone())
personenzeiger.execute("SELECT COUNT(*) from personen WHERE letzter_partner IS NULL AND erbfolge < ?",(max_erbfolge,))
print("davon Kinderlose: ",personenzeiger.fetchone())
personenzeiger.execute("SELECT COUNT(*) from personen WHERE erbfolge < ? AND todesjahr - geburtsjahr >=18 ",(max_erbfolge,))
print("Berücksichtigte ü18: ",personenzeiger.fetchone())
personenzeiger.execute("SELECT COUNT(*) from personen WHERE letzter_partner IS NULL AND erbfolge < ? AND todesjahr - geburtsjahr >=18 ",(max_erbfolge,))
print("davon Kinderlose: ",personenzeiger.fetchone())

i = 0
while i <= 120:
    personenzeiger.execute("SELECT COUNT(*) from personen WHERE todesjahr - geburtsjahr >= ? AND erbfolge < ?",(i,max_erbfolge))
    print("davon erreichten Alter von ",i,personenzeiger.fetchone())
    i+=10

kinderzahl = []
personenzeiger.execute("SELECT * FROM personen WHERE erbfolge < ?",(max_erbfolge,))
alle_rel_personen = personenzeiger.fetchall()
for person in alle_rel_personen:
    personenzeiger.execute("SELECT COUNT(*) FROM personen WHERE vater = ? OR mutter = ?",(person[0],person[0]))
    kinderzahl.append(personenzeiger.fetchone()[0])
print("Durchschnittliche Kinderzahl: ", sum(kinderzahl)/len(kinderzahl))

lebendige_personen = []
lebendige_personen_rel = []
for jahr in range(startjahr,endjahr):
    personenzeiger.execute("SELECT COUNT(*) FROM personen WHERE geburtsjahr <= ? AND todesjahr > ? AND erbfolge < ?",(jahr,jahr,max_erbfolge))
    lebendige_personen_rel.append(personenzeiger.fetchone()[0])
    personenzeiger.execute("SELECT COUNT(*) FROM personen WHERE geburtsjahr <= ? AND todesjahr > ?",(jahr,jahr))
    lebendige_personen.append(personenzeiger.fetchone()[0])
print("Lebendige Personen pro Jahr: ",lebendige_personen)
print("Lebendige berücksichtigte Personen pro Jahr: ",lebendige_personen_rel)

datei = open('LPpJ.txt','w')
output = ""
for jahr in lebendige_personen: output += str(jahr) +"\n"
datei.write(output)
datei.close()

datei = open('LbPpJ.txt','w')
output = ""
for jahr in lebendige_personen_rel: output += str(jahr) +"\n"
datei.write(output)
datei.close()