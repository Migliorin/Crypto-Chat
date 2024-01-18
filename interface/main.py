import sys
sys.path.append("/home/lucas/Documentos/Pessoal/Crypto-Chat/")

import PySimpleGUI as sg
from user.user import User
import requests
import threading

import pickle,os

from time import sleep

PATH ='./user_info.pkl'

def save_user_obj(obj):
    with open(PATH,'wb+') as outfile:
        pickle.dump(obj,outfile)
        outfile.close()

def load_pkl():
    if(os.path.exists(PATH)):
        with open(PATH,'rb') as infile:
            load = pickle.load(infile)
            infile.close()
            return load
    else:
        return None

user_name_obj = load_pkl()

def login_window():
    global user_name_obj
    layout = [[sg.Text('Username'),sg.Input(key='-username_login-',size=(10, 1))],
              [sg.Button("OK",button_color=(sg.YELLOWS[0], sg.GREENS[0])),sg.Button("CANCEL",button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

    window = sg.Window('Login Window', layout)
    while(True):
        event, values = window.read()
        if(event == 'OK'):
            user_name = values['-username_login-']
            if(user_name == ''):
                sg.popup("Login Invalido")
            else:
                #window.disappear()
                sg.popup('Creating public and private key and registring','Wait')
                user_name_obj = User(user_name)
                
                
                payload = user_name_obj.public_key.__dict__
                payload.update({"user_name":user_name})
                response = requests.post("http://127.0.0.1:8000/make_login/",json=payload)
                

                response = response.content.decode()
                response = response.replace('true','True').replace('false','False')
                if('True' in response):
                    response = eval(response)
                    user_name_obj.finger_print = response['finger_print']
                    save_user_obj(user_name_obj)
                    sg.popup(f'Status: Sucessefuly created')
                    break
                else:
                    user_name_obj = None
                    response = eval(response)
                    sg.popup(f'Status: {response["status"]}')

                #window.reappear()

        if(event == 'CANCEL'):
            break


    window.close()

def add_new_user():
    global user_name_obj
    layout = [[sg.Text('Username'),sg.Input(key='-username_login-',size=(10, 1))],
              [sg.Button("OK",button_color=(sg.YELLOWS[0], sg.GREENS[0])),sg.Button("CANCEL",button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

    window = sg.Window('Add new user window', layout)

    while(True):
        event, values = window.read()
        if(event == 'OK'):
            user_name = values['-username_login-']
            if(user_name == ''):
                sg.popup("Invalid username")
            else:
                #window.disappear()
                response = requests.get(f"http://127.0.0.1:8000/get_public_key/{user_name}",json={
                    "receiver":user_name_obj.user_name,
                    "token":user_name_obj.finger_print
                    })
                response = response.content.decode()
                response = response.replace('true','True').replace('false','False')
                
                if('True' in response):
                    response = eval(response)
                    sg.popup(response['public_key'])
                    user_name_obj.know_user[user_name] = response['public_key']
                    save_user_obj(user_name_obj)
                    sg.popup(f'Status: Sucessefuly added new user')
                    break
                else:
                    response = eval(response)
                    sg.popup(f'Status: {response["status"]}')

                #window.reappear()

        if(event == 'CANCEL'):
            break


    window.close()



sg.theme('GreenTan') # give our window a spiffy set of colors

menu_def = [['&Menu',['&Login']]]

layout = [[sg.Menu(menu_def, tearoff=True, font='_ 12', key='-MENUBAR-')],
          [sg.Text("Not logged yet",size=(40, 1),key='-LOGIN_STR-')],
          [sg.Text("Know users:"),sg.DropDown('',key='-DROPDOWN-',size=(40, 5),readonly=True,enable_events=True),sg.Text(expand_x=True),sg.Button('Add new User',key='-NEWUSER-',disabled=True)],
          [sg.Output(size=(110, 20), font=('Helvetica 10'),key="-OUTPUT-")],
          [sg.Multiline(size=(70, 5), enter_submits=True, key='-QUERY-', do_not_clear=False),
           sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
           sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

window = sg.Window('Chat window', layout, font=('Helvetica', ' 13'), default_button_element_size=(8,2), use_default_focus=False)


def update_dropdown(user_name_obj, window):
    if(len(user_name_obj.know_user) > 0):
        window['-DROPDOWN-'].update(values=list(user_name_obj.know_user.keys()))

while True:     # The Event Loop
    event, values = window.read()
    if(event in (sg.WIN_CLOSED, 'EXIT')):            # quit if exit button or X
        if(user_name_obj is not None):
            save_user_obj(user_name_obj)
        break
    if((event == 'SEND') and (user_name_obj is not None)):
        if(values['-DROPDOWN-'] != ''):
            query = values['-QUERY-'].rstrip()
            # EXECUTE YOUR COMMAND HERE
            res = user_name_obj.send_msg(values['-DROPDOWN-'],query)
            response = requests.post("http://127.0.0.1:8000/send_msg/",json={
            "sender":user_name_obj.user_name,
            "receiver":values['-DROPDOWN-'],
            "token":user_name_obj.finger_print,
            "msg":res
            })
            window['-OUTPUT-'].update(f"Me: {query}\n",append=True)

            

    if(event == 'Login'):
        if(user_name_obj is not None):
            window['-LOGIN_STR-'].update(f"Login as: {user_name_obj.user_name}")
            update_dropdown(user_name_obj, window)
            window['-NEWUSER-'].update(disabled=False)
            sg.popup('Warning','Login done')
        else:
            login_window()
            #sg.popup(user_name.user_name)
            window['-LOGIN_STR-'].update(f"Login as: {user_name_obj.user_name}")
            update_dropdown(user_name_obj, window)
            window['-NEWUSER-'].update(disabled=False)

    if(event == '-NEWUSER-'):
        add_new_user()
        update_dropdown(user_name_obj, window)

    if((user_name_obj is not None) and (values['-DROPDOWN-'] != '')):
        response = requests.get(f"http://127.0.0.1:8000/get_msg/{values['-DROPDOWN-']}",json={
            "receiver":user_name_obj.user_name,
            "token":user_name_obj.finger_print
        })
        response = response.content.decode()
        response = response.replace('true','True').replace('false','False')
        #sg.popup(response)
        
        if('True' in response):
            response = eval(response)
            mesages = response['mesages']
            #sg.popup(mesages)
            for msg in mesages:
                #sg.popup(msg)
                new_msg = f"{values['-DROPDOWN-']}: {msg}\n"
                window['-OUTPUT-'].update(new_msg,append=True)
            #    
            #    window['-OUTPUT-'].update(str(window['-OUTPUT-'].get()) + new_msg)
    #print(event)
    #print(values)
            
    

window.close()