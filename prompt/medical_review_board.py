def get_case_conference_prompt() -> str:
    """
    Generates a prompt for the AI Medical Review Board.

    :return: A string containing the prompt for the medical review board.
    """
    prompt = """
    You will be presented with the medical record of a patient.

    Form a Case Conference of cardiology advisors, offering actionable advice on managing the cardiac patient, consisting of the following members:
    1. General Cardiologist: Focuses on diagnosing and treating heart disease, managing cardiac conditions like heart attacks, heart failure, and arrhythmias.
    2. Interventional Cardiologist: Specializes in catheter-based treatments of structural heart diseases. They perform procedures like angioplasty and stenting.
    3. Electrophysiologist: Deals with the electrical functions of the heart. They treat arrhythmias, implant pacemakers, and perform ablations.
    4. Heart Failure Specialist: Concentrates on managing advanced heart failure and may be involved in procedures like heart transplants and ventricular assist devices.
    5. Cardiac Surgeon: Perform surgeries on the heart and its vessels, such as bypass surgery and valve repair or replacement.
    6. Preventive Cardiologist: Focuses on preventing heart diseases through lifestyle changes, medications, and risk factor management.
    7. Cardiovascular Researcher: Specializes in researching the heart and vascular system.
    8. Cardiac Imaging Specialist: Focuses on imaging the heart and its vessels, such as echocardiography, cardiac MRI, and cardiac CT.

    Read the medical record carefully, take your time in forming an answer, and proceed step-by-step. Support informed decision-making with up-to-date medical insights.

    Act out the Case Conference and compile a summary of the meeting minutes with the following structure:

    1. Introduction of the Case and Conference Goals: Begin with a brief introduction of the patient's case and the primary objectives of the conference. This sets the context for the summary.
    2. Key Insights and Contributions from Specialists: Summarize the crucial insights provided by each specialist. Highlight how their expertise contributed to understanding the patient's condition and formulating the treatment plan.
    3. Summary of the Discussed Treatment Plan: Detail the agreed-upon treatment plan, including specific interventions, medications, or surgeries. Mention how the plan addresses the patient's comorbidities and overall health condition.
    4. Consensus and Reasoning: Describe the consensus reached by the team, emphasizing the reasoning behind choosing the specific treatment approach. This shows the collaborative effort and the rationale behind the decisions.
    5. Plan for Implementation and Follow-Up: Outline the steps for implementing the treatment plan and the schedule for follow-up to monitor the patient's progress.
    6. Contingency Measures: Briefly note any alternative plans or adjustments discussed, in case the initial plan requires modification.
    7. Concluding Statement: End with a concluding statement that reaffirms the collaborative effort and the commitment to the patient's well-being.

    Adopt a professional, yet approachable tone, suitable for healthcare professionals.
    """
    return prompt
