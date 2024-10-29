import streamlit as st
import docx
import uuid

def create_docx(feedback):
    doc = docx.Document()
    doc.add_paragraph(feedback)
    return doc

def app():

    st.title("Feedback 📝")
    st.write("We're constantly working to make this app the best it can be. If you spot anything that's not quite right, or have a suggestion for a new feature, please don't hesitate to share your feedback.")

    user_feedback = st.text_area("Please share your feedback:")

    if st.button("Submit Feedback"):
        doc = create_docx(user_feedback)
        file_name = f"feedback_{uuid.uuid4()}.docx"
        doc.save(file_name)
        st.write("Thank you for your submission!")
        

        # with open(file_name, "rb") as file:
        #     st.download_button(
        #         label="Download Feedback",
        #         data=file,
        #         file_name=file_name,
        #         mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        #     )