#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
dateiname = "stammbuchAllg.txt"
datei = open(dateiname, "w")

personendatenbank = sqlite3.connect("personen.db")
personenzeiger = personendatenbank.cursor()

personenzeiger.execute("SELECT * FROM personen")
personen = personenzeiger.fetchall()

hauptfamilien = ["von Möwenburg","von Tiefenfels","von Eichenwald","von Bergetal","von Kisatris"]

titelfamilie = "von Möwenburg"
startjahr = -500
endjahr = 0

datei.write("Dies ist die Genealogie der hohen Familien, eine Nennung ihrer Söhne und Töchter.\n")
datei.write("Aufgezeichnet im Namen der edlen Familie "+titelfamilie+"\n")
datei.close()

aktuelles_jahr = startjahr
while aktuelles_jahr <= endjahr:
    datei = open(dateiname, "a")
    print(">>>JAHR: ",aktuelles_jahr)
    personenzeiger.execute("SELECT *, min(todesjahr) FROM personen WHERE geburtsjahr <= ? AND todesjahr >= ? AND erbfolge = 0 AND nachname = ?",(aktuelles_jahr,aktuelles_jahr,titelfamilie))
    zeitrechnungsperson = personenzeiger.fetchone()
#     print("zeitrechnungsperson: ",zeitrechnungsperson)
    if zeitrechnungsperson[6] == None and zeitrechnungsperson[7] == None:
        herrschaftsjahr = aktuelles_jahr - startjahr + 1
    else:
        personenzeiger.execute("SELECT *, max(todesjahr) FROM personen WHERE nachname = ? AND todesjahr < ? AND todesjahr >= ? AND erbfolge = 0",(zeitrechnungsperson[2],zeitrechnungsperson[5],zeitrechnungsperson[4],))
        vorherige_thronperson = personenzeiger.fetchone()
#         print("vorherige_thronperson: ",vorherige_thronperson)
        herrschaftsjahr = aktuelles_jahr - vorherige_thronperson[5]
#     print("Herrschaftsjahr: ",herrschaftsjahr)
    geborene_personen = []
    geborene_personen_familie = {}
    gestorbene_personen = []
    gestorbene_personen_familie = {}
    for familie in hauptfamilien:
        #geboren
        geborene_personen_familie[familie] = []
        personenzeiger.execute("SELECT * FROM personen WHERE geburtsjahr == ? AND nachname = ?",(aktuelles_jahr,familie))
        geborene_familienmitglieder = personenzeiger.fetchall()
        for familienmitglied in geborene_familienmitglieder:
            if familienmitglied == []: continue
            #print(familienmitglied,familienmitglied[9])
            geborene_personen.append(familienmitglied)
            geborene_personen_familie[familie].append(familienmitglied)
        #gestorben
        gestorbene_personen_familie[familie] = []
        personenzeiger.execute("SELECT * FROM personen WHERE todesjahr == ? AND nachname = ?",(aktuelles_jahr,familie))
        gestorbene_familienmitglieder = personenzeiger.fetchall()
        for familienmitglied in gestorbene_familienmitglieder:
            if familienmitglied == []: continue
            #print(familienmitglied,familienmitglied[9])
            gestorbene_personen.append(familienmitglied)
            gestorbene_personen_familie[familie].append(familienmitglied)
#     print("Geboren: ",geborene_personen)
#     print("Gestorben: ",gestorbene_personen)
    
    if len(geborene_personen) != 0 or len(gestorbene_personen) != 0:
        datei.write("\n\nEs war das "+str(herrschaftsjahr)+". Jahr der Herrschaft von "+zeitrechnungsperson[1]+" "+zeitrechnungsperson[2]+". ")
        if len(geborene_personen) != 0: datei.write("\n")
        for person in geborene_personen:
            personenzeiger.execute("SELECT * FROM personen WHERE uuid = ?",(person[6],))
            vater = personenzeiger.fetchone()
            print(vater)
            personenzeiger.execute("SELECT * FROM personen WHERE uuid = ?",(person[7],))
            mutter = personenzeiger.fetchone()
            datei.write(person[1]+" "+person[2]+" wurde geboren als Kind von "+vater[1]+" "+vater[2]+" und "+mutter[1]+" "+mutter[2]+". ")
        if len(gestorbene_personen) != 0:
            datei.write("\n")
            if len(gestorbene_personen) == 1:
                datei.write("Es starb " + gestorbene_personen[0][1]+" "+gestorbene_personen[0][2]+". ")
            elif len(gestorbene_personen) >= 1:
                datei.write("Es starben ")
                for person in gestorbene_personen:
                    datei.write(person[1]+" "+person[2])
                    if gestorbene_personen.index(person) <= len(gestorbene_personen)-3: datei.write(", ")
                    if gestorbene_personen.index(person) == len(gestorbene_personen)-2: datei.write(" und ")
                datei.write(". ")
            for person in gestorbene_personen:
                if person[9] == 0:
                    datei.write("\n")
                    personenzeiger.execute("SELECT *, min(todesjahr) FROM personen WHERE geburtsjahr <= ? AND todesjahr >= ? AND erbfolge = 0 AND nachname = ?",(aktuelles_jahr,aktuelles_jahr+1,person[2]))
                    thronfolger = personenzeiger.fetchone()
                    if thronfolger[3] == "m": datei.write(thronfolger[1]+" "+thronfolger[2]+" wurde das neue Oberhaupt seiner Familie. ")
                    if thronfolger[3] == "f": datei.write(thronfolger[1]+" "+thronfolger[2]+" wurde das neue Oberhaupt ihrer Familie. ")
            
    aktuelles_jahr += 1
    datei.close()

        
