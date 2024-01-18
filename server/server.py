import crypto.elgamal as elgamal
import random
import os
import json

from uuid import uuid4


msg_invalid_user = {"status" : "Invalid user"}
msg_finger_print = {"status" : "Finger print invalido"}
msg_create_group = {"status" : "Name in use"}

class ControlServer():
    def __init__(self,path="./server/bd.json") -> None:
        self.path = path
        self.load_keys_authentication()
    

    def load_keys_authentication(self):
        if(not os.path.exists(self.path)):
            with open(self.path,"w+") as outfile:
                json.dump({
                    "users":{},
                    "groups":{}
                    },outfile)
                outfile.close()

        with open(self.path,"r") as infile:
            load = json.load(infile)
            infile.close()
        self.keys_authentication = load

    def _save(self):
        with open(self.path,"w+") as outfile:
            json.dump(self.keys_authentication,outfile)
            outfile.close()

    def _verify_send_receive(self, sender, receiver):
        verify_sender = self._verify_user(sender)
        verify_receiver = self._verify_user(receiver)
        verify = (verify_sender) and (verify_receiver)
        return verify
            
    def _verify_user(self,user):
        list_users = list(self.keys_authentication['users'].keys())
        return user in list_users
    
    def _verify_finger_print(self,token,user):
        res = (token == self.keys_authentication['users'][user]['finger_print'])
        return res

    def make_login(self,user_name,public_key):
        verify = self._verify_user(user_name)
        if(verify):
            return msg_invalid_user
        else:
            
            while(True):
                flag = False
                token = str(uuid4())
                for key_ in list(self.keys_authentication['users'].keys()):
                    if(self.keys_authentication['users'][key_]['finger_print'] == token):
                        flag = True
                        break

                if(not flag):
                    break
            
            self.keys_authentication['users'][user_name] = {
                "public_key" : public_key.__dict__,
                "mesages" : {},
                "groups" : {},
                "finger_print" : token
            }
            self._save()
            return {"status" : True,"finger_print":token}
        
    def send_msg(self,sender,receiver, msg,token):
        #list_users = list(self.keys_authentication['users'].keys())
        verify = self._verify_send_receive(sender, receiver)
        if not verify:
            return msg_invalid_user
        else:
            if(not self._verify_finger_print(token,sender)):
            #if(token != self.keys_authentication['users'][sender]['finger_print']):
                return msg_finger_print
            else:
                mesage = self.keys_authentication['users'][receiver]['mesages']
                if(sender in list(mesage.keys())):
                    mesage[sender].append(msg)
                else:
                    mesage[sender] = [msg]

                self._save()
                return {"status" : True}

    
        
    def get_msg(self,receiver,token,who):
        #list_users = list(self.keys_authentication['users'].keys())
        verify_receiver = self._verify_send_receive(receiver,who)
        if(not verify_receiver):
            return msg_invalid_user
        else:
            #if(token != self.keys_authentication['users'][receiver]['finger_print']):
            if(not self._verify_finger_print(token,receiver)):
                return msg_finger_print
            else:
                mesage = self.keys_authentication['users'][receiver]['mesages']
                if(who in list(mesage.keys())):
                    aux = self.keys_authentication['users'][receiver]['mesages'][who].copy()
                    self.keys_authentication['users'][receiver]['mesages'][who] = []
                    self._save()
                    return {"status" : True,"mesages":aux}
                # if(len(mesage) > 0):
                #     aux = mesage.copy()
                #     self.keys_authentication['users'][receiver]['mesages'] = {}
                #     self._save()
                #     return {"status" : True,"mesages":aux}
                else:
                    return {"status" : "No mesages"}
                
    def get_public_key(self,receiver,token,who):
        #list_users = list(self.keys_authentication['users'].keys())
        #if(who not in list_users) and (receiver not in list_users):
        #    return {"status" : False}
        verify = self._verify_send_receive(who, receiver)
        if not verify:
            return msg_invalid_user
        else:
            if(not self._verify_finger_print(token,receiver)):
                return msg_finger_print
            
            else:
                return {"status" : True,"public_key":self.keys_authentication['users'][who]["public_key"]}
            
    def create_group(self,user,token,members,name_group):
        verify = self._verify_user(user)
        for user_ in members:
            verify = verify and self._verify_user(user_)

        if(not verify):
            return msg_invalid_user
        else:
            if(not self._verify_finger_print(token,user)):
                return msg_finger_print
            
            members.append(user)

            flag = False
            for user_ in members:
                if(name_group in list(self.keys_authentication['users'][user_]["groups"].keys())):
                    flag = True
                    break

            if(flag):
                return msg_create_group
            else:
                for user_ in members:
                    self.keys_authentication['users'][user_]["groups"][name_group] = []

                return {"status" : True}

            

            




class Server():
    def __init__(self) -> None:
        self.load_keys_authentication()    

    def receive_request(self,user_name,public_key):
        if(user_name in list(self.keys_authentication.keys())):
            return False
        else:
            number, msg = self._send_random_number(public_key)
            self.keys_authentication[user_name] = {
                "random_number_auth": number,
                "is_authenticated" : False
            }
            return msg
        
    def verify_number(self,user_name,number):
        print(self.keys_authentication)
        if(user_name not in list(self.keys_authentication.keys())):
            return False
        else:
            res = int(self.keys_authentication[user_name]["random_number_auth"]) == int(number)
            if(res):
                del self.keys_authentication[user_name]['random_number_auth']
                self.keys_authentication[user_name]["is_authenticated"] = True
                self.keys_authentication[user_name]["mesages"] = {}
                
            return res

    def is_msg(self,user_name):
        if(user_name not in list(self.keys_authentication.keys())):
            return False
        else:
            if(self.keys_authentication[user_name]["is_authenticated"]):
                print(self.keys_authentication)
                return self.keys_authentication[user_name]["mesages"]
            else:
                return False

    def _send_random_number(self,public_key):
        number = random.randint(1,10000)
        return number, elgamal.encrypt(public_key, str(number))
