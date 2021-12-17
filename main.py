# GCP CSV Congregate
# Taylor Bell
# 12.17.21

import csv
from google.cloud import storage


if __name__ == '__main__':

    print("+-------------------------+")
    print("| GCP CSV Congregate v0.1 |")
    print("+-------------------------+")

    # establish connection
    client = storage.Client()

    # grab bucket
    bucket = client.get_bucket('york-project-bucket')

    # grab folder
    folder = 'taylorryanbell/2021-12-17-18-12/'

    # create empty lists for later population
    blob_list = []
    single_file = [['author', 'points']]  # start with header here

    for blob in bucket.list_blobs(prefix=folder):
        blob_list.append(blob.name)

    blob_list.pop(0)  # remove directory name itself
    blob_list.pop(0)  # remove SUCCESS file
    # print(blob_list)

    # iterate through blob_list to add the content to the master list, "single_file"
    for item in blob_list:
        blob = bucket.get_blob(item)  # get the blob
        downloaded_blob = blob.download_as_string()  # download blob as bytes
        decoded_blob = downloaded_blob.decode("utf-8")  # parse bytes as string
        decoded_list = decoded_blob.split('\n')  # split string into list of pairs
        decoded_list.pop(0)  # remove header
        decoded_list.pop(-1)  # remove empty quotes at the end
        for row in decoded_list:
            row_list = row.split(',')
            single_file.append(row_list)  # add the list to the single_file

    # create the new CSV file locally
    with open('final-list.csv', 'w', encoding="utf-8") as file:
        write = csv.writer(file)
        write.writerows(single_file)

    # create a new file path in GCS
    new_blob_upload = bucket.blob(f'{folder}author_rankings.csv')

    # upload the CSV output file to GCS (file must exist locally first)
    new_blob_upload.upload_from_filename('final-list.csv', content_type='text/csv')
