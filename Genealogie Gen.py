#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sqlite3

namendatenbank = sqlite3.connect("namen.db")
namenzeiger = namendatenbank.cursor()
personendatenbank = sqlite3.connect("personen.db")
personenzeiger = personendatenbank.cursor()

startjahr = -500
endjahr = 20
max_erbfolge = 3  # Wenn man weiter vom Familienkern entfernt ist, werden keine Kinder mehr generiert
fruchtbar = [18, 60]  # In welcher Altersspanne kann man Kinder bekommen
hauptfamilien = ["von Möwenburg", "von Tiefenfels", "von Eichenwald", "von Bergetal", "von Kisatris"]
namenskuerzel = {"von Möwenburg": "MB", "von Tiefenfels": "TF", "von Eichenwald": "EW", "von Bergetal": "BT",
                 "von Kisatris": "KS", "von der Münze": "MU"}
herkunftmoeglich = ["TF", "EW", "MB", "BT", "MU"]


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

# neu = "Marie/Maria, Elisabeth/Else, Anna, Margarete, Helene, Gertrud, Luise/Louise, Hedwig, Auguste, Johanna, Sophie, Charlotte, Clara, Mathilde, Emma, Martha, Ida, Bertha, Frieda, Julie, Käthe"
# neuenamen("f", neu)

class color:  # um farbig zu printen
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


def get_erbfolge(person_input, jahr):
    if (person_input[3] == "von Kisatris"):
        personenzeiger.execute(
            "SELECT count(*) from personen WHERE nachname = ? and kisatris_primogen < ? and todesjahr > ? order by kisatris_primogen asc;",
            (person_input[2], person_input[13], jahr))
    else:
        personenzeiger.execute(
            "SELECT count(*) from personen WHERE nachname = ? and (erbfolge  < ? or (erbfolge = ? and geburtsjahr < ?)) and todesjahr > ? order by erbfolge asc, geburtsjahr asc;",
            (person_input[2], person_input[9], person_input[9], person_input[4], jahr))
    erbfolge_int = personenzeiger.fetchall()[0][0]

    return erbfolge_int


