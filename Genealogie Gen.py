#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sqlite3

namendatenbank = sqlite3.connect("namen.db")
namenzeiger = namendatenbank.cursor()
personendatenbank = sqlite3.connect("personen.db")
personenzeiger = personendatenbank.cursor()

startjahr = -500
endjahr = 0
max_erbfolge = 7 #Wenn man weiter vom Familienkern entfernt ist, werden keine Kinder mehr generiert
fruchtbar = [18,60] #In welcher Altersspanne kann man Kinder bekommen
hauptfamilien = ["von Möwenburg","von Tiefenfels","von Eichenwald","von Bergetal","von Kisatris"]
namenskuerzel = {"von Möwenburg":"MB","von Tiefenfels":"TF","von Eichenwald":"EW","von Bergetal":"BT","von Kisatris":"KS","von der Münze":"MU"}
herkunftmoeglich = ["KS","TF","EW","MB","BT","MU"]


# def neuenamen(mfd,namestring):
#     neu = namestring.replace("/", ", ")
#     neuliste = neu.split(", ")
#     for name in neuliste:
#         if mfd == "m" and not name in male: male.append(name)
#         if mfd == "f" and not name in female: female.append(name)
#         if mfd == "d" and not name in divers: divers.append(name)
#     if mfd == "m": print(mfd,male)
#     if mfd == "f": print(mfd,female)
#     if mfd == "d": print(mfd,divers)

#neu = "Marie/Maria, Elisabeth/Else, Anna, Margarete, Helene, Gertrud, Luise/Louise, Hedwig, Auguste, Johanna, Sophie, Charlotte, Clara, Mathilde, Emma, Martha, Ida, Bertha, Frieda, Julie, Käthe"
#neuenamen("f", neu)

