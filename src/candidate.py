class Candidate:

    def __init__(self, id, name, description):
        self._id = id
        self._name = name
        self._description = description
        self._votes = 0

    
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
    
    @property
    def votes(self):
        return self._votes

    @votes.setter
    def votes(self, value):
        self._votes = value
    
    

