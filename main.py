from itertools import islice

from documentcloud.addon import AddOn

PROJ_ID = 209284
FILECOIN_ID = 104
BATCH_SIZE = 10
BATCH_NUM = 20


class CrestFilecoin(AddOn):
    def main(self):

        # Search for all documents in the CREST project which do not yet have an
        # Estuary ID.  The Estuary ID metadata will be set by the Filecoin Add-On
        # after it has been uploaded to Filecoin via Estuary
        documents = self.client.documents.search(
            f"+project:{PROJ_ID} -data_estuaryId:*"
        )
        for i in range(BATCH_NUM):
            # Pull out the IDs for a batch of the documents
            doc_ids = [
                d.id for d in islice(documents, i * BATCH_SIZE, (i + 1) * BATCH_SIZE)
            ]
            # Run the Filecoin Add-On for this batch of documents
            self.client.post(
                "addon_runs/",
                json={
                    "addon": FILECOIN_ID,
                    "parameters": {},
                    "documents": doc_ids,
                    "dismissed": True,
                },
            )


if __name__ == "__main__":
    CrestFilecoin().main()