def geburt(geschlecht=None, jahr=None, todesjahr=None, vater=None, mutter=None, herkunft=None):
    if geschlecht == None: geschlecht = random.choice(["male", "female"])

    if vater != None:
        personenzeiger.execute("SELECT * from personen WHERE uuid = ?;", (vater,))
        vater_person = personenzeiger.fetchall()[0]
    if mutter != None:
        personenzeiger.execute("SELECT * from personen WHERE uuid = ?;", (mutter,))
        mutter_person = personenzeiger.fetchall()[0]

    if herkunft is None:
        if random.randint(0,100)<10:
            herkunft="KS"
    # -Nachname
    if(herkunft=="KS"):
        namenzeiger.execute("SELECT nachname FROM landadel where gender = ?", (geschlecht,))
    else:
        namenzeiger.execute("SELECT * FROM surname")
    nachnamensliste = namenzeiger.fetchall()
    nachname = random.choice(nachnamensliste)[0]

    # Nachnamen von Hauptfamilien bleiben
    if vater != None and mutter != None and vater_person[9] != None and mutter_person[9] != None:
        if get_erbfolge(vater_person, jahr) < get_erbfolge(mutter_person, jahr):  # wenn Vater näher in Erbfolge ist
            nachname = vater_person[2]
        elif get_erbfolge(vater_person, jahr) > get_erbfolge(mutter_person, jahr):  # wenn Mutter näher in Erbfolge ist
            nachname = mutter_person[2]
        else:
            if random.randint(0, 1) == 1:
                nachname = vater_person[2]
            else:
                nachname = mutter_person[2]
    elif mutter != None and mutter_person[2] in hauptfamilien:
        nachname = mutter_person[2]
    elif vater != None and vater_person[2] in hauptfamilien:
        nachname = vater_person[2]
    # Beide Eltern haben keinen Erbfolgeplatz, sind aber definiert. Dann bekommt Kind den Namen des Nichtadeligen Elternteils
    if vater != None and mutter != None and vater_person[9] == None and mutter_person[9] == None:
        if vater_person[6] == None and mutter_person[6] != None:
            nachname = vater_person[2]
        elif mutter_person[6] == None and vater_person[6] != None:
            nachname = mutter_person[2]
        else:
            if random.randint(0, 1) == 1:
                nachname = vater_person[2]
            else:
                nachname = mutter_person[2]

            # Herkunft bestimmen
    if nachname in hauptfamilien:
        herkunft = namenskuerzel[nachname]
    elif herkunft is None:
        herkunft = random.choice(herkunftmoeglich)

    # -Vorname
    namenzeiger.execute("SELECT * FROM " + geschlecht + " WHERE vorkommen LIKE '%" + herkunft + "%'")
    namensliste = namenzeiger.fetchall()
    vorname = ""
    # Zumeist einen Vornamen von Eltern übernehmen
    if vater != None and mutter != None:  # Zumeist einen Vornamen von Eltern übernehmen
        if random.randint(1, 20) >= 2:
            if geschlecht == "male" and vater_person[3] == "m":
                vorname = random.choice(vater_person[1].split(" ")) + " "
            elif geschlecht == "female" and mutter_person[3] == "w":
                vorname = random.choice(mutter_person[1].split(" ")) + " "
            # print(">>>>>NAMEN ÜBERNEHMEN: ", vorname)

    namenszahl = min(random.randint(1, 3), random.randint(1, 3)) + min(random.randint(0, 2), random.randint(0, 2))
    for i in range(namenszahl):
        neuername = random.choice(namensliste)[0]
        if not neuername in vorname:
            vorname += neuername
            if not i == namenszahl - 1: vorname += " "
    if vorname[-1] == " ": vorname = vorname[:-1]

    if vorname[0] == " ":
        print(color.RED, "ACHTUNG! Vorname beginnt mit Lehrzeichen", color.END)
        print(vorname)
        print(vater_person[1].split(" "))
        print(mutter_person[1].split(" "))

    # Todesjahr bestimmen
    if jahr != None and todesjahr == None: todesjahr = jahr + min(random.randint(0, 110), random.randint(0, 110),
                                                                  random.randint(0, 110)) + min(random.randint(0, 10),
                                                                                                random.randint(0, 10))

    # Erbfolgenplatz bestimmen
    erbfolge = None
    kisatrisPrimogen = "Z"
    if nachname == "von Kisatris":
        if vater_person[13] < mutter_person[13]:
            personenzeiger.execute(
                "SELECT count(*) from personen WHERE nachname = 'von Kisatris' and (mutter = ? OR vater = ?) and geburtsjahr <= ?  order by kisatris_primogen asc;",
                (vater_person[0],vater_person[0], jahr))
            kisatrisPrimogen = vater_person[13]
        else:
            personenzeiger.execute(
                "SELECT count(*) from personen WHERE nachname = 'von Kisatris' and (mutter = ? OR vater = ?) and geburtsjahr <= ? order by kisatris_primogen asc;",
                (mutter_person[0],mutter_person[0], jahr))
            kisatrisPrimogen = mutter_person[13]
        anzahl_geschwister = personenzeiger.fetchall()[0][0]
        kisatrisPrimogen = kisatrisPrimogen + chr(65 + anzahl_geschwister)

    if vater != None:
        if nachname == vater_person[2]:
            # print("vater: ",vater)
            erbfolge = vater_person[9]
    if mutter != None:
        if nachname == mutter_person[2]:
            erbfolge = mutter_person[9]

    geschlecht = geschlecht[0]  # nur den ersten Buchstaben des Strings
    personenzeiger.execute("INSERT INTO personen VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
        None, vorname, nachname, geschlecht, jahr, todesjahr, vater, mutter, None, erbfolge, 0, "", herkunft,
        kisatrisPrimogen, None, None, erbfolge))
    personendatenbank.commit()
    personenzeiger.execute("SELECT * from personen WHERE uuid = (SELECT MAX(uuid) FROM personen);")
    person = personenzeiger.fetchall()[0]
    return (person)


