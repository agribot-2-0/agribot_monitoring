import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#this class will monitor vital
class Monitor(object):
    #database
    def __init__(self, rsn):
        self.database = None
        self.rsn = rsn
        return

    def initialize_connection_with_firestore(self, certificate_file):
        cred = credentials.Certificate(certificate_file)
        firebase_admin.initialize_app(cred, {
            'projectID' : 'agrsibot-cd437',
        })
        self.database = firestore.client()
        return True

    def read_from_db(self, collection_name):
        agri_ref = self.database.collection(collection_name)
        docs = agri_ref.stream()
        for doc in docs:
            print u'{} => {}'.format(doc.id, doc.to_dict())

    def write_pose_to_db(self, obj):
        if obj != None:
            doc_ref = self.database.collection('robots').document(self.rsn)
            doc_ref = doc_ref.collection(u'localization').document(u'pose')
            doc_ref.set(obj)

    def write_orientation_to_db(self, obj):
        if obj != None:
            doc_ref = self.database.collection('robots').document(self.rsn)
            doc_ref = doc_ref.collection(u'localization').document(u'orientation')
            doc_ref.set(obj)
