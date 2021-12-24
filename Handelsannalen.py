#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

warenbedarfe = {"Wein":30,"Schaumwein":10,"Holz":10,"Bögen":5,"Armbrüste":2,"Weizen":100,"Gerste":20,"Hafer":80,"Bier":50,"Erz":10,"Schwerter":5,"Lehm":10,"Stein":10,"Fisch":50,"Muscheln":10,"Fleisch":20,"Zwiebeln":40,"Kartoffeln":40} #werden auf alle Städte angewandt

feierbedarf = ["Wein", "Schaumwein","Bier","Gerste"]
kriegsbedarf = ["Bögen","Schwerter","Armbrüste","Holz","Erz"]
baubedarf = ["Holz","Lehm","Stein","Erz"]
nahrung = ["Weizen","Hafer","Fisch","Muscheln","Fleisch","Zwiebeln","Kartoffeln"]

staedte = {"Tiefenfels":{"Wein":80,"Schaumwein":20,"Weizen":40},
           "Eichenwald":{"Holz":50,"Bögen":40,"Armbrüste":20},
           "Flusslauf":{"Weizen":150, "Hafer":120,"Bier":80},
           "Bergetal":{"Bier":80,"Gerste":60,"Erz":30},
           "Migdal":{"Erz":60,"Schwerter":40,"Holz":80}}
eigene_waren = {"Holz":3,"Bögen":2,"Armbrüste":1,"Weizen":50,"Gerste":5,"Hafer":20,"Bier":20,"Schwerter":2,"Lehm":20,"Stein":2,"Fisch":100,"Muscheln":20,"Fleisch":12,"Zwiebeln":15,"Kartoffeln":20}

herrscher = "Gräfin Nelenias von Möwenburg" #im Genitiv
jahre = 8 #Dauer, die berechnet werden soll

mindesthandelsmenge = 5 #Eigene Bedarfe unter diesem Wert werden aufs nächste Jahr aufgeschoben, Verkäufe unter diesem Wert kommen nicht zustande

warenarten = {"Wein":"Fässer","Schaumwein":"Fässer","Holz":"Karren","Bögen":"","Armbrüste":"","Weizen":"Säcke","Gerste":"Säcke","Hafer":"Säcke","Bier":"Fässer","Erz":"Karren","Schwerter":"","Lehm":"Karren","Stein":"Karren","Fisch":"Fässer","Muscheln":"Karren","Fleisch":"Säcke","Zwiebeln":"Säcke","Kartoffeln":"Säcke"}
ereignisse = ["Nichts","Feier","Krieg","Missernte","Glücksernte","Gebäudebau"]
ereignischance = [15,5,3,1,1,2]
ereignisoutput = ""
aufgeschoben = {}

output = ""
gekauft = {}
verkauft = {}