def parship(person, personen):
    partner = None
    if person[8] != None:  # bleibender partner
        if random.randint(1, 12) >= 2:
            personenzeiger.execute("SELECT * from personen WHERE uuid = ?;", (person[8],))
            partner = personenzeiger.fetchall()[0]
            partner_alter = aktuelles_jahr - partner[4]
            if partner[5] < aktuelles_jahr + 3: # Witwer heiraten neu
                if partner_alter >= fruchtbar[0] and partner_alter <= fruchtbar[1] and partner[5] >= aktuelles_jahr :
                    return (partner)
                else:
                    return (None)

    if random.randint(1, 10) >= 6:  # Partner aus Hauptfamilie
        partner = random.choice(personen)
        if partner != person:
            partner_alter = aktuelles_jahr - partner[4]
            if partner_alter >= fruchtbar[0] and partner_alter <= fruchtbar[1]:  # Partner muss im fruchtbaren Alter #//and partner[3] != person[3]
                 return (partner)

    # Nur einmal pro Jahr Kinder bekommen
    if person[0] in hat_gebaert: return (None)
    if person[3] == "f": hat_gebaert.append(person[0])
    if partner != None:
        if partner[0] in hat_gebaert: return (None)
        if partner[3] == "f": hat_gebaert.append(partner[0])

    # neuer Partner
    alter = aktuelles_jahr - person[4]
    # Partner muss ähnliches Alter haben, muss fruchtbares Alter haben und darf nicht schon vorher gestorben sein
    partner_alter = alter + random.randint(-5, 0) + random.randint(-3, 20)
    if partner_alter < fruchtbar[0]:
        partner_alter = fruchtbar[0]
    elif partner_alter > fruchtbar[1]:
        partner_alter = fruchtbar[1]
    partner_geburtsjahr = aktuelles_jahr - alter
    partner_todesjahr = partner_geburtsjahr + min(random.randint(0, 120), random.randint(0, 120),
                                                  random.randint(0, 120))
    if partner_todesjahr < aktuelles_jahr: partner_todesjahr = aktuelles_jahr  # Keine Nekrophilie hier!
    if (person[2] == "von Kisatris"):
        if person[3] == "m":
            partner = geburt(geschlecht="female", jahr=partner_geburtsjahr, todesjahr=partner_todesjahr, herkunft="KS")
        elif person[3] == "f":
            partner = geburt(geschlecht="male", jahr=partner_geburtsjahr, todesjahr=partner_todesjahr, herkunft="KS")
        else:
            raise ValueError("Elter hat kein akzeptiertes Geschlecht.")
    else:
        if person[3] == "m":
            partner = geburt(geschlecht="female", jahr=partner_geburtsjahr, todesjahr=partner_todesjahr)
        elif person[3] == "f":
            partner = geburt(geschlecht="male", jahr=partner_geburtsjahr, todesjahr=partner_todesjahr)
        else:
            raise ValueError("Elter hat kein akzeptiertes Geschlecht.")
    # print(partner,partner[0][0])
    # print(person,person[0][0])
    # personenzeiger.execute("UPDATE personen SET letzter_partner = ? WHERE uuid = ?",(partner[0],person[0],))
    # personenzeiger.execute("UPDATE personen SET letzter_partner = ? WHERE uuid = ?",(person[0],partner[0],))
    # personendatenbank.commit()
    return (partner)


