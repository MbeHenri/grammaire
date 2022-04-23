
class Grammaire():
    def __init__(self, axiome="S", sep=' '):
        self.sep = " "
        self.S = axiome
        self.Vn = [self.S]
        self.Vt = [""]
        self.P = {}
        self.P[self.S] = []

    def valid_b(self, b) -> bool:
        if b == "":
            return True
        for e in str(b).split(self.sep):
            if e not in self.Vt and e not in self.Vn:
                return False
        return True

    def add_production(self, a, b):
        if a in self.Vn and self.valid_b(b):
            self.P[a].append(b)

    def add_terminal(self, t):
        s = str(t)
        if s not in self.Vt:
            self.Vt.append(s)

    def add_none_terminal(self, nt):
        s = str(nt)
        if s not in self.Vn:
            self.Vn.append(s)
            self.P[s] = []

    def delete_none_terminal(self, nt):
        self.Vn.remove(nt)
        del self.P[nt]
        for a in self.Vn:
            list = []
            for b in self.P[a]:
                if nt in b:
                    list.append(b)
            for e in list:
                self.P[a].remove(e)

    # elimination des symboles inutiles
    def eliminate_inutil_symbol(self):
        utiles = []
        for a in self.Vn:
            for b in self.P[a]:
                if b in self.Vt:
                    utiles.append(a)

        for a in self.Vn:
            if a not in utiles:
                for b in self.P[a]:
                    ok = True
                    for mot in b.split(self.sep):
                        if mot not in utiles and mot not in self.Vt:
                            ok = False
                    if ok:
                        utiles.append(a)
        non_utiles = []
        for a in self.Vn:
            if a not in utiles:
                non_utiles.append(a)
        for a in non_utiles:
            self.delete_none_terminal(a)

        utiles = self.reaching_none_terminal(self.S)

        non_utiles = []
        for a in self.Vn:
            if a not in utiles:
                non_utiles.append(a)
        for a in non_utiles:
            self.delete_none_terminal(a)

    def reaching_none_terminal(self, nt):
        result = [nt]
        c = [nt]
        while len(c) != 0:
            list = []
            for new_nt in c:
                for b in self.P[new_nt]:
                    for mot in b.split(self.sep):
                        if mot not in list and mot not in result and mot in self.Vn:
                            list.append(mot)
            result += list
            c = []
            c += list
        return result
    
    # suppression des non terminaux annulables
    def delete_annulable_none_terminal():
        pass
        
    
    def is_annulable_none_terminal(self, nt) -> bool:
        parcouru = []
        val = self.__is_annulable_none_terminal_(nt, parcouru)
        return val
        
    def __is_annulable_none_terminal_(self, nt, parcouru) -> bool:
        parcouru.append(nt)
        ok = False
        i, n = 0, len(self.P[nt])
        while ok == False and i < n:
            if(self.P[nt][i] == ""):
                ok = True
            else:
                i += 1
        if ok:
            return True
    
        for b in self.P[nt]:
            mots = b.split(self.sep)
                
            ok = True
            i, n = 0, len(mots)
            while ok == True and i < n:
                if mots[i] not in self.Vn:
                    ok = False
                else:
                    i += 1
                        
            if ok:
                for mot in mots:
                    if mot in parcouru:
                        return False
                            
                i, n = 0, len(mots)
                while i < 2 and self.__is_annulable_none_terminal_(mots[i], parcouru):
                    i = i+ 1
                if i == n:
                    return True
        return False
    
    def __str__(self) -> str:
        return """
        Axiome : """ + str(self.S)+"""
        Non termimaux Vn:  """ + str(self.Vn)+"""
        Terminaux Vt:  """ + str(self.Vt)+"""
        Seperateur :  """ + str(self.sep)+"""
        Productions 
        """ + str(self.P)+"""
        """


    
G = Grammaire()
G.add_none_terminal("A")
G.add_none_terminal("C")
G.add_terminal('b')

G.add_production("S", "A C")
G.add_production("S", "b")
G.add_production("A", "")
G.add_production("A", "A b")
G.add_production("C", "S A")

print(G)
G.eliminate_inutil_symbol()
print(G)

print(G.is_annulable_none_terminal("A"))
