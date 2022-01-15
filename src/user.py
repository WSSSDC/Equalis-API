import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

class User:
    def __init__(self, uuid, full_name = "",):
        cred = credentials.Certificate("src/credentials.json")
        firebase_admin.initialize_app(cred, {
            'projectId' : "equalis-4ceff"
        })
        db = firestore.client()
        info = db.collection(u'Users').document(u'{}'.format(uuid)).get()
        if info.exists:
            data = info.to_dict()
            self.name = data['name']
            self.uuid = data['uuid']
            self.privilege = data['privilege']
            self.votes_sent = data['votes_sent']
            self.elections = data['elections']
        else:
            data = {
                u'name': full_name,
                u'privilege': 0,
                u'uuid': uuid,
                u'votes_sent': [],
                u'elections': []
            }
            db.collection(u'Users').document(u'{}'.format(uuid)).set(data)
            self.uuid = uuid
            self.name = full_name
            self.privilege = 0
            self.votes_sent = []

    def update_votes(self, election_id):
        self.votes_sent.append(election_id)
    
    def join_election(self, election_id):
        self.elections.append(election_id)
    
    def has_voted(self, election_id):
        return election_id in self.votes_sent
