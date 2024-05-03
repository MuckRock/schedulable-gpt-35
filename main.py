""" islice to make batches of documents, AddOn import """
from itertools import islice
from documentcloud.addon import AddOn

class GPTScheduler(AddOn):
    """Allows you to run the GPT 3.5 Turbo Add-On on a scheduled basis"""

    def main(self):
        """Pulls the batch size of documents and runs the Add-On on the next set"""
        run_id = 352

        batch_num = 1
        batch_size = self.data.get("batch_size")
        proj_id = self.data.get("project_id")
        key_name = self.data.get("key_name")
        prompt = self.data.get("prompt")
        limiter = self.data.get("limiter")
        filter_key = self.data.get("filter_key")
        filter_value = self.data.get("filter_value")

        if filter_key is not None:
            if filter_value is not None:
                documents = self.client.documents.search(
                    f'+project:{proj_id} -data_{key_name}:* data_{filter_key}:"{filter_value}"'
                )
            else:
                documents = self.client.documents.search(
                    f'+project:{proj_id} -data_{key_name}:* data_{filter_key}:*'
                )
        else:
            documents = self.client.documents.search(
                f'+project:{proj_id} -data_{key_name}:*'
            )
        for i in range(batch_num):
            # Pull out the IDs for a batch of the documents
            doc_ids = [
                d.id for d in islice(documents, i * batch_size, (i + 1) * batch_size)
            ]
            # Run the GPT 3.5 Turbo Add-On for this batch of documents
            self.client.post(
                "addon_runs/",
                json={
                    "addon": run_id,
                    "parameters": {
                        "value": f"{key_name}",
                        "prompt": f"{prompt}",
                        "limiter": limiter
                    },
                    "documents": doc_ids,
                    "dismissed": True,
                },
            )


if __name__ == "__main__":
    GPTScheduler().main()
