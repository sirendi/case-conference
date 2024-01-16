import json
import requests
from openai import OpenAI
import os
from prompt.medical_review_board import get_case_conference_prompt
from api.clinical_trials.clinical_trials import ClinicalTrialsAPI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class Agent:
    def __init__(self):
        api_key = OPENAI_API_KEY
        self.client = OpenAI(api_key=api_key)
        self.model_version = "gpt-4"

    @staticmethod
    def chat_completion_request(messages, tools=None, tool_choice=None, model=None):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + OPENAI_API_KEY,
        }
        json_data = {"model": model, "messages": messages}
        if tools is not None:
            json_data.update({"tools": tools})
        if tool_choice is not None:
            json_data.update({"tool_choice": tool_choice})
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
            return response
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e

    def extract_primary_diagnosis(self, clinical_data: str) -> str:
        messages = [
            {"role": "system", "content": "Extract the primary diagnosis from the following patient data."},
            {"role": "system", "content": "Only include one diagnosis. If there are multiple, choose the most severe."},
            {"role": "system", "content": "Do not add any additional information before or after the diagnosis. Only include the diagnosis."},
            {"role": "user", "content": clinical_data}
        ]
        response = self.client.chat.completions.create(model=self.model_version, messages=messages)
        return response.choices[0].message.content.strip()

    @staticmethod
    def search_clinical_trials(condition: str, max_results: int = 5) -> str:
        api = ClinicalTrialsAPI()
        try:
            results = api.search_trials(condition, max_results)
            formatted_results = api.format_trials(results)
            return formatted_results
        except Exception as e:
            return (f"Error: {e}")

    def get_actionable_advice(self, clinical_data: str, case_conference: str) -> str:
        messages = [
            {"role": "system", "content": case_conference},
            {"role": "user", "content": clinical_data}
        ]
        response = self.client.chat.completions.create(model=self.model_version, messages=messages)
        return response.choices[0].message.content.strip()

    def run_conversation(self, user_input: str, clinical_data: str) -> str:
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_clinical_trials",
                    "description": "Search for clinical trials based on a condition",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "condition": {"type": "string"},
                            "max_results": {"type": "integer"}
                        },
                        "required": ["condition"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_actionable_advice",
                    "description": "Get actionable advice for a patient based on their data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "clinical_data": {"type": "string"},
                            "case_conference": {"type": "string"}
                        },
                        "required": ["clinical_data", "case_conference"],
                    },
                },
            }
        ]

        messages = [
            {"role": "system", "content": "Assist with medical inquiries and advice."},
            {"role": "user", "content": user_input},
            {"role": "user", "content": clinical_data}
        ]

        response = self.chat_completion_request(messages=messages, tools=tools, tool_choice="auto", model=self.model_version)

        if response.status_code == 200:
            response_data = response.json()

            tool_calls = response_data['choices'][0]['message'].get('tool_calls')
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call['function']['name']
                    args = tool_call['function']['arguments']
                    if isinstance(args, str):
                        args = json.loads(args)
                    if function_name == "search_clinical_trials":
                        primary_diagnosis = self.extract_primary_diagnosis(clinical_data)
                        max_results = args.get("max_results", 5)
                        return self.search_clinical_trials(primary_diagnosis, max_results)
                    elif function_name == "get_actionable_advice":
                        case_conference = get_case_conference_prompt()
                        return self.get_actionable_advice(clinical_data, case_conference)

            return response_data['choices'][0]['message']['content']
        else:
            print(f"Error with ChatCompletion request: {response.status_code}")
            return "Error in processing request"
