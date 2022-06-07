import random
from typing import Counter

#Januar 2022
"""
Hra je navrhnuta na vyber medzi panakmi takze ich moze byt viac na sachovnici, pri vstupe do domceka sa panak uklada na posledne miesto v domceku.
Pri hodeni 6 a vybere noveho panaka sa sachovnica nezobrazi hned (pomocna premenna f), hrac hadze este raz a po hodeni sa zobrazi sachovnica(na zamedzenie aby hrac nestal nikdy na 
pozicii domceka)
Pri nastaveni noveho panacika ked jeden je uz na hracej ploche je mozne ze nastane chyba kedze by sme mali napr panaka A0 - 5 a zvolime noveho panaka po hode 6
a ten hodi tiez 5 nastane chyba .. Toto nie je dorisene este
"""

def gensachovnica(n):
    sachovnica = [[" " for i in range(n)]for j in range(n)] #vytvorenie praznej sachovnice n*n
    middle_pos = int((n-1)/2)   #vypocet stredu sachovnice
    count = 1
    # postupne nahratie pozici z listu policka do sachovnice n*n(aby som to nemusel ratat cez suradnice)
    for j in range(1):
        sachovnica[0][middle_pos+1] = policka[0]
    #riadok opkujuci sa
    for j in range(1,middle_pos-1):
        sachovnica[j][middle_pos+1] = policka[count]
        count +=1
    #riadok nad stred
    for j in range(middle_pos+1,n):
        sachovnica[middle_pos-1][j] = policka[count]
        count +=1
    #riadok stred
    for j in range(1):
        sachovnica[middle_pos][n-1] = policka[count]
        count +=1
    #riadok pod stred
    for j in range(n-1,middle_pos,-1):
        sachovnica[middle_pos+1][j] = policka[count]
        count +=1
    #riadok opakujuci sa
    for j in range(middle_pos+2,n-1):
        sachovnica[j][middle_pos+1] = policka[count]
        count +=1
    #riadok spodok
    for j in range(middle_pos+1,middle_pos-1,-1):
        sachovnica[n-1][j] = policka[count]
        count +=1   
    #riadok opakujuci sa
    for j in range(n-1,middle_pos+1,-1):
        sachovnica[j][middle_pos-1] = policka[count]
        count +=1
    #riadok pod stred
    for j in range(middle_pos-1,-1,-1):
        sachovnica[middle_pos+1][j] = policka[count]
        count +=1
    #riadok stred
    for j in range(1):
        sachovnica[middle_pos][0] = policka[count]
        count +=1
    #riadok nad stred
    for j in range(0,middle_pos):
        sachovnica[middle_pos-1][j] = policka[count]
        count +=1
    #riadok opakujuci sa
    for j in range(middle_pos-2,0,-1):
        sachovnica[j][middle_pos-1] = policka[count]
        count +=1
    #riadok final
    for j in range(middle_pos-1,middle_pos+1):
        sachovnica[0][j] = policka[count]
        count +=1
    #stred stred
    sachovnica[middle_pos][middle_pos] = "■"
    #domcek 1
    i=0
    for j in range(1,middle_pos):
        sachovnica[j][middle_pos] = dom[0][i]
        i+=1
    #domcek 2
    i=0
    for j in range(n-2,middle_pos,-1):
        sachovnica[middle_pos][j] = dom[2][i]
        i+=1
    #domcek 3
    i=0
    for j in range(n-2,middle_pos,-1):
        sachovnica[j][middle_pos] = dom[1][i]
        i+=1
    #domcek 4
    i=0
    for j in range(1,middle_pos):
        sachovnica[middle_pos][j] = dom[3][i]
        i+=1

    return sachovnica

while True:
    n = int(input("Zadaj velkost hracej plochy = "))    
    if n < 5:
        print("Zadal si cislo mensie ako 5")
        continue
    elif n%2 == 0:
        print("Zadal si parne cislo")
        continue
    else:
        break

pocet_panakov = int((n-3)/2)    #vypocet poctu panakov
pocet_policok = int(16+8*(pocet_panakov-1)) #vypocet poctu policok na hracom poli
policka = ["*"]*pocet_policok   #list s polickami
dom = [["D" for i in range(pocet_panakov)]for i in range(4)]    #vytvorenie listu pre domceky

def print_sachovnica(a):    #vykreslenie sachovnice
    print("  ", end = "")
    for column1 in range(0,n):
        print(column1%10, end= " ") #vypis hornych cisel
    print()
    for row in range(0,n):
        print(row%10,end = " ") #vypis kolmych cisel
        for column in range(0,n):
            print(a[row][column],end = " ") # vypis sachovnice
        print()

