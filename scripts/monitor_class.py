import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


#this class will monitor vital
class Monitor(object):
    #database
    def __init__(self, rsn):
        self.database = None
        self.rsn = rsn

    def initialize_connection_with_firestore(self, certificate_file):
        cred = credentials.Certificate(certificate_file)
        firebase_admin.initialize_app(cred, {
            'projectID': 'agrsibot-cd437',
        })
        self.database = firestore.client()
        return True

    def write_to_db(self, path, obj):
        if obj is not None:
            path = 'robots/' + self.rsn + '/' + path
            doc_ref = self.database.document(path)
            doc_ref.set(obj)