for i in range(jahre):
    #print(">>>>>Jahr: ", i+1)
    if i == 5: staedte.pop("Migdal") #Migdal wird zerstört
    
    #Ereignischeck
    ereignis = random.choices(ereignisse,weights = ereignischance)[0]
    if ereignis != "Nichts": ereignisoutput += "Im Jahr " + str(i+1) + " war in der Stadt ein(e) " + ereignis + ". \n"
    #print(">>Ereignis: ",ereignis)
    
    #Eigenproduktion errechnen
    jahresproduktion = {}
    for ware in eigene_waren:
        jahresproduktion[ware] = round(eigene_waren[ware]+eigene_waren[ware]*(random.randint(-10,10)/100))
    if ereignis == "Glücksernte":
        for ware in nahrung:
            if ware in jahresproduktion:
                jahresproduktion[ware] += jahresproduktion[ware] *0.5
    elif ereignis == "Missernte":
        for ware in nahrung:
            if ware in jahresproduktion: jahresproduktion[ware] += jahresproduktion[ware] *-0.5
    #print(">>Jahresproduktion: ", jahresproduktion)
    
    #Bedarf errechnen
    jahresbedarf = {}
    for bedarf in warenbedarfe:
        jahresbedarf[bedarf]= round(warenbedarfe[bedarf]+warenbedarfe[bedarf]*(random.randint(-10,10)/100))
    if ereignis == "Feier":
        for ware in feierbedarf: jahresbedarf[ware] += jahresbedarf[ware]*0.8
        for ware in nahrung: jahresbedarf[ware] += jahresbedarf[ware]*0.1
    if ereignis == "Krieg":
        for ware in kriegsbedarf: jahresbedarf[ware] += jahresbedarf[ware]*1.2
        for ware in eigene_waren: jahresproduktion[ware] -= jahresproduktion[ware]*0.2
    if ereignis == "Gebäudebau":
        for ware in baubedarf:jahresbedarf[ware] += jahresbedarf[ware]*0.2
    for bedarf in aufgeschoben:
        jahresbedarf[bedarf] += aufgeschoben[bedarf]
    #print(">>Jahresbedarf: ",jahresbedarf)
    
    #Selbstversorgung
    for ware in jahresproduktion:
        jahresbedarf[ware] -= jahresproduktion[ware]
        jahresproduktion[ware] -= jahresbedarf[ware]
        if jahresbedarf[ware] < 0: jahresbedarf[ware] = 0
        if jahresproduktion[ware] < 0: jahresproduktion[ware] = 0
        if jahresbedarf[ware] < mindesthandelsmenge:
            aufgeschoben[ware] = jahresbedarf[ware]
            jahresbedarf[ware] = 0
            
    #print(">>>Netproduktion: ",jahresproduktion)
    #print(">>>Netbedarf: ",jahresbedarf)
    
    
    #berechnen
    staedtereihe = random.sample(list(staedte), k=len(staedte))
    #print(staedtereihe)
    for stadt in staedtereihe:
        #produktion der Handelsstadt
        stadtproduktion = {}
        for ware in staedte[stadt]:
            stadtproduktion[ware] = round(staedte[stadt][ware]+staedte[stadt][ware]*(random.randint(-10,10)/100))
        #Bedarf der Handelsstadt
        stadtbedarf = {}
        for bedarf in warenbedarfe:
            stadtbedarf[bedarf] = round(warenbedarfe[bedarf]+warenbedarfe[bedarf]*(random.randint(-10,10)/100))
            if bedarf in stadtproduktion:
                stadtbedarf[bedarf] -= stadtproduktion[bedarf]
                stadtproduktion[bedarf] -= stadtbedarf[bedarf]
                if stadtbedarf[bedarf] < 0: stadtbedarf[bedarf] = 0
                if stadtproduktion[bedarf] < 0: stadtproduktion[bedarf] = 0
                
        #Käufe        
        gekauft[stadt] = []
        for ware in jahresbedarf:
            if jahresbedarf[ware] > 0 and random.randint(1,100) <= 90: #manchmal kommt kein Handel zustande um Varianz zu erzwingen
                if ware in stadtproduktion:
                    if jahresbedarf[ware] >= stadtproduktion[ware]:
                        menge = round(stadtproduktion[ware])
                        jahresbedarf[ware] -= menge
                    elif jahresbedarf[ware] < stadtproduktion[ware]:
                        menge = round(jahresbedarf[ware])
                        jahresbedarf[ware] = 0
                    if menge >= 1: gekauft[stadt].append([menge,warenarten[ware],ware])
        if gekauft[stadt] == []: gekauft.pop(stadt)
        
        #Verkäufe
        verkauft[stadt] = []
        for ware in eigene_waren:
            if stadtbedarf[ware] > 0 and random.randint(1,100) <= 90: #manchmal kommt kein Handel zustande um Varianz zu erzwingen
                menge = 0
                #print("JAHR: ", i+1, " STADT: ", stadt, " WARE: ",ware," PRODUKTION: ",jahresproduktion[ware], " BEDARF: ",stadtbedarf[ware])
                if stadtbedarf[ware] >= jahresproduktion[ware] and jahresproduktion[ware] >=mindesthandelsmenge:
                    menge = round(jahresproduktion[ware])
                    jahresproduktion[ware] = 0
                elif stadtbedarf[ware] < jahresproduktion[ware] and stadtbedarf[ware] >=mindesthandelsmenge:
                    menge = round(stadtbedarf[ware])
                    jahresproduktion[ware] -= menge
                if menge != 0:
                    verkauft[stadt].append([menge,warenarten[ware],ware])
        if verkauft[stadt] == []: verkauft.pop(stadt)
    
    #Output generieren
    output+= "\n Im " + str(i+1) + ". Jahr der Herrschaft " + herrscher + " kaufte die Stadt "
    handelmitstaedten = len(gekauft)
    x = 0
    for stadt in gekauft:
        x += 1
        zahlgekaufterdinge = len(gekauft[stadt])
        
        for i in range(zahlgekaufterdinge):
            gekauftes = gekauft[stadt][i]
            if gekauftes[1] == "": output += str(gekauftes[0]) + " " + gekauftes[2]
            else: output += str(gekauftes[0]) + " " + gekauftes[1] + " " + gekauftes[2]
            if i < zahlgekaufterdinge-2: output += ", "
            elif i == zahlgekaufterdinge-2: output += " sowie "
        if zahlgekaufterdinge != 0: output += " in " + stadt + " "
        if x == handelmitstaedten-1: output += "und "
        elif x < handelmitstaedten-1: output = output[:-1]+", "
        #elif x == handelmitstaedten: output = output[:-1]+". "
    
    output = output[:-1]+" und verkaufte "
    
    #print("GEKAUFT:",gekauft)
    #print("VERKAUFT:",verkauft)
    
    handelmitstaedten = len(verkauft)
    if handelmitstaedten == 0: output += "nichts."
    x = 0
    for stadt in verkauft:
        x += 1
        zahlverkaufterdinge = len(verkauft[stadt])
        
        for i in range(zahlverkaufterdinge):
            verkauftes = verkauft[stadt][i]
            if verkauftes[1] == "": output += str(verkauftes[0]) + " " + verkauftes[2]
            else: output += str(verkauftes[0]) + " " + verkauftes[1] + " " + verkauftes[2]
            if i < zahlverkaufterdinge-2: output += ", "
            elif i == zahlverkaufterdinge-2: output += " sowie "
        if zahlverkaufterdinge != 0: output += " in " + stadt + " "
        if x == handelmitstaedten-1: output += "und "
        elif x < handelmitstaedten-1: output = output[:-1]+", "
        elif x == handelmitstaedten: output = output[:-1]+". "
        
print(output)
print(ereignisoutput)
