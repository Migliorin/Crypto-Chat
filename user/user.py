import crypto.elgamal as elgamal

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class User():
    def __init__(self,user_name) -> None:
        keys = elgamal.generate_keys()
        self.private_key = keys['privateKey']
        self.public_key = keys['publicKey']
        self.user_name = user_name

        self.know_user = {}
        self.finger_print = None

    def add_know_user(self,user_name,public_key):
        if(user_name in list(self.know_user.keys())):
            return False
        else:
            self.know_user[user_name] = public_key
            return True

    def send_msg(self,user:str,msg:str)->str:
        if(user not in list(self.know_user.keys())):
            return False
        else:
            aux = self.know_user[user]
            if isinstance(aux,dict):
                aux = Struct(**aux)
            return elgamal.encrypt(aux, msg)

    def receive_msg(self,msg_crypto:str)->str:
        return elgamal.decrypt(self.private_key, msg_crypto)