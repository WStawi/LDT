from __future__ import division
from __future__ import print_function
from psychopy import visual, core, event, gui
from builtins import range
from typing import List, Dict
from os.path import join
import csv
import numpy
import os
import yaml
import random
import atexit
import codecs

paryZgodne = dict(yellow=["pisklak", "cytryna", "kukurydza", "ser", "banan", "żonkil"],
                  red=["krew", "mak", "pomidor", "truskawka", "róża", "biedronka", "serce"],
                  green=["trawa", "liść", "awokado", "żaba", "mech", "oliwka", "kaktus", "glon", "szmaragd"],
                  cyan=["morze", "niebo", "jagoda", "smerfy", "niezapominajka", "dżins", "szafir"],
                  orange=["pomarańcza", "marchew", "tygrys", "dynia", "lis", "wiewiórka", "batat"],
                  purple=["bakłażan", "śliwka", "fiołek", "winogrona", "wrzos"],
                  pink=["świnia", "flaming", "łosoś", "malina"])

paryNiezgodne = dict(red=["sałata", "groszek", "lazuryt", "bursztyn", "kurkuma"],
                     yellow=["mięso", "bocian", "bambus", "poziomka", "srebro"],
                     purple=["papaja", "czekolada", "zebra", "słońce"],
                     pink=["marchew", "papryka", "dąb", "kości", "dziobak"],
                     green=["drewno", "lawenda", "prosiak", "mysz", "śnieg"],
                     cyan=["lis", "morela", "złoto", "skała", "jeż"],
                     orange=["czosnek", "świerk", "kapusta", "śmietana", "płetwal"])

paryNeutralne = dict(gray=["powietrze", "deszcz", "spotkanie", "neutralność", "podróż", "sesja",
                           "wakacje", "praca", "kawiarnia", "komputer", "zajęcie",
                           "walka", "dokument", "muzyka", "kropka", "kwadrat",
                           "piosenkarz", "piasek", "asfalt", "sok", "woda", "ruch",
                           "modliszka", "kwiat", "diament", "rubin"])

nParyZgodne = dict(yellow=["pisklok", "cjtryna", "kukorydza", "bunan", "słeńce", "kurkoma"],
                   red=["krcw", "mok", "pcmidcr", "grajfrut", "wuśnia"],
                   cyan=["dźinsy", "jegoda", "niezopaminajka", "niobo", "szefir"],
                   purple=["bakżałan", "fejołek", "lewenda", "winogrino", "ślawki"],
                   orange=["pomarararcz", "marchaw", "tugryz", "weiwórka", "orungatan"],
                   green=["awakodo", "wadorost", "kaktas", "papratka", "emarald"],
                   pink=["fleming", "presię", "maliaa", "łośos", "akoslolt"])

nParyNiezgodne = dict(red=["sałota", "canymen", "głoąb", "złato", "sasna"],
                      green=["drawno", "karw", "orungotan", "mniaszek", "popraka"],
                      cyan=["ljs", "sarce", "marole", "lyść", "cytrina"],
                      pink=["bursasztyn", "oilwa", "sołńec", "kupasta", "słań"],
                      yellow=["morzc", "loas", "fiołołki", "dziabok", "rzaka"],
                      orange=["lewanda", "jaziora", "szemragd", "akawodo", "akosolt"],
                      purple=["aloas", "lwicia", "dzikik", "piaisek", "zieimia"], )

nParyNeutralne = dict(gray=["trskawka", "frawa", "niedo", "wajna", "nautrolność", "poweitreze",
                            "kołkó", "hynmn", "wimpar", "dzeici", "prezsałnki", "filozafia",
                            "wcda", "bakżałan", "mcucha", "stokratka", "ruibin", "srobro", ])


odp = 0
sesjaTest = 15
sesjeEksp = 20
random.seed()
poprSlowa = ["paryZgodne", "paryNiezgodne", "paryNeutralne"]
niepoprSlowa = ["nParyZgodne", "nParyNiezgodne", "nParyNeutralne"]
Slowa = ["poprSlowa", "niepoprSlowa"]

def check_exit(key='f9'):
    stop = event.getKeys(keyList=[key])
    if len(stop) > 0:
        exit(1)

def get_participant_id():
    participant_info = dict()
    participant_info['participant_id'] = ''
    participant_info['plec'] = 'mezczyzna', 'kobieta'
    participant_info['wiek'] = ''
    dlg = gui.DlgFromDict(participant_info)
    if not dlg.OK:
        core.quit()
    return participant_info['participant_id'], participant_info['plec'], participant_info['wiek']


