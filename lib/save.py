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

        self.depenses = []
        self.projets = []
        self.produits = []

        self.temps = None
        self.lesRH = None
        self.month = 0
        self.argent = 0

        self.sha = ''
        self.user_name = ''
        self.date_creation = None
        self.total_time = 0
        self.last_used = None

    def save(self, window):
        self.individus    = window.individus
        self.produits     = window.produits
        self.operations   = window.operations
        self.materiaux    = window.materiaux
        self.formations   = window.formations
        self.populations  = window.populations
        self.fournisseurs = window.fournisseurs
        self.machines     = window.machines
        self.transports   = window.transports
        self.stocks       = window.stocks
        self.candidats    = window.candidats
        self.departs      = window.departs
        self.couts        = window.couts

        self.depenses = window.depenses
        self.projets = window.projets
        self.produits = window.produits

        self.temps = window.temps
        self.lesRH = window.lesRH
        self.month = window.month
        self.argent = window.argent

        self.donneesF = window.donneesF

        self.sha = window.sha
        self.user_name = window.user_name
        self.date_creation = window.date_creation
        self.total_time = window.total_time + window.time_used
        self.last_used = window.last_used

        with open('./save/' + window.sha, 'wb') as f:
            pickle.dump(self, f)

    def load(self, window, file):

        with open('./save/' + file, 'rb') as f:
            self = pickle.load(f)

        window.individus    = self.individus
        window.produits     = self.produits
        window.operations   = self.operations
        window.materiaux    = self.materiaux
        window.formations   = self.formations
        window.populations  = self.populations
        window.fournisseurs = self.fournisseurs
        window.machines     = self.machines
        window.transports   = self.transports
        window.stocks       = self.stocks
        window.candidats    = self.candidats
        window.departs      = self.departs
        window.couts        = self.couts

        window.depenses = self.depenses
        window.projets = self.projets
        window.produits = self.produits

        window.temps = self.temps
        window.lesRH = self.lesRH
        window.month = self.month
        window.argent = self.argent

        window.donneesF = self.donneesF

        window.sha = self.sha
        window.user_name = self.user_name
        window.date_creation = self.date_creation
        window.total_time = self.total_time
        window.last_used = self.last_used

    def isSaved(self, window):
        pass

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
        for i in range(len(tab_f)):
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
