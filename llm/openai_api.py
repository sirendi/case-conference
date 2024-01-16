from openai import OpenAI
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def call_openai_gpt(system_prompt: str, patient_data: str, user_input: str) -> str:
    """Call OpenAI GPT model to get the response.

    Args:
        system_prompt (str): The system's guiding prompt.
        patient_data (str): Clinical data of the selected patient.
        user_input (str): User's specific prompt.

    Returns:
        str: The response text from the model.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Patient medical record: {patient_data}"},
        {"role": "user", "content": user_input}
    ]

    api_key = OPENAI_API_KEY
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,  # type: ignore
        stream=True,
    )

    response_text = ""
    for chunk in response:
        response_text += chunk.choices[0].delta.content or ""  # type: ignore

    return response_text