def dice_throw():   #funkcia hodu 
    input("Stlac enter pre hod kockou")
    vysledok = random.randint(1,6)
    return vysledok

def start_player_A(spawn,hrac,dostupny_panaci,f):   #funkcia startu pre hraca A
    spawnpoint = 0                                             #miesto kde zacian
    spawn[hrac][dostupny_panaci[hrac][0]][1] = spawnpoint   #ulozenie pozicie
    f[0] = dostupny_panaci[hrac][0]                         #pomocna premenna 
    print("Hodil si 6 a zvolil noveho panaka, hadz este raz")                            
    dostupny_panaci[hrac].pop(0)                            #delete jedneho pacanika z dostupnych panakov hraca A

def start_player_B(spawn,hrac,dostupny_panaci,f):      #funkcia startu pre hraca B
    spawnpoint = int((pocet_policok/2))                 #vypocet kde zacina hrac B
    spawn[hrac][dostupny_panaci[hrac][0]][1] = spawnpoint   #ulozenie pozicie
    f[0] = dostupny_panaci[hrac][0]                         #pomocna premenna
    print("Hodil si 6 a zvolil noveho panaka, hadz este raz")                     
    dostupny_panaci[hrac].pop(0)                           #delete jedneho panacika z dostupnych panakov hraca B

def basicmove(pouzivana_pozicia,hod,hraci,hrac,spawn,aktual_panak,home_B): #funkcia klasickeho pohybu po sachovnici
    policka[hod+pouzivana_pozicia] = hraci[hrac][0]                 #prepis za * na hracom poli pri posune
    symbol = policka[pouzivana_pozicia]                          
    if hrac == 0 and spawn[hrac][aktual_panak][1] == 0:
        policka[pouzivana_pozicia] = symbol
    elif hrac == 1 and spawn[hrac][aktual_panak][1] == home_B:
        policka[pouzivana_pozicia] = symbol
    else:
        policka[pouzivana_pozicia] = "*"
    print_sachovnica(gensachovnica(n))
    pouzivana_pozicia = pouzivana_pozicia+hod                       
    spawn[hrac][aktual_panak][1] = pouzivana_pozicia                #ulozenie pozicie kam dosiel panak
    print(spawn)
    
def basicmove_prelom(pouzivana_pozicia,hraci,hrac,aktual_panak,spawn,x):    #posun pre hraca B cez koniec sachonice/zaciatok
    policka[pouzivana_pozicia] = "*"                #prepis kde sa stal
    policka[x] = hraci[hrac][0]                     #posun na nove policko
    print_sachovnica(gensachovnica(n))
    spawn[hrac][aktual_panak][1] = x                #ulzoenie pozicie
    print(spawn)

def domcek(pouzivana_pozicia,hrac,hraci,spawn,aktual_panak,homespace):  #posun do domceka 
    policka[pouzivana_pozicia] = "*"                    #prepis pozicie kde stal
    dom[hrac][homespace[hrac][0]] = hraci[hrac][0]         #prepis pozicie v domceku
    homespace[hrac][0] -= 1                                 #odcitanie posledneho volneho miesta 
    print_sachovnica(gensachovnica(n))
    spawn[hrac][aktual_panak][1] = "D"                      #ulozeine pozicie
    print(spawn)

def vyhadzovanie_classic(hrac,hraci,hod,pouzivana_pozicia,spawn,dostupny_panaci,aktual_panak,vyhod,home_B): #vyhadzovanie panakov
    policka[hod+pouzivana_pozicia] = hraci[hrac][0]             #prepis novej pozicie
    symbol = policka[pouzivana_pozicia]
    if hrac == 0 and spawn[hrac][aktual_panak][1] == 0:
        policka[pouzivana_pozicia] = symbol
    elif hrac == 1 and spawn[hrac][aktual_panak][1] == home_B:
        policka[pouzivana_pozicia] = symbol
    else:
        policka[pouzivana_pozicia] = "*"                          #prepis pozicie kde stal
    for i in range(pocet_panakov):                          #scan panakov od vyhodeneho hraca
        if spawn[vyhod][i][1] == hod+pouzivana_pozicia:
            dostupny_panaci[vyhod].append(i)                    #pridanie panaka do dostupnych
            dostupny_panaci[vyhod].sort()                          #zoradenie
            spawn[vyhod][i][1] = " "                               #prepis pozicie vyhodeneho
            print("Vyhodil si panacika hracovi ",hraci[vyhod][0])
            print_sachovnica(gensachovnica(n))
            pouzivana_pozicia = pouzivana_pozicia+hod
            spawn[hrac][aktual_panak][1] = pouzivana_pozicia        #prepis pozicie panaka ktory ho vyhodil
            print(spawn)