participant_id = get_participant_id()
with open(join('c:\LDT\daneRejestrowane.txt'), mode='a') as f:
    for v in participant_id:
        f.write(v + ",")
with open(join('c:\LDT\daneRejestrowane.txt'), mode='a') as f:
    f.write("\n")

win = visual.Window(size=(1920, 1080), color='#8B8989', fullscr=True, units='cm', monitor='testMonitor', screen=0)
mouse = event.Mouse(visible=False)
clock = core.Clock()

msgPrzerwa = visual.TextStim(win, text="Trwa przerwa.\nNaciśnij klawisz Spacji, aby rozpocząć kolejny etap.", font='Arial', color='black', pos=(0, 0))
msgspace = visual.TextStim(win, text="Aby przejść dalej naciśnij klawisz Spacji.", font='Arial', color='#BDBDBD', pos=(0, -10))
msg1 = visual.TextBox2(win, text="Za chwilę wyświetli się instrukcja.", font='Arial', letterHeight=1, color='black', pos=(0, 0), alignment='center')
msg2 = visual.TextBox2(win, text="W zadaniu, które będziesz wykonywać, w jasnoszarym prostokącie na środku ekranu będą pojawiać się słowa w języku polskim oraz zestawy liter, które nie są słowami. Kolor tła będzie się zmieniał. Twoim zadaniem będzie ocenienie, czy bodziec jest istniejącym słowem w języku polskim, czy nie.", font='Arial', letterHeight=1, color='black', pos=(0, 0), alignment='center')
msg3 = visual.TextBox2(win, text='Na prawdziwe słowa reaguj klawiszem prawego Ctrl, a na fałszywe klawiszem lewego Ctrl.\n\nAby usprawnić reakcję trzymaj palec wskazujący lewej ręki na klawiszu lewego Ctrl, a prawej ręki na klawiszu prawego Ctrl.', font='Arial', letterHeight=1, color='black', pos=(0, -0.2), alignment='center')
msg4 = visual.TextBox2(win, text="Staraj się odpowiadać szybko, gdyż czas Twojej odpowiedzi będzie mierzony.\n\nPamiętaj przy tym o poprawności.", font='Arial', letterHeight=1, color='black', pos=(0, -0.2), alignment='center')
msg5 = visual.TextBox2(win, text="Aby oswoić się z regułami badania pierwsza sesja, którą wykonasz będzie treningowa i nie zostanie poddana analizie.\nPo sesji treningowej nastąpi przerwa, którą możesz zakończyć klawiszem Spacji.\nWówczas rozpocznie się właściwa część badania, która będzie składała się z czterech części przedzielonych przerwami.\nSygnałem zakończenia całego badania będzie napis KONIEC.", font='Arial', letterHeight=1, color='black', pos=(0, -0.2), alignment='center')
msg6 = visual.TextBox2(win, text="Aby rozpocząć sesję treningową naciśnij klawisz Spacji.", font='Arial', letterHeight=1, color='black', pos=(0, -0.2), alignment='center')
msgTest = visual.TextStim(win, text="Właśnie rozpoczynasz sesję treningową.", font='Arial', color='black', pos=(0, 0))

def spacja():
    key = event.waitKeys(keyList=['space'])
    if key == ['space']:
        core.quit

def instrukcja(wiadomosc):
    wiadomosc.draw()
    msgspace.draw()
    win.flip()
    spacja()

instrukcja(msg1)
instrukcja(msg2)
instrukcja(msg3)
instrukcja(msg4)
instrukcja(msg5)