def kinderchance(hauptp, nebenp, aktuelles_jahr):
    ok = [False, False]
    alterhp = aktuelles_jahr - hauptp[4]
    alternp = aktuelles_jahr - nebenp[4]
    if hauptp[3] == "m":
        if random.randint(100, 300) - alterhp * 2 >= 100: ok[0] = True
    elif hauptp[3] == "f":
        if random.randint(125, 205) - alterhp * 2 >= 100: ok[0] = True
    if nebenp[3] == "m":
        if random.randint(100, 300) - alternp * 2 >= 100: ok[1] = True
    elif nebenp[3] == "f":
        if random.randint(125, 205) - alternp * 2 >= 100: ok[1] = True
    if hauptp[3] == nebenp[3] and ok[0]:
        return True  # Bei Gleichgeschlechtlich ist nur Hauptpartner relevant
    elif ok[0] and ok[1]:
        return True
    else:
        return False  # keine Kinder


def erbfolge_setzen(ahn):
    personenzeiger.execute(
        "update personen set erbfolge = 1 WHERE uuid = ? ",
        (ahn[0],))
    personenzeiger.execute(
        "SELECT * FROM personen WHERE (vater = ? OR mutter = ?) AND nachname = ? ",
        (ahn[0], ahn[0], ahn[2]))
    print("erbfolge setzen fuer ? ", ahn[0])
    for kind in personenzeiger.fetchall():
        erbfolge_setzen(kind)
    pass

aktuelles_jahr = startjahr
neustarten = False

def reset():
    global aktuelles_jahr
    global neustarten
    personenzeiger.execute("delete from  personen where true")
    personenzeiger.execute("insert into personen select * from start_personen")
    personenzeiger.execute("update sqlite_sequence set seq = 100 where name = 'personen' ")
    personendatenbank.commit()
    aktuelles_jahr = startjahr
    neustarten = False
pass

# Hier beginnt der Durchgang!

