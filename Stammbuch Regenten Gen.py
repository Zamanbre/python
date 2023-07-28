#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
dateiname = "stammbuch Regenten.txt"
datei = open(dateiname, "w")

personendatenbank = sqlite3.connect("personen.db")
personenzeiger = personendatenbank.cursor()

personenzeiger.execute("SELECT * FROM personen")
personen = personenzeiger.fetchall()

hauptfamilien = ["von Möwenburg","von Tiefenfels","von Eichenwald","von Bergetal","von Kisatris"]

startjahr = -500
endjahr = 0

aktuelles_jahr = startjahr

vorjahr_zeitrechnungsperson = {"von Möwenburg":[],"von Tiefenfels":[],"von Eichenwald":[],"von Bergetal":[],"von Kisatris":[]}
letzte_zeitrechnungsperson = {"von Möwenburg":[],"von Tiefenfels":[],"von Eichenwald":[],"von Bergetal":[],"von Kisatris":[]}

while aktuelles_jahr <= endjahr:
    datei = open(dateiname, "a")
    print(">>>JAHR: ",aktuelles_jahr)
    datei.write("\n "+str(aktuelles_jahr))
    for familie in hauptfamilien:
        personenzeiger.execute("SELECT *, min(todesjahr) FROM personen WHERE geburtsjahr <= ? AND todesjahr >= ? AND erbfolge = 0 AND nachname = ?",(aktuelles_jahr,aktuelles_jahr,familie))
        zeitrechnungsperson = personenzeiger.fetchone()
        if letzte_zeitrechnungsperson[familie] != vorjahr_zeitrechnungsperson[familie] and letzte_zeitrechnungsperson[familie] != zeitrechnungsperson: letzte_zeitrechnungsperson[familie] = vorjahr_zeitrechnungsperson[familie]
        vorjahr_zeitrechnungsperson[familie] = zeitrechnungsperson
        if zeitrechnungsperson[6] == None and zeitrechnungsperson[7] == None:
            herrschaftsjahr = aktuelles_jahr - startjahr + 1
        else:
            personenzeiger.execute("SELECT *, max(todesjahr) FROM personen WHERE nachname = ? AND todesjahr < ? AND todesjahr >= ? AND erbfolge = 0",(zeitrechnungsperson[2],zeitrechnungsperson[5],zeitrechnungsperson[4],))
            vorherige_thronperson = personenzeiger.fetchone()
            herrschaftsjahr = aktuelles_jahr - vorherige_thronperson[5]
            if herrschaftsjahr <= 0: print("FEHLER!!")
        datei.write("; "+zeitrechnungsperson[1]+" "+zeitrechnungsperson[2]+"; "+str(herrschaftsjahr))
#     print(letzte_zeitrechnungsperson)
        
    
    
    
    aktuelles_jahr += 1
    datei.close()