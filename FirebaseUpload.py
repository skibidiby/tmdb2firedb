# python
# To run code use: python upload-json-file-to-firestore.py data.json add users-demo-add
# for command line arguements.
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def import_data(data, collection_name):
    print(data)
    try:
        # CONNECT TO FIRESTORE DB
        cred = credentials.Certificate(
            "./serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        doc_ref = db.collection(collection_name)
        # UPLOAD DATA
        for dataum in data:
            doc_ref.document(str(dataum['id'])).set(dataum)
            print("\nAdded: {}".format(dataum))
    except Exception as error:
        print("\nERROR: {}".format(str(error)))
    else:
        print("\nImport completed")


def sync_data(scanned_data, collection_name):
    try:
        # CONNECT TO FIRESTORE DB
        cred = credentials.Certificate(
            "./serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        # COLLECTION SNAPSHOT
        doc_ref = db.collection(collection_name)
        snapshots = doc_ref.get()
        print('snapshot successful')
        scanned_list = [str(x['id']) for x in scanned_data]
        snapshots_list = [x.id for x in snapshots]
        # CHECK IF THERE'S USELESS DATA IN THE DB
        useless_records = list(set(snapshots_list) - set(scanned_list))
        if useless_records:
            print('Unnecessary database records found:')
            for i in snapshots:
                if i.id in useless_records:
                    print(i['title'])
        else:
            print('No unnecessary database records.')
            # CHECK IF THERE ARE SOME MISSING MOVIES IN THE DATABASE
        missing_movies = list(set(scanned_list) - set(snapshots_list))
        if missing_movies:
            print("There's some missing movies in the databse:")
            for i in scanned_data:
                if str(i['id']) in missing_movies:
                    if input('Do you want to add ' + i['title'] + ' to the database? y/n') == 'y':
                        try:
                            doc_ref.document(str(i['id'])).set(i)
                        except Exception as error:
                            print("\nERROR: {}".format(str(error)))

        else:
            print("There's no missing movies in the database")
    except Exception as error:
        print("\nERROR: {}".format(str(error)))