reset()
while aktuelles_jahr <= endjahr:
    print(color.BOLD, "Jahr: ", aktuelles_jahr, color.END)
    hat_gebaert = []
    personen_familie = {}
    lebendige_hauptfamilien = 0
    for familie in hauptfamilien:
        # print(familie)
        personen_familie[familie] = []
        personenzeiger.execute("SELECT * FROM personen WHERE nachname = ? AND geburtsjahr <= ? AND todesjahr >= ?",
                               (familie, aktuelles_jahr, aktuelles_jahr))
        lebendige_familienmitglieder = personenzeiger.fetchall()
        # print(">>lebendige_familienmitglieder: ",lebendige_familienmitglieder)

        personenzeiger.execute(
            "SELECT count(*) FROM personen WHERE geburtsjahr < ? AND todesjahr >= ? AND nachname = ? AND amtsantritt is not null and amtsantritt >= ?",
            (aktuelles_jahr, aktuelles_jahr, familie, aktuelles_jahr))
        if (personenzeiger.fetchone()[0] > 1):
            print("Error: mehr als ein Fürst bei Familie ? ind Jahr ? ", familie, aktuelles_jahr)


        personenzeiger.execute(
            "SELECT * FROM personen WHERE geburtsjahr < ? AND todesjahr >= ? AND nachname = ? AND amtsantritt is not null and amtsantritt <= ?",
            (aktuelles_jahr, aktuelles_jahr, familie, aktuelles_jahr))
        fuerst_list=personenzeiger.fetchall()
        if len(fuerst_list) > 0:
            fuerst = fuerst_list[0]
        else:
            fuerst = None

        # Unklare Erbfolge klären
        if fuerst is None:
            print("Erbfolgeproblem bei ", familie)

            if (familie == "von Kisatris"):
                personenzeiger.execute(
                    "SELECT * from personen WHERE nachname = ? and todesjahr >= ? and geburtsjahr < ? order by kisatris_primogen asc;",
                    (familie, aktuelles_jahr, aktuelles_jahr))
                anwaerter = personenzeiger.fetchall()
                if len(anwaerter) < 1:
                    print("ERROR Familie stirbt aus ", familie)
                    neustarten = True
                    break
                else:
                    fuerst = anwaerter[0]
                    comment = "Amtsantritt nach Primogenität"
                    if fuerst[9] == 1:
                        personenzeiger.execute(
                            "update personen set erbfolge = erbfolge + 1 WHERE nachname = ? and uuid != ?",
                            (familie, fuerst[0]))
                    erbfolge_setzen(fuerst)
            else:
                personenzeiger.execute(
                    "SELECT * from personen WHERE nachname = ? and todesjahr >= ? and geburtsjahr < ? order by erbfolge asc, geburtsjahr asc, uuid asc;",
                    (familie, aktuelles_jahr, aktuelles_jahr))
                anwaerter = personenzeiger.fetchall()
                if len(anwaerter)<1:
                    print("ERROR Familie stirbt aus ", familie)
                    neustarten = True
                    break
                else:
                    if(random.randint(1, 100)<=5 and len(anwaerter) > 1):
                        print("greater army diplomancy bei ", familie)
                        if(random.randint(1, 2)==1):
                            fuerst = anwaerter[1]
                            comment = "Amtsantritt als zweiter in Thronfolge"
                        else:
                            index = random.randint(1, min(10, len(anwaerter) - 1))
                            fuerst = anwaerter[index]
                            comment = "Amtsantritt als n-ter in Thronfolge: " + str(index)
                    else:
                        fuerst = anwaerter[0]
                        comment = "Amtsantritt mit entfernung zum alten Fürsten: " +str(fuerst[9])
                if fuerst[9] == 1:
                    personenzeiger.execute(
                        "update personen set erbfolge = erbfolge + 1 WHERE nachname = ? and uuid != ?",
                        (familie, fuerst[0]))
                erbfolge_setzen(fuerst)

            personenzeiger.execute(
                "update personen set amtsantritt = ?, comment = ? WHERE uuid = ? ",
                (aktuelles_jahr, comment, fuerst[0]))
            personendatenbank.commit()

            print("neuer Fürst von ", familie ," ist ", fuerst[0] ,": ", fuerst[1] ," ", fuerst[2] ," im Jahr ", aktuelles_jahr)

            personenzeiger.execute("SELECT * FROM personen WHERE geburtsjahr < ? AND todesjahr >= ? AND nachname = ?",
                                   (aktuelles_jahr, aktuelles_jahr, familie))
            personen_familie[familie] = personenzeiger.fetchall()
        else:
            personenzeiger.execute(
                "SELECT * FROM personen WHERE geburtsjahr < ? AND todesjahr >= ? AND nachname = ? AND amtsantritt is not null and amtsantritt <= ?",
                (aktuelles_jahr, aktuelles_jahr, familie, aktuelles_jahr))
            fuerst = personenzeiger.fetchall()[0]

        if (fuerst is None):
            print(color.RED, "Familie " + familie + " stirbt aus.", color.END)
            hauptfamilien.pop(hauptfamilien.index(familie))

        else:
            lebendige_hauptfamilien += 1

    if (neustarten):
        reset()
        continue
    personenzeiger.execute("SELECT * FROM personen WHERE geburtsjahr < ? AND todesjahr >= ? AND erbfolge < ?",
                           (aktuelles_jahr, aktuelles_jahr, max_erbfolge))
    personen = personenzeiger.fetchall()
    personenzeiger.execute("SELECT COUNT(*) FROM personen")
    personenzahl = personenzeiger.fetchone()[0]
    print(">>>Lebendige relevante Hauptfamilienmitglieder: ", len(personen), ", lebendige_hauptfamilien: ",
          lebendige_hauptfamilien, ", Personen gesamt: ", personenzahl)

    for person in personen:  # bekommen Personen Kinder?
        if person[9] == None or person[
            9] >= max_erbfolge: continue  # wer zu weit von Erbfolge entfernt ist, wird ignoriert
        # print("person: ",person)
        alter = aktuelles_jahr - person[4]
        # print(alter)
        if alter >= fruchtbar[0] and alter <= fruchtbar[1]:  # Wenn im fruchtbaren Alter
            kinderzahl = person[10]
            if random.randint(1, 10) >= 5 + (kinderzahl / 1.5):  # Wahrscheinlichkeit eines Kinderwunsches
                # print("XXX BABY XXX")
                partner = parship(person, personen)
                if partner != None:
                    kind = None
                    # print("PERSON: ",person)
                    # print("PARTNER: ",partner)
                    if person[3] == partner[3]:  # Partner haben gleiches geschlecht
                        # print("Gleichgeschlechtlich: ",person[0],partner[0])
                        if person[9] == None:
                            person_erbfolge = 100
                        else:
                            person_erbfolge = person[9]
                        if partner[9] == None:
                            partner_erbfolge = 100
                        else:
                            partner_erbfolge = partner[9]
                        if person_erbfolge < partner_erbfolge:  # wenn Person näher in Erbfolge ist
                            hauptpartner = person
                            nebenpartner = partner
                        elif person_erbfolge > partner_erbfolge:  # wenn Partner näher in Erbfolge ist
                            hauptpartner = partner
                            nebenpartner = person
                        else:  # beide sind gleich Erbberechtigt, also entscheidet Zufall
                            if random.randint(0, 1) == 1:
                                hauptpartner = partner
                                nebenpartner = person
                            else:
                                hauptpartner = person
                                nebenpartner = partner
                        if hauptpartner[3] == "m":
                            if kinderchance(hauptpartner, nebenpartner, aktuelles_jahr): kind = geburt(geschlecht=None,
                                                                                                       jahr=aktuelles_jahr,
                                                                                                       vater=
                                                                                                       hauptpartner[0],
                                                                                                       mutter=
                                                                                                       nebenpartner[0])
                        elif hauptpartner[3] == "f":
                            if kinderchance(hauptpartner, nebenpartner, aktuelles_jahr): kind = geburt(geschlecht=None,
                                                                                                       jahr=aktuelles_jahr,
                                                                                                       vater=
                                                                                                       nebenpartner[0],
                                                                                                       mutter=
                                                                                                       hauptpartner[0])
                        else:
                            raise ValueError("Elter hat kein akzeptiertes Geschlecht.")
                    # Partner haben unterschiedliches Geschlecht
                    if person[3] == "m":
                        if kinderchance(person, partner, aktuelles_jahr): kind = geburt(geschlecht=None,
                                                                                        jahr=aktuelles_jahr,
                                                                                        vater=person[0],
                                                                                        mutter=partner[0])
                    elif person[3] == "f":
                        if kinderchance(person, partner, aktuelles_jahr): kind = geburt(geschlecht=None,
                                                                                        jahr=aktuelles_jahr,
                                                                                        vater=partner[0],
                                                                                        mutter=person[0])
                    else:
                        raise ValueError("Elter hat kein akzeptiertes Geschlecht.")
                    if kind != None:
                        personenzeiger.execute("UPDATE personen SET kinderzahl = kinderzahl + 1 WHERE uuid IN (?,?)",
                                               (person[0], partner[0],))
                        personenzeiger.execute("UPDATE personen SET kinder = kinder || ? || ',' WHERE uuid IN (?,?)",
                                               (kind[0], person[0], partner[0],))
                        personenzeiger.execute("UPDATE personen SET letzter_partner = ? WHERE uuid = ?",
                                               (partner[0], person[0],))
                        personenzeiger.execute("UPDATE personen SET letzter_partner = ? WHERE uuid = ?",
                                               (person[0], partner[0],))
                        personendatenbank.commit()
                    # print("KIND: ",kind)

    aktuelles_jahr += 1

# namendatenbank.commit()
namendatenbank.close()
# personendatenbank.commit()
personendatenbank.close()
