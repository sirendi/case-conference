import streamlit as st
from database.connection import get_patient_names, get_patient_clinical_data
from pdf.pdf_converter import create_pdf
from agents.agent import Agent


def main() -> None:
    st.title("AI Case Conference")

    patient_names = get_patient_names()
    if patient_names:
        selected_patient = str(st.selectbox("Select a Patient:", patient_names, index=0))
        clinical_data = get_patient_clinical_data(selected_patient) or "No clinical data available."
        clinical_data = "\n".join(clinical_data)

        user_input = st.text_area("Enter your request:", "")

        if st.button("Generate"):
            with st.spinner("Generating..."):
                agent = Agent()
                response = agent.run_conversation(user_input, clinical_data)
                pdf_file = create_pdf(response)
                st.download_button(
                    label="Download report",
                    data=pdf_file,
                    file_name="analysis_outcome.pdf",
                    mime="application/octet-stream"
                )
    else:
        st.write("No patients available.")


if __name__ == "__main__":
    main()
