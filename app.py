import streamlit as st
import google.generativeai as genai
api_key = "AIzaSyC5yI3fLcsSIqgt9OSvyz9YaNxwcn3utCI"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Define generation settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}
def generate_resume(name, job_title):
    # Create the generative model instance
    model = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config=generation_config)

    # Construct the context dynamically based on user input
    context = f"name: {name}\njob_title: {job_title}\nWrite a professional resume for the above details."

    # Start chat session
    chat_session = model.start_chat(history=[{"role": "user", "parts": [{"text": context}]}])

    # Get response from the model
    response = chat_session.send_message(context)

    # Extract and return the resume content
    if isinstance(response.candidates[0].content, str):
        return response.candidates[0].content
    else:
        return response.candidates[0].content.parts[0].text
def clean_resume_text(text):
    # Replace placeholders with more user-friendly ones
    cleaned_text = text.replace("[Add Email Address]", "[Your Email Address]")
    cleaned_text = cleaned_text.replace("[Add Phone Number]", "[Your Phone Number]")
    cleaned_text = cleaned_text.replace("[Add LinkedIn Profile URL (optional)]", "[Your LinkedIn Profile URL]")
    cleaned_text = cleaned_text.replace("[University Name]", "[Your University Name]")
    cleaned_text = cleaned_text.replace("[Graduation Year]", "[Your Graduation Year]")
    return cleaned_text
st.title("SmartResume Generator")
st.subheader("Create a professional resume in seconds!")

# Text input fields for user data
name = st.text_input("Enter your name")
job_title = st.text_input("Enter your job title")
if st.button("Generate Resume"):
    if name and job_title:
        resume = generate_resume(name, job_title)
        cleaned_resume = clean_resume_text(resume)

        # Display the generated resume
        st.markdown("### Generated Resume")
        st.markdown(cleaned_resume)
    else:
        st.warning("Please enter both your name and job title.")
