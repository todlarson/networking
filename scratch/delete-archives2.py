import json
import logging
import boto3
from botocore.exceptions import ClientError
import sys


def main():

    # Process input args
    fn = sys.argv[1]

    # Opening JSON file
    fn="/Users/todlarson/workspace/networking/scratch/" + fn
    f = open(fn)
    # Closing file
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    f.close()

    archive = data["ArchiveList"]

    #for a in archive:
    #    print("I want to delete this-",a["ArchiveId"],"-asap")
    
    test_vault_name = data["VaultARN"]

    tvn=test_vault_name.split(':')[5]
    vn=tvn.split('/')[1]
    vault_name = vn

    print(vault_name)

    # Set up logging
    print("Setting Up Logging.")
    logging.basicConfig(level=logging.WARNING,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Delete the archive
    print("Deleting the archives.")
    glacier = boto3.client('glacier')
    print("Assigned boto3 client as glacier.")
    mycounter = 0
    for a in archive:
        mycounter += 1
        print("Deleting ArchiveId #", mycounter)
        archive_id = a["ArchiveId"]
        print("trying to delete")
        response = glacier.delete_archive(vaultName=vault_name,
                                          archiveId=archive_id)
        print("this is the response ", response)

if __name__ == '__main__':
    main()