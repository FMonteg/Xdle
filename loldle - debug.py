########## To Do ##############
#
# Complete the database
# Format data
# Test


########## Imports ############

import pandas as pd
import math


########## Classes ############



class Loldle_Game():
    def __init__(self, **kwargs):
        self.states = []
        self.possible = range(kwargs.get("size"))
        self.entropy = 0
        pass

    def update(self, database):
        state = []

        print('Champion proposé :')
        name = input()
        state.append(name)

        print('Genre (r/o/v) :')
        state.append(input())

        print('Rôle (r/o/v) :')
        state.append(input())

        print('Espèce (r/o/v) :')
        state.append(input())

        print('Ressource (r/o/v) :')
        state.append(input())

        print('Portée (r/o/v) :')
        state.append(input())

        print('Régions (r/o/v) :')
        state.append(input())

        print('Année (+/=/-):')
        state.append(input())

        state = tuple(state)
        self.states.append(state)

        remaining=[]
        stats_hint = database.iloc[database[database['Nom'] == name].index[0]]
        for i in self.possible:
            stats_test = database.iloc[i]
            if self.compatible(state[1:], stats_hint, stats_test):
                remaining.append(i)
        self.possible = remaining

        pass

    def compatible(self, hint, stats_hint, stats_test):
        columns_std = ['Genre', 'Rôle', 'Espèce', 'Ressource', 'Type de portée', 'Régions']

        #Compare each characteristic
        for i in range(len(columns_std)):
            T = set(stats_hint[columns_std[i]])
            R = set(stats_test[columns_std[i]])
            if hint[i]=='v' and T!=R:
                return False
            elif hint[i]=='r' and len(set.intersection(T,R))>0:
                return False
            elif hint[i]=='o' and (T==R or len(set.intersection(T,R))==0):
                return False

        
        #Compare year
        if hint[-1]=="=" and stats_hint['Année']!=stats_test['Année']:
            return False
        elif hint[-1]=="+" and stats_hint['Année']>stats_test['Année']:
            return False
        elif hint[-1]=="-" and stats_hint['Année']<stats_test['Année']:
            return False
        
        return True


    def suggest_play(self, database):

        temp = database.iloc[self.possible]
        entropy = pd.Series(index = temp['Nom'].to_list())

        print(self.possible)

        for i in self.possible:
            stats_try = database.iloc[i]


            counts = {}
            for j in self.possible:
                stats_real = database.iloc[j]

                hint = self.compare(stats_try, stats_real)
                counts[hint] = counts.get(hint, 0) + 1
            
            calcul = []
            total = len(self.possible)
            for hint in counts.keys():
                p = counts[hint]/total
                log = math.log(1/p, 2)
                calcul.append(p*log)
            entropy.loc[temp.loc[i,'Nom']] = sum(calcul) + self.entropy

        print("10 entropies les plus élevées :")
        print(entropy.sort_values(ascending=False).head(10))

        self.entropy += entropy.sort_values(ascending=False).iloc[0]
        pass

    def compare(self, test, real):
        hint = []

        columns_std = ['Genre', 'Rôle', 'Espèce', 'Ressource', 'Type de portée', 'Régions']

        #Compare each characteristic
        for col in columns_std:
            T = set(test[col])
            R = set(real[col])
            if T==R:
                hint.append('v')
            elif len(set.intersection(T,R))>0:
                hint.append('o')
            else:
                hint.append('r')

        
        #Compare year
        if test['Année']==real['Année']:
            hint.append('=')
        elif test['Année']>real['Année']:
            hint.append('-')
        else:
            hint.append('+')


        return tuple(hint)



########## Main code ############

pd.set_option('display.max_rows', None)

#On récupère notre base de données
path = __file__[:-17] + "database_lol.csv"
database = pd.read_csv(path)

print(database.shape)
database = database[database['Genre'] != 'Féminin']
print(database.shape)
database = database[database['Type de portée'] == 'Mêlée']
print(database.shape)
database = database[database['Ressource'] != 'Mana']
print(database.shape)
database = database[database['Année'] > 2011]
print(database.shape)

print(database.head(200))


def compatible_test(hint, stats_hint, stats_test):
        columns_std = ['Genre', 'Rôle', 'Espèce', 'Ressource', 'Type de portée', 'Régions']

        #Compare each characteristic
        for i in range(len(columns_std)):
            T = set(stats_hint[columns_std[i]])
            R = set(stats_test[columns_std[i]])
            if hint[i]=='v' and T!=R:
                return (False, columns_std[i])
            elif hint[i]=='r' and len(set.intersection(T,R))>0:
                return (False, columns_std[i])
            elif hint[i]=='o' and (T==R or len(set.intersection(T,R))==0):
                return (False, columns_std[i])
        
        #Compare year
        if hint[-1]=="=" and stats_hint['Année']!=stats_test['Année']:
            return (False, 'Année')
        elif hint[-1]=="+" and stats_hint['Année']>stats_test['Année']:
            return (False, 'Année')
        elif hint[-1]=="-" and stats_hint['Année']<stats_test['Année']:
            return (False, 'Année')
        
        return (True, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

stats_hint = database.iloc[database[database['Nom'] == 'Vayne'].index[0]]

hint = ['r', 'o', 'o', 'r', 'r', 'r', '+']
for name in database['Nom']:
    print(name)
    stats_test = database.iloc[database[database['Nom'] == name].index[0]]
    print(compatible_test(hint, stats_hint, stats_test))