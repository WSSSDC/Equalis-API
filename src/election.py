from tracemalloc import start
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import datetime
class Election:

    def __init__(self, id, name = "", start_date = datetime.datetime.today(), end_date = datetime.datetime.today(), candidates = []):
        db = firestore.client()
        info = db.collection(u'Elections').document(u'{}'.format(id)).get()
        if info.exists:
            data = info.to_dict()
            self.id = data[u'id']
            self.name = data[u'name']
            self.start_date = data[u'start_date']
            self.end_date = data[u'end_date']
            self.candidates = data[u'candidates']
        else:
            data = {
                u'id': id,
                u'name': name,
                u'start_date': start_date,
                u'end_date': end_date,
                u'candidates': candidates
            }
            db.collection(u'Elections').document(u'{}'.format(id)).set(data)
            self.id = data[u'id']
            self.name = data[u'name']
            self.start_date = data[u'start_date']
            self.end_date = data[u'end_date']
            self.candidates = data[u'candidates']

    def get_election(id):
        db = firestore.client()
        return db.collection(u'Elections').document(u'{}'.format(id)).get().to_dict()

cred = credentials.Certificate("src/credentials.json")
firebase_admin.initialize_app(cred, {
    'projectId' : "equalis-4ceff"
})

print(Election.get_election(1))


