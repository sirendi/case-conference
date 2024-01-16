import requests
from typing import Any, Dict


class ClinicalTrialsAPI:
    def __init__(self):
        self.base_url = "https://clinicaltrials.gov/api/v2/studies"

    def search_trials(self, condition: str, max_results: int = 5) -> Dict[str, Any]:
        params = {
            "format": "json",
            "query.cond": condition,
            "pageSize": max_results
        }

        response = requests.get(self.base_url, params={key: str(value) for key, value in params.items()})

        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError(f"Error: {response.status_code} - {response.text}")

    def format_trials(self, data: Dict[str, Any]) -> str:
        if 'studies' not in data or not data['studies']:
            return "No studies found or unexpected data format."

        formatted_results = []
        for study in data['studies']:
            identification_module = study['protocolSection']['identificationModule']
            status_module = study['protocolSection']['statusModule']

            nct_id = identification_module.get('nctId', 'Not provided')
            title = identification_module.get('briefTitle', 'Not provided')
            status = status_module.get('overallStatus', 'Not provided')

            formatted_results.append(f"NCT ID: {nct_id}\nTitle: {title}\nStatus: {status}\n")

        return "\n".join(formatted_results)
