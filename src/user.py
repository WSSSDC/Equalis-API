class User:

    def __init__(self, uuid, name, wallet_address):
        self._wallet_address = wallet_address
        self._uuid = uuid
        self._name = name
        self._privilege = 0
        self._votes_sent = set()

    @property
    def privilege(self):
        return self._privilege

    @privilege.setter
    def privilege(self, value):
        self._privilege = value
    
    def update_votes(self, election_id):
        self._votes_sent.add(election_id)
    
    def has_voted(self, election_id):
        return election_id in self._votes_sent