def vyhadzovanie_prelom(x,hrac,hraci,pouzivana_pozicia,hod,dostupny_panaci,spawn,aktual_panak): #vyhadzovanie panakov pre hraca B cez koniec/zaciatok sachovnice
    policka[x] = hraci[hrac][0]                                                                 #(princip rovanky ako pri klasickom vyhadzovanie + vypocet novej suradnice x 
    policka[pouzivana_pozicia] = "*"                                                            # kedze musime ist od zaciatku sachovnice)
    for i in range(pocet_panakov):
        if spawn[0][i][1] == hod+pouzivana_pozicia:
            dostupny_panaci[0].append(i)
            dostupny_panaci[0].sort()
            spawn[0][i][1] = " "
            print("Vyhodil si panacika hracovi ",hraci[0][0])
            print_sachovnica(gensachovnica(n))
            pouzivana_pozicia = pouzivana_pozicia+hod
            spawn[hrac][aktual_panak][1] = pouzivana_pozicia
            print(spawn)

def result_A():                         #funkcia vyhry hrac A
    if dom[0] == ["A"]*pocet_panakov:   
        return True
    else:
        return False

def result_B():                         #funkcia vyhry hrac B
    if dom[1] == ["B"]*pocet_panakov:
        return True
    else:
        return  False

def all_moves(f,spawn,hrac,hraci,count,hod,home_B,dostupny_panaci,homespace):  #funkcia vsetkych pohybov 
    if hod == 6: #pripocitanie ak hodi dalsie kolo ide ten isty hrac
         count +=0
    else:
        count +=1   #ak hodi 6< dalsie kolo ide nasledujuci hrac
    while True:
        if type(f[0]) == int:   #scan ci je pomocna premenna f == int() ak ano tak bol vybraty novy panak a ulozia sa pozicie
            aktual_panak = f[0]
            pouzivana_pozicia = spawn[hrac][aktual_panak][1]
            f[0] = ""
        else:                 # ak nie 
            c = 0
            for i in range(pocet_panakov):      #Sken ktory panacik je na hracej ploche
                if type(spawn[hrac][i][1]) == int:      #sken ktory panaci maju ulozenu poziciu == int
                    print(spawn[hrac][i][0])               #vypis jednotlivych panakov
                else:
                    continue 
            vyberhraca = int(input("Zvol cislo panacika ktoreho chces ovladat = ")) #Vyber z panakov
            
            for i in range(pocet_panakov):
                if hraci[hrac][0]+str(vyberhraca) in spawn[hrac][i][0] and type(spawn[hrac][i][1]) == int: #scan ci ten panak je spravny a je na hracej ploche
                    aktual_panak = i                                    #ulozeie panaka a pozicie 
                    pouzivana_pozicia = spawn[hrac][i][1]
                    break                          
                else:
                    c+=1            #ak nie vyberas znova
                    continue
            if c == pocet_panakov:
                continue


        if  home_B > pouzivana_pozicia > 0 and hrac == 1 and home_B - pouzivana_pozicia <=hod:#posun do domceka pre hraca B
            domcek(pouzivana_pozicia,hrac,hraci,spawn,aktual_panak,homespace)
            return count
            

        elif hrac == 1 and pocet_policok-pouzivana_pozicia <= hod: # posun cez sachovnicu poect_policok/0 
            x = hod - (pocet_policok-pouzivana_pozicia) #vypocet novej pozicie 

            if policka[x] == hraci[hrac][0]:         #ak na novej pozicii uz hrac panaka ma
                continue      

            elif policka[x] == "A":                                 #pokial tam je hrac A vyhodis ho
                vyhadzovanie_prelom(x,hrac,hraci,pouzivana_pozicia,hod,dostupny_panaci,spawn,aktual_panak)
            else:                                   #pokial nie klasicky posun 
                basicmove_prelom(pouzivana_pozicia,hraci,hrac,aktual_panak,spawn,x)
                return count
            
        elif pocet_policok-pouzivana_pozicia <= hod:  #posun do domceka hrac A
            
                domcek(pouzivana_pozicia,hrac,hraci,spawn,aktual_panak,homespace)
                return count

        else:           ##### KLASICKE POSUVNAIE / VYHADZOVANIE
            if policka[hod+pouzivana_pozicia] == hraci[hrac][0]:    #AK MAS PANAKA HADZES ZAS
                print("Na tomto policku uz mas panaka")
                continue

            else:
                if hrac == 0 and policka[hod+pouzivana_pozicia] == "B": # vyhadzovanie hrac A vyhadzuje B
                    vyhod = 1
                    vyhadzovanie_classic(hrac,hraci,hod,pouzivana_pozicia,spawn,dostupny_panaci,aktual_panak,vyhod,home_B)
                    return count
                elif hrac == 1 and policka[hod+pouzivana_pozicia] == "A":   #vyhadzuje hrac B hraca A
                    vyhod = 0
                    vyhadzovanie_classic(hrac,hraci,hod,pouzivana_pozicia,spawn,dostupny_panaci,aktual_panak,vyhod,home_B)
                    return count
                else:
                    basicmove(pouzivana_pozicia,hod,hraci,hrac,spawn,aktual_panak,home_B)
                    return count

