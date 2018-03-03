# -*- coding: utf-8 -*-

import bot_manager    

from bot_manager import (send_message, send_photo, send_location, 
    direct_user_to_state, repeatState, set_user_var_value, get_user_var_value)

#other imports
from utility import import_url_csv
import asd
import re
##############################
# STATES FUNCTIONS
# * each function's name has to start with 'state_X' where X is the name of the state
# * each function is split in two parts: 
#   - if bot_turn: bot's turn to say something
#   - else: the user said something
##############################

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
        return False
def controllo_ora(user, valore_ora):
    if ":" in valore_ora:
        split = valore_ora.split(':')
        try:
            int(split[0])
            int(split[1])
            return True
        except:
            return False
    else:
        send_message(user,'Formato non valido')
        return False
def controllo_data(user,valore_data):
    if "-" in valore_data:
        try:
            valore = valore_data.split('/')
            return True
        except:
            return False
    else:
        send_message(user,'Formato non valido')
        return False
        

def state_0(user, message):

    bot_turn = message is None
    if bot_turn:
        registrato = get_user_var_value(user,"REGISTRATO",False)
        if registrato:
            direct_user_to_state(user,'questionario_associazione')
        else:
            direct_user_to_state(user,'registrazione_nome')
    else:
        pass


def state_registrazione_nome(user, message):
    bot_turn = message is None
    if bot_turn:
        reply_text = 'Inserisci il tuo Nome e Cognome :'
        send_message(user, reply_text)
    else:
        if message.text:
            input_text = message.text
            set_user_var_value(user,'NOMECOGNOME',input_text)
            direct_user_to_state(user,'registrazione_email')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_registrazione_email(user, message):
    bot_turn = message is None
    if bot_turn:
        reply_text = 'Inserisci la tua email :'
        send_message(user, reply_text)
    else:
        if message.text:
            input_text = message.text            
            if validateEmail(input_text):
                bot_manager.set_user_var_value(user,'EMAIL',input_text)
                direct_user_to_state(user,'registrazione_codice_fiscale')
            else:
                reply_text = "Indirizzo email non valido!"
                send_message(user, reply_text)
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_registrazione_codice_fiscale(user, message):
    bot_turn = message is None
    if bot_turn:
        reply_text = 'Inserisci il tuo codice fiscale :'
        send_message(user, reply_text)
    else:
        if message.text:
            input_text = message.text
            bot_manager.set_user_var_value(user,'CODF',input_text)
            set_user_var_value(user,"REGISTRATO",True)
            direct_user_to_state(user,'0')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_questionario_associazione(user, message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Fai parte di un'associazione ? "
        keyboard = [['SI','NO']]
        send_message(user, reply_text,keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == "SI":
                direct_user_to_state(user,'dati_associazione')
            elif input_text == "NO":
                direct_user_to_state(user,'autorizzazione_dati')
            else:
                reply_text = 'Input non riconosciuto, usa la tastiera.'
                send_message(user, reply_text)           
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_dati_associazione(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Inserisci il nome dell'associazione : "
        send_message(user,reply_text)
    else:
        if message.text:
            input_text = message.text
            set_user_var_value(user,'NOME_ASSOCIAZIONE',input_text)
            direct_user_to_state(user,'dati_ruolo') 
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_dati_ruolo(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Inserisci il tuo ruolo : "
        send_message(user,reply_text)
    else:
        if message.text:
            input_text = message.text
            set_user_var_value(user,'RUOLO',input_text) 
            direct_user_to_state(user,'autorizzazione_dati')  
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_autorizzazione_dati(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Autorizzo il trattamento dei miei dati personali ai sensi del Decreto Legislativo 30 giugno 2003, n. 196 “Codice in materia di protezione dei dati personali”"
        keyboard = [['Confermo']]
        send_message(user,reply_text,keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == "Confermo":             
                direct_user_to_state(user,'scelte_utente')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_scelte_utente(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Cosa desideri fare? "
        keyboard = [['Organizzare un evento'],['Partecipare ad un evento']]
        send_message(user,reply_text,keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == "Organizzare un evento":
                direct_user_to_state(user,'luogo')
            elif input_text == "Partecipare ad un evento":
                send_message(user, input_text)
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_luogo(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Dove?"
        keyboard = [['In una sala/struttura comunale'],['In un luogo pubblico']]
        send_message(user,reply_text,keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == "In una sala/struttura comunale":
                direct_user_to_state(user,'evento_scelto')
            elif input_text == "In un luogo pubblico":
                send_message(user, input_text)
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)


def state_evento_scelto(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Che tipo di evento vuoi organizzare? (es. festa privata, assemblea, attività sportiva...)"
        send_message(user,reply_text)
    else:
        if message.text:
            input_text = message.text
            set_user_var_value(user,'TIPO_EVENTO_SCELTO',input_text)
            direct_user_to_state(user,'tipo_struttura')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_tipo_struttura(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "In base a cosa vuoi cercare la struttura?"
        keyboard = [['Data/Ora'],['Lista delle strutture']]
        send_message(user,reply_text,keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == "Data/Ora":
                direct_user_to_state(user,'data')
            elif input_text == "Lista delle strutture":
                direct_user_to_state(user,'lista_strutture')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_lista_strutture(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Inserisci data  [gg-mm-aaaa]"
        send_message(user,reply_text)
    else:
        if message.text:
            input_text = message.text
            if controllo_data(user,input_text):
                set_user_var_value(user,'DATA',input_text)
                direct_user_to_state(user,'lista_strutture_ORE')
            else:
                direct_user_to_state(user,'lista_strutture')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_lista_strutture_ORE(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Inserisci ora iniziale per la ricerca [00:00]"
        send_message(user,reply_text)
    else:
        if message.text:
            input_text = message.text
            if controllo_ora(user, input_text):
                set_user_var_value(user,'DATA_RICERCA_STRUTTURA',input_text)
                direct_user_to_state(user,'lista_strutture_ORE_finale')
            else:
                direct_user_to_state(user,'lista_strutture_ORE')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_lista_strutture_ORE_finale(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Inserisci ora finale per la ricerca [00:00]"
        send_message(user,reply_text)
    else:
        if message.text:
            input_text = message.text
            if controllo_ora(user, input_text):
                
                oraInizialeRicerca = get_user_var_value(user,'DATA_RICERCA_STRUTTURA',None)
                oraFinaleRicerca = input_text
                send_message(user,'Sto elaborando la richiesta...')
                vettoreFull = asd.ricerca_valori_dati_iniziali(oraInizialeRicerca,oraFinaleRicerca)
                messaggio = ""
                stanze_giorno_str = ""     
                for stanze_giorno in vettoreFull:        
                    try:
                        valore_data = str.split('/')
                        invio = "Data " + stanze_giorno
                        send_message(user,invio)
                    except:
                        stanze_giorno_str = ", ".join(stanze_giorno) + "\n\n"
                    if len(messaggio) > 1000:
                        send_message(user,messaggio)
                        messaggio = ""
                    messaggio += stanze_giorno_str
                if len(messaggio) > 0:             
                    send_message(user,messaggio)
                direct_user_to_state(user,'prendi_seconda_data')
            else:
                direct_user_to_state(user,'lista_strutture_ORE_finale')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_prendi_seconda_data(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Inserisci data per selezionare la stanza [gg-mm-aaaa]"
        send_message(user,reply_text)
    else:
        if message.text:
            input_text = message.text
            if controllo_data(user,input_text):
                set_user_var_value(user,'DATA_NUMERO_DUE',input_text)
                direct_user_to_state(user,'prendi_secondo_indice')
            else:
                direct_user_to_state(user,'prendi_seconda_data')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_prendi_secondo_indice(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Inserisci indice per la stanza desiderata:"
        send_message(user,reply_text)
    else:
        if message.text:
            input_text = message.text
            set_user_var_value(user,'DATA_INDICE_DUE',input_text)

        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_seconda_conferma(user,message):
    bot_turn = message is None
    stanza_scelta = get_user_var_value(user,'DATA_NUMERO_DUE',None)
    numero_stanza = get_user_var_value(user,'DATA_INDICE_DUE',None)

    if bot_turn:
        reply_text = "Confermi di voler prenotare la stanza numero {} per il giorno {} ?:".format(numero_stanza,stanza_scelta)
        keyboard = [['SI'],['NO']]
        send_message(user,reply_text,keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == "SI":
                pass
            else:
                pass
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)


def state_data(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Inserisci data  [gg-mm-aaaa]"
        send_message(user,reply_text)
    else:
        if message.text:
            input_text = message.text
            if controllo_data(user,input_text):              
                set_user_var_value(user,'DATA',input_text)
                direct_user_to_state(user,'ora_inizio')
            else:
                direct_user_to_state(user,'data')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_ora_inizio(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Inserisci ora di inizio [00:00]"
        send_message(user,reply_text) 
    else:
        if message.text:
            input_text = message.text
            if controllo_ora(user, input_text):
                set_user_var_value(user,'ORA_INIZIO',input_text)
                direct_user_to_state(user,'ora_fine')
            else:
                direct_user_to_state(user,'ora_inizio')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_ora_fine(user,message):
    bot_turn = message is None
    if bot_turn:    
        reply_text = "Inserisci ora di fine [00:00]"
        send_message(user,reply_text)
    else:
        if message.text:
            input_text = message.text
            if controllo_ora(user, input_text):
                set_user_var_value(user,'ORA_FINE',input_text)
                direct_user_to_state(user,'call_metodo')
            else:
                direct_user_to_state(user,'ora_fine')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_call_metodo(user,message):
    data = get_user_var_value(user,'DATA',None)
    ora = get_user_var_value(user,'ORA_INIZIO',None)
    oraFine = get_user_var_value(user,'ORA_FINE',None)

    dati = asd.ritorna_date(data,ora,oraFine)
    send_message(user,dati)
    if len(dati) > 0:      
        direct_user_to_state(user,'input_scelto')
        set_user_var_value(user,'VETTORE_DATI',dati)
    else:
        send_message(user,"DATI NON PRESENTI ")

def state_input_scelto(user,message):
    bot_turn = message is None
    if bot_turn:    
        reply_text = "Inserisci il numero della struttura che vuoi prenotare:"
        send_message(user,reply_text)
    else:
        if message.text:
            input_text = int(message.text)
            set_user_var_value(user,'POS_SELEZ',input_text)
            direct_user_to_state(user,'conferma_input')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_conferma_input(user,message):
    bot_turn = message is None
    posizioneScelta = get_user_var_value(user,'VETTORE_DATI',None)
    data = get_user_var_value(user,'DATA',None)
    gg = get_user_var_value(user,'POS_SELEZ',None)
    posizioneScelta = posizioneScelta[gg]
    oreA = get_user_var_value(user,'ORA_INIZIO',None)
    oreB = get_user_var_value(user,'ORA_FINE',None)

    if bot_turn:
        reply_text = "Confermi di voler prenotare la stanza {} per il giorno {} dalle ore {} alle ore {}:".format(posizioneScelta,data,oreA,oreB)
        keyboard = [['SI'],['NO']]
        send_message(user,reply_text,keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == "SI":
                direct_user_to_state(user,'valida_mail')
            else:
                send_message(user,'Ti faccio rinserire i dati')
                direct_user_to_state(user,'data')
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)


def state_valida_mail(user,message):
    reply_text = "Entro due giorni riceverai la conferma da parte dell'ufficio via email"
    send_message(user,reply_text)
    reply_text = "Inoltre sarà presente il link per modificare o annullare l'evento"
    send_message(user,reply_text)
    direct_user_to_state(user,'patrocinio')

def state_patrocinio(user,message):
    bot_turn = message is None
    if bot_turn:
        reply_text = "Vuoi che l'evento venga patrocinato dal comune di Ville d'Anaunia"
        keyboard = [['SI', 'NO']]
        send_message(user,reply_text, keyboard)
    else:        
        direct_user_to_state(user,'pubblicità')

def state_pubblicità(user,message):
    bot_turn = message is None
    if bot_turn:
        testo = "https://www.facebook.com/comune.ville.danaunia/?ref=page_internal"    
        reply_text = "Vuoi che l'evento venga pubblicizzato sulla pagina Facebook del comune?"
        keyboard = [['SI', 'NO']]
        send_message(user,reply_text, keyboard)
        send_message(user,testo)
    else:
        reply_text = "Seconda parte in sviluppo"
        send_message(user,reply_text)




if __name__ == '__main__':
    bot_manager.startBot()