import json
from snowflake.core import Root
from snowflake.snowpark import Session
from typing import List, Union, Dict

class CortexSearch:
    def __init__(
        self, 
        connection_config: Union[str, Dict], 
        service_config: Union[str, Dict]
    ) -> None:
        """
        Initializes the RetrievalAgent by reading connection and service parameters.

        Args:
            connection_config (Union[str, Dict]): Path to the JSON file or dictionary containing connection parameters.
            service_config (Union[str, Dict]): Path to the JSON file or dictionary containing service parameters.
        """
        # Load connection parameters
        if isinstance(connection_config, str):
            with open(connection_config, "r") as file:
                connection_parameters = json.load(file)
        else:
            connection_parameters = connection_config

        self.session: Session = Session.builder.configs(connection_parameters).create()
        self.root: Root = Root(self.session)

        # Load service parameters
        if isinstance(service_config, str):
            with open(service_config, "r") as file:
                service_parameters = json.load(file)
        else:
            service_parameters = service_config

        database: str = service_parameters["database"]
        schema: str = service_parameters["schema"]
        service_name: str = service_parameters["service_name"]

        self.service = (
            self.root.databases[database]
            .schemas[schema]
            .cortex_search_services[service_name]
        )

    def get_retrieval(self, query: str, k: int) -> List[str]:
        if not self.service:
            raise ValueError(
                "Service not set. Use `set_service` method to initialize the service."
            )

        resp = self.service.search(query=query, columns=["text"], limit=k)

        response = json.loads(resp.to_json())
        retrieval_result: List[str] = [result["text"] for result in response["results"]]

        return retrieval_result