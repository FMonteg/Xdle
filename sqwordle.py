########## Imports ############

import pandas as pd
import math



########## Classes ############

class Sqwordle_Game():
    def __init__(self, **kwargs):
        self.states = []
        self.possible = range(151)
        pass

    def update(self, pokedex):
        state = []

        print('Pokemon tried:')
        name = input()
        state.append(name)

        print('First type (y/n):')
        state.append(input())

        if not pd.isna(pokedex[pokedex['name']==name]['type2'].iloc[0]):
            print('Second type (y/n):')
            state.append(input())
        else:
            state.append('')
        
        print('Evolution Chain (y/n):')
        state.append(input())

        print('Attack (+/-/=):')
        state.append(input())

        print('Defense (+/-/=):')
        state.append(input())

        print('Height (+/-/=):')
        state.append(input())

        print('Weight (+/-/=):')
        state.append(input())

        state = tuple(state)
        self.states.append(state)

        remaining=[]
        stats_hint = pokedex.iloc[pokedex[pokedex['name'] == name].index[0]]
        for i in self.possible:
            stats_test = pokedex.iloc[i]
            if self.compatible(state, stats_hint, stats_test):
                remaining.append(i)
        self.possible = remaining
        pass

    def compatible(self, hint, stats_hint, stats_test):
        #Compare EvC
        if hint[3] == 'y' and stats_hint['EvC']!=stats_test['EvC']:
            return False
        elif hint[3] == 'n' and stats_hint['EvC']==stats_test['EvC']:
            return False


        #Compare types
        if hint[1] == 'y' and (stats_hint['type1']!=stats_test['type1'] and stats_hint['type1']!=stats_test['type2']): 
            return False 
        elif hint[1] == 'n' and (stats_hint['type1']==stats_test['type1'] or stats_hint['type1']==stats_test['type2']):
            return False
        if hint[2] == 'y' and (stats_hint['type2']!=stats_test['type1'] and stats_hint['type1']!=stats_test['type2']): 
            return False
        elif hint[2] == 'n' and (stats_hint['type2']==stats_test['type1'] or stats_hint['type1']==stats_test['type2']):
            return False


        #Compare stats
        stats_name = ['attack', 'defense', 'height_m', 'weight_kg']
        for i in range(4):
            if hint[i+4] == '=' and stats_hint[stats_name[i]]!=stats_test[stats_name[i]]: 
                return False
            elif hint[i+4] == '+' and stats_hint[stats_name[i]]>=stats_test[stats_name[i]]: 
                return False
            elif hint[i+4] == '-' and stats_hint[stats_name[i]]<=stats_test[stats_name[i]]: 
                return False
            
            
        return True


    def suggest_play(self, pokedex):

        temp = pokedex.iloc[self.possible]
        entropy = pd.Series(index = temp['name'].to_list())
        for i in self.possible:
            stats_try = pokedex.iloc[i]


            counts = {}
            for j in self.possible:
                stats_real = pokedex.iloc[j]

                hint = self.compare(stats_try, stats_real)
                counts[hint] = counts.get(hint, 0) + 1
            
            calc = []
            total = len(self.possible)
            for hint in counts.keys():
                p = counts[hint]/total
                log = math.log(1/p, 2)
                calc.append(p*log)
            entropy[i] = sum(calc)

        print("10 entropies les plus élevées :")
        print(entropy.sort_values(ascending=False).head(10))
        pass

    def compare(self, test, real):
        hint = []

        #Compare type 1
        if test['type1']==real['type1'] or test['type1']==real['type2']:
            hint.append('y')
        else:
            hint.append('n')

        
        #Compare type 2
        if pd.isna(test['type2']):
            hint.append('')
        elif test['type2']==real['type1'] or test['type1']==real['type2']:
            hint.append('y')
        else:
            hint.append('n')


        #Compare Evolution Chain
        if test['EvC']==real['EvC']:
            hint.append('y')
        else:
            hint.append('n')

        
        #Compare stats
        stats_name = ['attack', 'defense', 'height_m', 'weight_kg']
        for i in range(4):
            if test[stats_name[i]]==real[stats_name[i]]:
                hint.append('=')
            elif test[stats_name[i]]>real[stats_name[i]]:
                hint.append('-')
            else:
                hint.append('+')


        return tuple(hint)



########## Main code ############

#On récupère notre base de données
path = __file__[:-11] + "pokedex.csv"
pokedex = pd.read_csv(path)


if False:
    game = Sqwordle_Game()
    test1 = pokedex.iloc[72]
    hint = tuple(['Tentacruel', 'n','y','n','+','+','-','+'])
    test2 = pokedex.iloc[33]
    print(test1)
    print(hint)
    print(test2)
    X = game.compatible(hint,test1,test2)
    print(X)


if True:
    game = Sqwordle_Game()
    play = True
    while play:
        game.suggest_play(pokedex)
        game.update(pokedex)
        print("Keep playing? (y/n)")
        temp = input()
        if temp == 'n':
            play = False
