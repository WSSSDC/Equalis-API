import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

class User:
    def __init__(self, full_name, uuid = "", privilege = 0, votes_sent = set()):
        cred = credentials.Certificate("src/credentials.json")
        firebase_admin.initialize_app(cred, {
            'projectId' : "equalis-4ceff"
        })
        db = firestore.client()
        name_id = "_".join([x.title() for x in full_name.split(" ")])
        info = db.collection(u'Users').document(u'{}'.format(name_id)).get()
        if info.exists:
            data = info.to_dict()
            self.name = data['name']
            self.uuid = data['uuid']
            self.privilege = data['privilege']
            self.votes_sent = data['votes_sent']
        else:
            data = {
                u'name': full_name,
                u'privilege': privilege,
                u'uuid': uuid,
                u'votes_sent': votes_sent,
            }
            db.collection(u'Users').document(u'{}'.format(name_id)).set(data)
            self.uuid = uuid
            self.name = full_name
            self.privilege = 0
            self.votes_sent = set()

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