def game():
    spawn_A = [[" "for i in range(2)]for j in range(pocet_panakov)]  #vytvorenie spawnu s poziciami hrac A
    for i in range(pocet_panakov):
        spawn_A[i][0] = "A"+str(i)

    spawn_B = [[" "for i in range(2)]for j in range(pocet_panakov)] # vytvorenie spawnu s poziciami hrac B
    for i in range(pocet_panakov):
        spawn_B[i][0] = "B"+str(i)
    spawn = []
    spawn.append(spawn_A),spawn.append(spawn_B) #spojenie spawnov dokopy
    hraci = [["A"],["B"]]        #hraci
    vyhod = 0   #pomocna premenna pri vyhadzovanie
    dostupny_panaci = [[i for i in range(pocet_panakov)]for i in range(2)] #list s dostupnymi panakmi
    home_B = int((pocet_policok/2)) #vypocet startu hrac v
    pouzivana_pozicia = 0   #pommocna premenna pre pouzivanu poziciu
    aktual_panak = 0    #pomocna premenna pre katualneho panaka
    count = 0 #pocita kola
    z = 0 #counter pri starte 3x hod
    c = 0 #counter pri zlom vybrati panacika
    f = [""]    #pomocna premanna
    homespace = [[pocet_panakov-1],[pocet_panakov-1]] #list s volnymi poziciami v dome
    while True:
        if count%2 == 0:    #urcovanie ktory hrac je na rade
            hrac = 0
        else:
            hrac = 1
    #podmienky ktory hrac vyhral
        if result_A() == True:
            print("Vitaz je hrac A")
            break
        if result_B() == True:
            print("Vitaz je hrac B")
            break

        print("Na rade je hrac",hraci[hrac][0])
        hod = dice_throw()
        print("Hodil si cislo = ",hod)

        if hraci[hrac][0] not in policka and f == [""] :  #pokial nie je ziadny panacik v sachovnici a premenna f je prazdna
            if hod !=6:
                z+=1
                if z == 3 : # ak 3x nehodis 6 na zaciaktku ide druhy hrac
                    count +=1
                    z= 0
                    continue
                continue
                
            elif hod == 6: #ked hodis 6
                z = 0
                if hrac == 0 :
                    start_player_A(spawn,hrac,dostupny_panaci,f) 
                    continue
                else:
                    start_player_B(spawn,hrac,dostupny_panaci,f)
                    continue
        else: #pri panakovi uz na hracej ploche
            if hod == 6 and f ==[""]: 
                while True:
                    vstup = int(input("Zvol moznost pohybu: 1 - novy, else - pohyb na sachovnici:")) #hodis 6 mozes si vybrat noveho alebo pohyb s panakom
                    if vstup == 1:  #volba noveho panaka
                        if dostupny_panaci[hrac] == []:
                            print("Uz nemas volneho panacika!!!!!") #uz nemas volneho panacika
                            continue
                        else: # funkcie noveho panaka
                            if hrac == 0:
                                start_player_A(spawn,hrac,dostupny_panaci,f)
                                break
                            elif hrac == 1:
                                start_player_B(spawn,hrac,dostupny_panaci,f)
                                break          
                    else:  #Vyber panaka, ktoreho s ktorym sa budes pohybavat
                        count = all_moves(f,spawn,hrac,hraci,count,hod,home_B,dostupny_panaci,homespace) #pohyb po sachovnici    
                        break
            elif hod <=6:       # posuny panakov ked hodim cislo menej ako 6
                count = all_moves(f,spawn,hrac,hraci,count,hod,home_B,dostupny_panaci,homespace) #pohyb po sachovnici


print_sachovnica(gensachovnica(n))
game()