nr = 0
msg6.draw()
win.flip()
key = event.waitKeys(keyList=['space'])
if key == ['space']:
    win.setColor('#8B8989')
    win.flip()
    msgTest.draw()
    win.flip()
    core.wait(5)
    for y in range(sesjaTest):
        poprBodzca = random.choice(Slowa)
        if poprBodzca == "poprSlowa":
            zgodnosc = dict(niezgodne=paryNiezgodne, zgodne=paryZgodne, neutralne=paryNeutralne)
            kategoria = random.choice(list(zgodnosc))
            kolor = random.choice(list(zgodnosc[kategoria]))
            bodziec = random.choice(zgodnosc[kategoria][kolor])
            text = visual.TextStim(win, text=bodziec, color='black', height=1.5)
            for frame in range(300):
                win.setColor(kolor)
                text.draw()
                l = event.getKeys('lctrl')
                r = event.getKeys('rctrl')
                if len(l) > 0:
                    break
                elif len(r) > 0:
                    break
                win.flip()

        else:
            nZgodnosc = dict(niezgodne=nParyNiezgodne, zgodne=nParyZgodne, neutralne=nParyNeutralne)
            nKategoria = random.choice(list(nZgodnosc))
            nKolor = random.choice(list(nZgodnosc[nKategoria]))
            nBodziec = random.choice(nZgodnosc[nKategoria][nKolor])
            text = visual.TextStim(win, text=nBodziec, color='black', height=1.5)
            for frame in range(300):
                text.draw()
                win.setColor(nKolor)
                l = event.getKeys('lctrl')
                r = event.getKeys('rctrl')
                if len(l) > 0:
                    break
                elif len(r) > 0:
                    break
                win.flip()

    for i in range(4):
        win.setColor('#8B8989')
        win.flip()
        msgPrzerwa.draw()
        win.flip()
        key = event.waitKeys(keyList=['space'])
        if key == ['space']:
            core.quit
        win.flip()
        nr = nr + 1
        msgPoczEtapu = visual.TextStim(win, text=f"Właśnie rozpoczynasz sesję nr {nr}.", font='Arial', color='black', pos=(0, 0))
        msgEtap = visual.TextStim(win, text=f"Sesja {nr}/4", font='Arial', color='white', pos=(0, 11), height=0.7)
        win.setColor('#8B8989')
        win.flip()
        msgPoczEtapu.draw()
        win.flip()
        core.wait(5)

        for x in range(sesjeEksp):
            poprBodzca = random.choice(Slowa)
            if poprBodzca == "poprSlowa":
                with open(join('c:\LDT\daneRejestrowane.txt'), mode='a') as f:
                    f.write("poprawne,")
                zgodnosc = dict(niezgodne=paryNiezgodne, zgodne=paryZgodne, neutralne=paryNeutralne)
                kategoria = random.choice(list(zgodnosc))
                kolor = random.choice(list(zgodnosc[kategoria]))
                bodziec = random.choice(zgodnosc[kategoria][kolor])
                with open(join('c:\LDT\daneRejestrowane.txt'), mode='a') as f:
                    f.write(kategoria + "," + kolor + "," + bodziec + ",")
                text = visual.TextStim(win, text=bodziec, color='black', height=1.5)
                win.callOnFlip(clock.reset)
                for frame in range(300):
                    win.setColor(kolor)
                    text.draw()
                    msgEtap.draw()
                    l = event.getKeys('lctrl')
                    r = event.getKeys('rctrl')
                    if len(l) > 0:
                        rt = clock.getTime()
                        odp = "lctrl"
                        break
                    elif len(r) > 0:
                        rt = clock.getTime()
                        odp = "rctrl"
                        break
                    else:
                        rt = "bd"
                        odp = "bd"
                    win.flip()

                data = str(odp) + "," + str(rt) + "," + "\n"
                with open(join('c:\LDT\daneRejestrowane.txt'), mode='a') as f:
                    f.write(data)

            else:
                with open(join('c:\LDT\daneRejestrowane.txt'), mode='a') as f:
                    f.write("niepoprawne,")
                nZgodnosc = dict(niezgodne=nParyNiezgodne, zgodne=nParyZgodne, neutralne=nParyNeutralne)
                nKategoria = random.choice(list(nZgodnosc))
                nKolor = random.choice(list(nZgodnosc[nKategoria]))
                nBodziec = random.choice(nZgodnosc[nKategoria][nKolor])
                with open(join('c:\LDT\daneRejestrowane.txt'), mode='a') as f:
                    f.write(nKategoria + "," + nKolor + "," + nBodziec + ",")
                text = visual.TextStim(win, text=nBodziec, color='black', height=1.5)
                win.callOnFlip(clock.reset)
                for frame in range(300):
                    text.draw()
                    msgEtap.draw()
                    win.setColor(nKolor)
                    l = event.getKeys('lctrl')
                    r = event.getKeys('rctrl')
                    if len(l) > 0:
                        rt = clock.getTime()
                        odp = "lctrl"
                        break
                    elif len(r) > 0:
                        rt = clock.getTime()
                        odp = "rctrl"
                        break
                    else:
                        rt = "bd"
                        odp = "bd"
                    win.flip()
                data = str(odp) + "," + str(rt) + "," + "\n"
                with open(join('c:\LDT\daneRejestrowane.txt'), mode='a') as f:
                    f.write(data)

with open(join('c:\LDT\daneRejestrowane.txt'), mode='a') as f:
    f.write("\n""\n" "-------------------------------------" "\n" "\n")

win.setColor('#8B8989')
win.flip()
msgEnd = visual.TextStim(win, text="KONIEC\n\nDziękujemy za udział w badaniu.", font='Arial', color='black', pos=(0, 0))
msgEnd.draw()
win.flip()
core.wait(10)
win.close()
core.quit()
