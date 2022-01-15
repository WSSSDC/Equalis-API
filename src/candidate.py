import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
class Candidate:

    def __init__(self, full_name, id = -1, description = "", votes = 0, uuid = ""):
        cred = credentials.Certificate("src/credentials.json")
        firebase_admin.initialize_app(cred, {
            'projectId' : "equalis-4ceff"
        })
        db = firestore.client()
        name_id = "_".join([x.title() for x in full_name.split(" ")])
        info = db.collection(u'Candidates').document(u'{}'.format(name_id)).get()
        if info.exists:
            data =  info.to_dict()
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
            db.collection(u'Candidates').document(u'{}'.format(name_id)).set(data)
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

doug = Candidate("Doug Ford")
print(doug._uuid)