class color: #um farbig zu printen
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def geburt(geschlecht=None,jahr=None,todesjahr=None,vater=None,mutter=None,herkunft=None):
    if geschlecht == None: geschlecht = random.choice(["male","female"])

    if vater != None:
        personenzeiger.execute("SELECT * from personen WHERE uuid = ?;",(vater,))
        vater_person = personenzeiger.fetchall()[0]
    if mutter != None:
        personenzeiger.execute("SELECT * from personen WHERE uuid = ?;",(mutter,))
        mutter_person = personenzeiger.fetchall()[0]
       
    #-Nachname
    namenzeiger.execute("SELECT * FROM surname")
    nachnamensliste = namenzeiger.fetchall()
    nachname = random.choice(nachnamensliste)[0]
    
    #Nachnamen von Hauptfamilien bleiben
    if vater != None and mutter != None and vater_person[9] != None and mutter_person[9] != None:
        if vater_person[9] < mutter_person[9]: #wenn Vater näher in Erbfolge ist
            nachname = vater_person[2]
        elif vater_person[9] > mutter_person[9]: #wenn Mutter näher in Erbfolge ist
            nachname = mutter_person[2]
        else:
            if random.randint(0,1) == 1: nachname = vater_person[2]
            else: nachname = mutter_person[2]
    elif mutter != None and mutter_person[2] in hauptfamilien: nachname = mutter_person[2]
    elif vater != None and vater_person[2] in hauptfamilien: nachname = vater_person[2]
    #Beide Eltern haben keinen Erbfolgeplatz, sind aber definiert. Dann bekommt Kind den Namen des Nichtadeligen Elternteils
    if vater != None and mutter != None and vater_person[9] == None and mutter_person[9] == None: 
        if vater_person[6] == None and mutter_person[6] != None: nachname = vater_person[2]
        elif mutter_person[6] == None and vater_person[6] != None: nachname = mutter_person[2]
        else:
            if random.randint(0,1) == 1: nachname = vater_person[2]
            else: nachname = mutter_person[2]       

    #Herkunft bestimmen
    if nachname in hauptfamilien: herkunft = namenskuerzel[nachname]
    else: herkunft = random.choice(herkunftmoeglich)

    #-Vorname
    namenzeiger.execute("SELECT * FROM "+geschlecht+" WHERE vorkommen LIKE '%"+herkunft+"%'")
    namensliste = namenzeiger.fetchall()
    vorname = ""
    #Zumeist einen Vornamen von Eltern übernehmen
    if vater != None and mutter != None: #Zumeist einen Vornamen von Eltern übernehmen
        if random.randint(1,20) >= 2:
            if geschlecht == "male" and vater_person[3] == "m":
                vorname = random.choice(vater_person[1].split(" ")) + " "
            elif geschlecht == "female" and mutter_person[3] == "w":
                vorname = random.choice(mutter_person[1].split(" ")) + " "
            #print(">>>>>NAMEN ÜBERNEHMEN: ", vorname)
            
    namenszahl = min(random.randint(1,3),random.randint(1,3)) + min(random.randint(0,2),random.randint(0,2))
    for i in range(namenszahl):
        neuername = random.choice(namensliste)[0]
        if not neuername in vorname:
            vorname += neuername
            if not i == namenszahl-1: vorname += " "
    if vorname[-1] == " ": vorname=vorname[:-1]
    
    if vorname[0] == " ":
        print(color.RED,"ACHTUNG! Vorname beginnt mit Lehrzeichen", color.END)
        print(vorname)
        print(vater_person[1].split(" "))
        print(mutter_person[1].split(" "))

    #Todesjahr bestimmen
    if jahr != None and todesjahr == None: todesjahr = jahr + min(random.randint(0,110),random.randint(0,110),random.randint(0,110)) + min(random.randint(0,10),random.randint(0,10))
    
    #Erbfolgenplatz bestimmen
    erbfolge = None
    if vater != None:
        if nachname == vater_person[2]:
            #print("vater: ",vater)
            personenzeiger.execute("SELECT COUNT(*) FROM personen WHERE vater = ? AND nachname = ?",(vater,vater_person[2])) #Zähle Geschwister mit gleichem Nachnamen
            kinder_vater = personenzeiger.fetchone()[0]
            #print("kinder_vater: ",kinder_vater)
            personenzeiger.execute("SELECT erbfolge FROM personen WHERE uuid = ?",(vater,))
            erbfolge_vater = personenzeiger.fetchone()[0]
            #print("erbfolge_vater: ",erbfolge_vater)
            if erbfolge_vater == None: erbfolge = None
            else: erbfolge = erbfolge_vater + kinder_vater + 1
            #print("erbfolge: ", erbfolge)
    if mutter != None:
        if nachname == mutter_person[2]:
            #print("mutter: ",mutter)
            personenzeiger.execute("SELECT COUNT(*) FROM personen WHERE mutter = ? AND nachname = ?",(mutter,mutter_person[2])) #Zähle Geschwister mit gleichem Nachnamen
            kinder_mutter = personenzeiger.fetchone()[0]
            #print("kinder_mutter: ",kinder_mutter)
            personenzeiger.execute("SELECT erbfolge FROM personen WHERE uuid = ?",(mutter,))
            erbfolge_mutter = personenzeiger.fetchone()[0]
            #print("erbfolge_mutter: ", erbfolge_mutter)
            if erbfolge_mutter == None: erbfolge = None
            else: erbfolge = erbfolge_mutter + kinder_mutter + 1
            #print("erbfolge: ", erbfolge)
