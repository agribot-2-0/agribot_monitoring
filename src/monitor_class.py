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
        self.db = firestore.client()
        return True

    def read_from_db(self, collection_name):
        agri_ref = self.db.collection(collection_name)
        docs = agri_ref.stream()
        for doc in docs:
            print (u'{} => {}'.format(doc.id, doc.to_dict()))

    def write_to_df(self, collection_name, document_name, object):
        if object!=None:
            doc_ref = self.db.collection(collection_name).document(document_name)
            doc_ref.set(object)
