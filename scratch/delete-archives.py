import json
import logging
import boto3
from botocore.exceptions import ClientError
import sys


def delete_vault(vault_name):
    """Delete an Amazon S3Glacier vault

    :param vault_name: string
    :return: True if vault was deleted, otherwise False
    """

    # Delete the vault
    glacier = boto3.client('glacier')
    try:
        response = glacier.delete_vault(vaultName=vault_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_archive(vault_name, archive_id):
    """Delete an archive from an Amazon S3 Glacier vault

    :param vault_name: string
    :param archive_id: string
    :return: True if archive was deleted, otherwise False
    """

    # Delete the archive
    glacier = boto3.client('glacier')
    print("Assigned boto3 client as glacier.")
    try:
        print("trying to delete")
        response = glacier.delete_archive(vaultName=vault_name,
                                          archiveId=archive_id)
        print("this is the response ", response)
        print("done with trying to delete")

    except ClientError as e:
        logging.error(e)
        return False
    return True


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
    test_vault_name = vn

    print(test_vault_name)

    # Set up logging
    print("Setting Up Logging.")
    logging.basicConfig(level=logging.WARNING,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Delete the archive
    print("Deleting the archives.")
    mycounter = 0
    for a in archive:
        mycounter += 1
        print("Deleting ArchiveId #", mycounter)
        test_archive_id = a["ArchiveId"]
        success = delete_archive(test_vault_name, test_archive_id)
        print("Did the archive get deleted? ",success)
    if success:
        logging.info(f'Deleted archive {test_archive_id} from {test_vault_name}')
    else:
        logging.info(f'ERROR ERROR')

if __name__ == '__main__':
    main()