#     if erbfolge != None and erbfolge >= max_erbfolge:
#         erbfolge = None
    
    geschlecht = geschlecht[0] #nur den ersten Buchstaben des Strings
    personenzeiger.execute("INSERT INTO personen VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(None,vorname,nachname,geschlecht,jahr,todesjahr,vater,mutter,None,erbfolge,0,"",herkunft))
    personendatenbank.commit()
    personenzeiger.execute("SELECT * from personen WHERE uuid = (SELECT MAX(uuid) FROM personen);")
    person = personenzeiger.fetchall()[0]
    return(person)


def parship(person,personen):
    partner = None
    if person[8] != None: #bleibender partner
        if random.randint(1,12) >= 2:
            personenzeiger.execute("SELECT * from personen WHERE uuid = ?;",(person[8],))
            partner = personenzeiger.fetchall()[0]
            partner_alter = aktuelles_jahr - partner[4]
            if partner_alter >= fruchtbar[0] and partner_alter <= fruchtbar[1]:
                return(partner)
            else: return(None)
    
    if random.randint(1,10) >= 6: #Partner aus Hauptfamilie
        partner = random.choice(personen)
        if partner != person:
            partner_alter = aktuelles_jahr - partner[4]
            if partner_alter >= fruchtbar[0] and partner_alter <= fruchtbar[1]: #Partner muss im fruchtbaren Alter #//and partner[3] != person[3] und von einem anderem Geschlecht sein
                return(partner)
    
    #Nur einmal pro Jahr Kinder bekommen
    if person[0] in hat_gebaert: return(None)
    if person[3] == "f": hat_gebaert.append(person[0])
    if partner != None:
        if partner[0] in hat_gebaert: return(None)
        if partner[3] == "f": hat_gebaert.append(partner[0])
            
    #neuer Partner
    alter = aktuelles_jahr - person[4]
    #Partner muss ähnliches Alter haben, muss fruchtbares Alter haben und darf nicht schon vorher gestorben sein
    partner_alter = alter + random.randint(-5,0)+ random.randint(-3,20)
    if partner_alter < fruchtbar[0]: partner_alter = fruchtbar[0]
    elif partner_alter > fruchtbar[1]: partner_alter = fruchtbar[1]
    partner_geburtsjahr = aktuelles_jahr - alter
    partner_todesjahr = partner_geburtsjahr + min(random.randint(0,120),random.randint(0,120),random.randint(0,120))
    if partner_todesjahr < aktuelles_jahr: partner_todesjahr = aktuelles_jahr #Keine Nekrophilie hier!
    if person[3] == "m": partner  = geburt(geschlecht="female",jahr=partner_geburtsjahr,todesjahr=partner_todesjahr)
    elif person[3] == "f": partner  = geburt(geschlecht="male",jahr=partner_geburtsjahr,todesjahr=partner_todesjahr)
    else: raise ValueError("Elter hat kein akzeptiertes Geschlecht.")
    #print(partner,partner[0][0])
    #print(person,person[0][0])
    #personenzeiger.execute("UPDATE personen SET letzter_partner = ? WHERE uuid = ?",(partner[0],person[0],))
    #personenzeiger.execute("UPDATE personen SET letzter_partner = ? WHERE uuid = ?",(person[0],partner[0],))
    #personendatenbank.commit()
    return(partner)

def kinderchance(hauptp,nebenp,aktuelles_jahr):
    ok = [False,False]
    alterhp = aktuelles_jahr - hauptp[4]
    alternp = aktuelles_jahr - nebenp[4]
    if hauptp[3] == "m":
        if random.randint(100,300) - alterhp*2 >= 100: ok[0] = True
    elif hauptp[3] == "f":
        if random.randint(125,205) - alterhp*2 >= 100: ok[0] = True
    if nebenp[3] == "m":
        if random.randint(100,300) - alternp*2 >= 100: ok[1] = True
    elif nebenp[3] == "f":
        if random.randint(125,205) - alternp*2 >= 100: ok[1] = True
    if hauptp[3] == nebenp[3] and ok[0]: return True #Bei Gleichgeschlechtlich ist nur Hauptpartner relevant
    elif ok[0] and ok[1]: return True
    else: return False #keine Kinder


#Hier beginnt der Durchgang!

aktuelles_jahr = startjahr
while aktuelles_jahr <= endjahr:
    print(color.BOLD,"Jahr: ",aktuelles_jahr,color.END)
    hat_gebaert = []
    personen_familie = {}
    lebendige_hauptfamilien = 0
    for familie in hauptfamilien:
        #print(familie)
        personen_familie[familie] = []
        personenzeiger.execute("SELECT * FROM personen WHERE nachname = ? AND geburtsjahr <= ? AND todesjahr >= ?",(familie,aktuelles_jahr,aktuelles_jahr))
        lebendige_familienmitglieder = personenzeiger.fetchall()
        #print(">>lebendige_familienmitglieder: ",lebendige_familienmitglieder)
        
        personenzeiger.execute("SELECT MIN(erbfolge) FROM personen WHERE geburtsjahr < ? AND todesjahr >= ? AND nachname = ?",(aktuelles_jahr,aktuelles_jahr,familie))
        min_erbfolge = personenzeiger.fetchone()[0]
        if min_erbfolge == None: min_erbfolge = 100
        personenzeiger.execute("SELECT * FROM personen WHERE geburtsjahr < ? AND todesjahr >= ? AND nachname = ?",(aktuelles_jahr,aktuelles_jahr,familie))
        personen_familie[familie] = personenzeiger.fetchall()
            
        #Unklare Erbfolge klären
        if min_erbfolge > 0:
            print("Erbfolgeproblem bei ",familie)
            print("min_erbfolge: ",min_erbfolge)
            personenzeiger.execute("SELECT uuid FROM personen WHERE nachname = ? AND geburtsjahr <= ? AND todesjahr >= ? AND erbfolge = ?",(familie,aktuelles_jahr,aktuelles_jahr,min_erbfolge))
            berechtigste_personen = personenzeiger.fetchall()
            #print(len(personen),personen)
            print(len(personen_familie[familie]), personen_familie[familie])
            print("berechtigste_personen: ",berechtigste_personen)
            if len(berechtigste_personen) != 0:
                berechtigste_person = random.choice(berechtigste_personen)[0] #wählt eine zufällige Person mit entsprechender Erbberechtigung aus
                personenzeiger.execute("SELECT erbfolge FROM personen WHERE uuid = ?",(berechtigste_person,))
                alte_erbfolge = personenzeiger.fetchone()[0]
                if alte_erbfolge != min_erbfolge: raise ValueError("Ungültige Person bei Erbfolgeproblem gewählt")
                if alte_erbfolge >= max_erbfolge: print(color.RED,"ACHTUNG!", color.END)
                print(berechtigste_person, " steigt in der Erbfolge auf um ", alte_erbfolge)
                personenzeiger.execute("UPDATE personen SET erbfolge = 0 WHERE uuid = ?",(berechtigste_person,))
                personendatenbank.commit()
                personenzeiger.execute("SELECT uuid FROM personen WHERE (vater = ? OR mutter = ?) AND nachname = ?",(berechtigste_person,berechtigste_person,familie))
                erben_des_erben = personenzeiger.fetchall()
                for erbe in erben_des_erben:
                    personenzeiger.execute("UPDATE personen SET erbfolge = erbfolge - ? WHERE uuid = ?",(alte_erbfolge,erbe[0],)) #Erbberechtigung von Erben des Erben werden angepasst
            else:
                print(color.RED,"Familie " + familie + " stirbt aus.",color.END)
                hauptfamilien.pop(hauptfamilien.index(familie))
                
            
        if len(personen_familie[familie]) > 0: lebendige_hauptfamilien += 1
    
    personenzeiger.execute("SELECT * FROM personen WHERE geburtsjahr < ? AND todesjahr >= ? AND erbfolge < ?",(aktuelles_jahr,aktuelles_jahr,max_erbfolge))
    personen = personenzeiger.fetchall()
    personenzeiger.execute("SELECT COUNT(*) FROM personen")
    personenzahl = personenzeiger.fetchone()[0]
    print(">>>Lebendige relevante Hauptfamilienmitglieder: ", len(personen), ", lebendige_hauptfamilien: ", lebendige_hauptfamilien, ", Personen gesamt: ", personenzahl)
    
    for person in personen: #bekommen Personen Kinder?
        if person[9] == None or person[9] >= max_erbfolge: continue #wer zu weit von Erbfolge entfernt ist, wird ignoriert
        #print("person: ",person)
        alter = aktuelles_jahr - person[4]
        #print(alter)
        if alter >= fruchtbar[0] and alter <= fruchtbar[1]: #Wenn im fruchtbaren Alter
            kinderzahl = person[10]
            if random.randint(1,10) >= 5+(kinderzahl/1.5): #Wahrscheinlichkeit eines Kinderwunsches
                #print("XXX BABY XXX")
                partner = parship(person,personen)
                if partner != None:
                    kind = None
                    #print("PERSON: ",person)
                    #print("PARTNER: ",partner)
                    if person[3] == partner[3]: #Partner haben gleiches geschlecht
                        #print("Gleichgeschlechtlich: ",person[0],partner[0])
                        if person[9] == None: person_erbfolge = 100
                        else: person_erbfolge = person[9]
                        if partner[9] == None: partner_erbfolge = 100
                        else: partner_erbfolge = partner[9]
                        if person_erbfolge < partner_erbfolge: #wenn Person näher in Erbfolge ist
                            hauptpartner = person
                            nebenpartner = partner
                        elif person_erbfolge > partner_erbfolge: #wenn Partner näher in Erbfolge ist
                            hauptpartner = partner
                            nebenpartner = person
                        else: #beide sind gleich Erbberechtigt, also entscheidet Zufall
                            if random.randint(0,1) == 1:
                                hauptpartner = partner
                                nebenpartner = person
                            else:
                                hauptpartner = person
                                nebenpartner = partner                                
                        if hauptpartner[3]=="m":
                            if kinderchance(hauptpartner,nebenpartner,aktuelles_jahr): kind = geburt(geschlecht=None,jahr=aktuelles_jahr,vater=hauptpartner[0],mutter=nebenpartner[0])
                        elif hauptpartner[3]=="f":
                            if kinderchance(hauptpartner,nebenpartner,aktuelles_jahr): kind = geburt(geschlecht=None,jahr=aktuelles_jahr,vater=nebenpartner[0],mutter=hauptpartner[0])
                        else: raise ValueError("Elter hat kein akzeptiertes Geschlecht.")
                    #Partner haben unterschiedliches Geschlecht
                    if person[3]=="m":
                        if kinderchance(person,partner,aktuelles_jahr): kind = geburt(geschlecht=None,jahr=aktuelles_jahr,vater=person[0],mutter=partner[0])
                    elif person[3]=="f":
                        if kinderchance(person,partner,aktuelles_jahr): kind = geburt(geschlecht=None,jahr=aktuelles_jahr,vater=partner[0],mutter=person[0])
                    else: raise ValueError("Elter hat kein akzeptiertes Geschlecht.")
                    if kind != None:
                        personenzeiger.execute("UPDATE personen SET kinderzahl = kinderzahl + 1 WHERE uuid IN (?,?)",(person[0],partner[0],))
                        personenzeiger.execute("UPDATE personen SET kinder = kinder || ? || ',' WHERE uuid IN (?,?)",(kind[0],person[0],partner[0],))
                        personenzeiger.execute("UPDATE personen SET letzter_partner = ? WHERE uuid = ?",(partner[0],person[0],))
                        personenzeiger.execute("UPDATE personen SET letzter_partner = ? WHERE uuid = ?",(person[0],partner[0],))
                        personendatenbank.commit()
                    #print("KIND: ",kind)
                    
    aktuelles_jahr += 1
    
# namendatenbank.commit()
namendatenbank.close()
# personendatenbank.commit()
personendatenbank.close()