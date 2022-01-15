import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
class Candidate:

    def __init__(self, uuid, full_name = "", id = -1, description = "", votes = 0):
        cred = credentials.Certificate("src/credentials.json")
        firebase_admin.initialize_app(cred, {
            'projectId' : "equalis-4ceff"
        })
        db = firestore.client()
        info = db.collection(u'Candidates').document(u'{}'.format(uuid)).get()
        if info.exists:
            data = info.to_dict()
            self.id = data['id']
            self.description = data['description']
            self.name = data['name']
            self.votes = data['votes']
            self.uuid = data['uuid']
        else:
            data = {
                u'name': full_name,
                u'description': description,
                u'id': id,
                u'votes': votes,
                u'uuid': uuid
            }
            db.collection(u'Candidates').document(u'{}'.format(uuid)).set(data)
            self.id = id
            self.description = description
            self.name = full_name
            self.votes = votes
            self.uuid = uuid

    
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

    def onWin(self, privilege):
        db = firestore.client()
        db.collection(u'Users').document(u'{}'.format(self.uuid)).update({u'privilege': privilege})
