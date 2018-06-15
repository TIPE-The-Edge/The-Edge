import os
import pickle
import platform

class Save():

    def __init__(self):

        self.individus    = []
        self.produits     = []
        self.operations   = []
        self.materiaux    = []
        self.formations   = []
        self.populations  = []
        self.fournisseurs = []
        self.machines     = []
        self.transports   = []
        self.stocks       = []
        self.candidats    = []
        self.departs      = []
        self.couts        = []
        self.magasin      = []

        self.depenses = []
        self.projets = []
        self.produits = []

        self.temps = None
        self.lesRH = None
        self.month = 1
        self.argent = 0

        self.donneesF = {}
        self.listePret = []

        self.sha = ''
        self.user_name = ''
        self.date_creation = None
        self.total_time = 0
        self.last_used = None

        self.notifications = []


    def save(self, window):

        for attr, value in self.__dict__.items():
            setattr(self, attr, getattr(window, attr))

        self.total_time = window.total_time + window.time_used

        with open('./save/' + window.sha, 'wb') as f:
            pickle.dump(self, f)

    def load(self, window, file):

        with open('./save/' + file, 'rb') as f:
            save = pickle.load(f)

        # FIXME: reference problem
        for attr, value in save.__dict__.items():
            setattr(window, attr, getattr(save, attr))

    def isSaved(self, window):
        # FIXME: pls
        # with open('./save/' + window.sha, 'rb') as f:
        #     save = pickle.load(f)
        #
        # for attr, value in save.__dict__.items():
        #     if value != getattr(window, attr):
        #         print(attr)
        #         print(value, getattr(window, attr))
        #         return False
        return True

    def getSave(self, file):
        with open('./save/' + file, 'rb') as f:
            save = pickle.load(f)

        return save

    def getSaves(self):
        if platform.system() == 'Windows':
            os.system('dir .\\save\\* /b > savelist.txt')
        else:
            os.system('ls ./save/* > savelist.txt')

        f = open("savelist.txt", "r")
        tab_f = f.readlines()
        tab_save_info = []
        for i in range(1,len(tab_f)):
            tab_f[i] = tab_f[i][:-1]

            with open('save/' + tab_f[i], 'rb') as f:
                save = pickle.load(f)

            tab_save_info.append([tab_f[i], save.user_name])

        f.close()

        if platform.system() == 'Windows':
            os.system('del .\\savelist.txt')
        else:
            os.system('rm ./savelist.txt')

        return tab_save_info

    def delete(self, file):
        if platform.system() == 'Windows':
            os.system('del .\\save\\' + file)
        else:
            os.system('rm ./save/' + file)
