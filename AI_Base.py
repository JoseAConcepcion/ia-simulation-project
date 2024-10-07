
class Rule:
    def __init__(self, conditions, actions, potentiators):
        self.conditions = conditions
        self.actions = actions
        self.potentiators = potentiators

class Personality:
    def __init__(self):
        self.named_rules = {}
        self.rules = []
        self.emergency_rules = []
    
    #Conditions in format [["a","b"],["c"]], representing "(a and b) or c"
    #Actions in format [("a", [["b", "c"], ["d"]]), ...], representing "do a until condition [[],[]] is met, and then do the rest..."
    #Potentiators in the format [("enemies_in_sight", 20), ("distance_from_border", 3)]. The pairs are: (variable_name, multiplier)
    #name != "" si se quiere que la regla solo pueda llamada por otra regla
    def add_rule(self, conditons, actions, potentiators, name = ""):
        r = Rule(conditons, actions, potentiators)
        if name == "":
            self.rules.append(r)
        else:
            self.named_rules[name] = r

            

    def add_emergency_rule(self, conditons, actions):
        self.emergency_rules.append(Rule(conditons, actions, []))
