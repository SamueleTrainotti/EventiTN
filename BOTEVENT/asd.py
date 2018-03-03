import urllib.request
import json
import datetime
import calendar
import bot_manager

def ritorna_date(data,ora,oraFine):
    oras = ora.split(":")
    oraFines = oraFine.split(":")
    parametri = "%253D"+data+"*"+oras[0]+"%253A"+oras[1]+"%2526to%253D"+data+"*"+oraFines[0]+"%253A"+oraFines[1]+"%2526%2520%2520"
    contents = json.loads(urllib.request.urlopen("http://www.comune.villedanaunia.tn.it/prenotazioni/openpa/data/booking_sala_pubblica/(availability)/search/?q=from" + parametri).read())
    
    return costruzione_vettore(contents)


def costruzione_vettore(valore_ricerca):
    ritorno = [""] * 15
    ind = 0
    for x in valore_ricerca["locations"]:
        try:
            if x["data"]["ita-IT"]["titolo"] != "":
                    ritorno[ind] =  str(ind) + " " +  x["data"]["ita-IT"]["titolo"]
        except:  
            try:
                if x["data"]["ita-IT"]["name"] != "":
                    ritorno[ind] = str(ind) + " " +  x["data"]["ita-IT"]["name"]
            except:
                pass
        ind = ind + 1 
    return ritorno

def ricerca_valori_dati_iniziali(oraIniziale,oraFinale):
    
    ritorno_dati = [""] * 30
    oraIni = oraIniziale.split(':')
    oraFin = oraFinale.split(':')
    Data = datetime.datetime.now()
    mese = Data.month
    giorno = Data.day
    giorniDisponibili = calendar.monthrange(2018,Data.month)
    Data_ricerca = '-'+str(Data.month)+'-'+str(Data.year)
    diff = giorniDisponibili[1] - giorno 
    indice_giorno = Data.day
    continuo = True 
    ind = 1

    while continuo: 
        if diff != 30:#mese successivo
            while indice_giorno <= giorniDisponibili[1]:
                Data_uso =str(indice_giorno) + Data_ricerca 
                parametri = "%253D"+Data_uso+"*"+oraIni[0]+"%253A"+oraIni[1]+"%2526to%253D"+Data_uso+"*"+oraFin[0]+"%253A"+oraFin[1]+"%2526%2520%2520"
                ritorno_dati[0] = Data_uso
                try:
                    contents = json.loads(urllib.request.urlopen("http://www.comune.villedanaunia.tn.it/prenotazioni/openpa/data/booking_sala_pubblica/(availability)/search/?q=from" + parametri).read())
                    ritorno_dati[ind] = costruzione_vettore(contents)
                    indice_giorno += 1
                except:
                    pass
                ind += 1
     
            mese = Data.month
            valore = ind + 1
            if mese == 12:#caso 1gen   
                giorni = calendar.monthrange(Data.year,1)
                nuovo_padding = giorni[1] - diff 
                while indice_giorno < nuovo_padding:
                    Data_uso = str(indice_giorno) + '-' + str(1) + '-' + str(Data.year)
                    parametri = "%253D"+Data_uso+"*"+oraIni[0]+"%253A"+oraIni[1]+"%2526to%253D"+Data_uso+"*"+oraFin[0]+"%253A"+oraFin[1]+"%2526%2520%2520"
                    try:
                        contents = json.loads(urllib.request.urlopen("http://www.comune.villedanaunia.tn.it/prenotazioni/openpa/data/booking_sala_pubblica/(availability)/search/?q=from" + parametri).read())
                        ritorno_dati[ind] = costruzione_vettore(contents)
                        indice_giorno += 1
                    except:
                        pass
                    ind += 1              
                continuo = False
                return ritorno_dati
            else:
                mese = mese + 1
                giorni = calendar.monthrange(Data.year,mese)
                nuovo_padding = giorni[1] - diff 
                while indice_giorno < nuovo_padding:
                    Data_uso = str(indice_giorno) + '-' + str(1) + '-' + str(Data.year)
                    ritorno_dati[valore] = Data_uso
                    parametri = "%253D"+Data_uso+"*"+oraIni[0]+"%253A"+oraIni[1]+"%2526to%253D"+Data_uso+"*"+oraFin[0]+"%253A"+oraFin[1]+"%2526%2520%2520"
                    contents = json.loads(urllib.request.urlopen("http://www.comune.villedanaunia.tn.it/prenotazioni/openpa/data/booking_sala_pubblica/(availability)/search/?q=from" + parametri).read())
                    ritorno_dati[ind] = costruzione_vettore(contents)
                    indice_giorno += 1
                    ind += 1
                continuo = False
                return ritorno_dati
        else:#mese normale
            while indice_giorno < giorniDisponibili[1]:
                Data_uso = str(indice_giorno) + str(Data_ricerca)
                parametri = "%253D"+Data_uso+"*"+oraIni[0]+"%253A"+oraIni[1]+"%2526to%253D"+Data_uso+"*"+oraFin[0]+"%253A"+oraFin[1]+"%2526%2520%2520"
                try: 
                    contents = json.loads(urllib.request.urlopen("http://www.comune.villedanaunia.tn.it/prenotazioni/openpa/data/booking_sala_pubblica/(availability)/search/?q=from" + parametri).read())
                    ritorno_dati[ind] = costruzione_vettore(contents)
                    indice_giorno += 1
                except:
                    pass
                ind += 1
            continuo = False

    return ritorno_dati