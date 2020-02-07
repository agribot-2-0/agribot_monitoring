import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore

#this class will monitor vital
class Monitor:
    #db 

    def __init__(self):
        return

    def initialize_connection_with_firestore(self, certificate_file):
        cred = credentials.Certificate(certificate_file)
        firebase_admin.initialize_app(cred, {
            'projectID' : 'agribot-cd437', 
        })
        db = firestore.client()
        agri_ref = db.collection(u'agribot')
        docs = agri_ref.stream()
        for doc in docs:
            print (u'{} => {}'.format(doc.id, doc.to_dict()))

        return True
