import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from Smart_Contract import elections_solidity_functions as contract


class User:
    def __init__(
        self,
        uuid,
        full_name="",
    ):
        db = firestore.client()
        info = db.collection(u"Users").document(u"{}".format(uuid)).get()
        if info.exists:
            data = info.to_dict()
            self.name = data["name"]
            self.uuid = data["identity hash"]
            self.description = data["description"]
            self.privilege = data["privilege"]
            self.elections = data["elections"]
        else:
            data = {
                u"name": full_name,
                u"privilege": 0,
                u"identity hash": uuid,
                u"description": "",
                u"elections": [],
            }
            db.collection(u"Users").document(u"{}".format(uuid)).set(data)
            self.uuid = uuid
            self.name = full_name
            self.privilege = 0
            self.votes_sent = []

    def join_election(self, election_id):
        db = firestore.client()
        self.elections.append(election_id)
        db.collection(u"Users").document(u"{}".format(self.uuid)).update(
            {u"elections": firestore.ArrayUnion([election_id])}
        )
        contract.createCandidate(election_id, self.name, self.description)

    def has_voted(self, election_id):
        return contract.hasUserVoted(election_id, self.uuid)

    def get_user(uuid):
        db = firestore.client()
        return db.collection(u"Users").document(u"{}".format(uuid)).get().to_dict()

    def vote(self, election_id, candidate_id):
        contract.vote(election_id, candidate_id, self.uuid)


cred = credentials.Certificate("src/credentials.json")
firebase_admin.initialize_app(cred, {"projectId": "equalis-4ceff"})
user = User.get_user("MTR0wePMRozc8mJLhpNc")
print(user[u"elections"])
