#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
dateiname = "Stammbaum5.ged"
datei = open(dateiname, "a")

personendatenbank = sqlite3.connect("personen.db")
personenzeiger = personendatenbank.cursor()

personenzeiger.execute("SELECT * FROM personen")
personen = personenzeiger.fetchall()

datei.write("0 HEAD")
datei.write("\n 1 CHAR UTF-8")

datei.close()
famcount = 1

for person in personen:
    datei = open(dateiname, "a")
    print(person[0])
    datei.write("\n\n0 @I"+str(person[0])+"@ INDI")
    datei.write("\n 1 NAME "+person[1]+" /"+person[2]+"/")
    datei.write("\n 1 SEX "+person[3].upper())
    datei.write("\n 1 BIRT")
    datei.write("\n 2 DATE "+str(person[4]))
    datei.write("\n 1 DEAT")
    datei.write("\n 2 DATE "+str(person[5]))
    
    personenzeiger.execute("SELECT * FROM personen WHERE vater = ?",(person[0],))
    kinder_vater = personenzeiger.fetchall()
    for kind in kinder_vater:
        datei.write("\n 1 FAMS @F"+str(kind[0])+"@")
    personenzeiger.execute("SELECT * FROM personen WHERE mutter = ?",(person[0],))
    kinder_mutter = personenzeiger.fetchall()
    for kind in kinder_mutter:
        datei.write("\n 1 FAMS @F"+str(kind[0])+"@")        
    
    if person[6] != None or person[7] != None:
        datei.write("\n 1 FAMC @F"+str(famcount)+"@")
    
        datei.write("\n\n0 @F"+str(person[0])+"@ FAM")
        if person[6] != None: datei.write("\n 1 HUSB @I"+str(person[6])+"@")
        if person[7] != None: datei.write("\n 1 WIFE @I"+str(person[7])+"@")
        datei.write("\n 1 MARR")
        datei.write("\n 1 CHIL @I"+str(person[0])+"@")
        
        famcount +=1
    datei.close()

datei = open(dateiname, "a")
datei.write("\n\n0 TRLR")

personendatenbank.commit()
personendatenbank.close()
datei.close()
print("DONE")
