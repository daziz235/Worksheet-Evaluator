import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
from openai import OpenAI
from PIL import Image



# Initialize OpenAI client
api_key = st.secrets.get("OPENAI_API_KEY")
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
)

# Custom CSS Styles
st.markdown(
    """
    <style>
        body { background-color: #f7f9fc; }
        .title { font-size: 1.7rem; color: #888; font-weight:bold; text-align: left; margin-bottom: 0px; }
        .subtitle { font-size: 1.2rem; color: #888; text-align: left; margin-bottom: 70px; }
        .section-header { color: #264653; font-size: 1.5rem; margin-top: 30px; }
        .success-box { background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 10px; margin-top: 20px; }
        .success-message { color: #28a745; font-size: 14px; font-weight: 600; text-align: center; margin-top: 8px; }
        .footer { text-align: center; color: #888; font-size: 0.9rem; margin-top: 120px; }
        .stFileUploader { padding: 1px 1px; font-size: 13px; border-radius: 6px; color: #fff; background-color: #4A90E2; border: none; transition: 0.3s; }
        .stFileUploader:hover { background-color: #FF8C00; transform: scale(1.05); }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and Subtitle
st.markdown('<div class="title">EvalAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your worksheets and get detailed AI-powered evaluations instantly!</div>', unsafe_allow_html=True)

# Sidebar Instructions
with st.sidebar:
    st.title("📋 Instructions")
    st.write(
        """
        1. Upload **two PDFs/Images**:
            - **Questions PDF/Image**: Contains only questions.
            - **Responses PDF/Image**: Contains questions and student responses.
        2. Click **Start Evaluation** to get the Evaluation done.
        3. View the detailed feedback and overall improvement areas!
        """
    )
    st.info("Ensure the files are legible for the best results.")

# File Upload Section
col1, col2 = st.columns(2)

with col1:
    st.write("Upload **Questions Only** PDF/Image:")
    questions_file = st.file_uploader(
        "Browse files", type=["pdf", "png", "jpg", "jpeg"], key="questions", label_visibility="collapsed"
    )

with col2:
    st.write("Upload **Questions with Responses** PDF/Image:")
    responses_file = st.file_uploader(
        "Browse files", type=["pdf", "png", "jpg", "jpeg"], key="responses", label_visibility="collapsed"
    )



if questions_file:
    st.markdown('<p class="success-message">✔️ File with questions uploaded successfully.</p>', unsafe_allow_html=True)
if responses_file:
    st.markdown('<p class="success-message">✔️ File with questions and responses uploaded successfully.</p>', unsafe_allow_html=True)

if not questions_file or not responses_file:
    st.warning("⚠️ Please upload **both files** to proceed.")

# Extract Text from PDF
def extract_text_from_file(file):
    if not file:
        return ""

    if file.type in ["application/pdf"]:
        # Convert PDF pages to images
        images = convert_from_bytes(file.read())
    else:
        # Directly read the image file
        images = [Image.open(file)]

    # Extract text from all images
    all_text = []
    for img in images:
        text = pytesseract.image_to_string(img)
        all_text.append(text)
    return "\n".join(all_text)


# Function to evaluate responses 
def evaluate_responses_stream(questions_text, responses_text):
    combined_content = f"Questions:\n{questions_text}\n\nQuestions with Student Responses:\n{responses_text}"
    
    completion = client.chat.completions.create(
        model="mistralai/mixtral-8x22b-instruct-v0.1",
        messages=[
            {
                "role": "user",
                "content": f"""
                    You are a helpful and knowledgeable teacher. 
                    Below are questions and student responses extracted from PDF documents:

                    {combined_content}

                    Please evaluate each question individually and provide your feedback in the following format always:

                    **[Question Number] Question:** [The original question] \n
                    **Student Answer:** [The student answer] \n
                    **Evaluation:** [Correct/Incorrect/Partially Correct] \n
                    **Feedback:** [Detailed explanation of why the answer is correct/incorrect, including specific points about the student's reasoning, potential errors, and suggestions for improvement in case of incomplete or partially correct answers to improve the student's understanding]

                    After evaluating all the questions, please provide a final note on the areas where the student should focus for improvement:

                    **Overall Focus Areas:** [List the specific topics or concepts the student should focus on to improve, based on their answers across all questions.]
                    **[Overall]**: [<very accurate number of correct answers> out of <total number of questions accurately> are correct and <number of partially correct> are partially correct.]

                    Please be clear, concise, and objective in your feedback.
                """,
            }
        ],
        temperature=0.5,
        top_p=1,
        max_tokens=4096,
        stream=True,
    )
    return completion

# Evaluation Section
if st.button("🚀 Start Evaluation"):
    if not questions_file or not responses_file:
        st.error("❗ Please upload both the Questions pdf/image and the Responses pdf/image.")
    else:
        with st.spinner("⏳ Extracting text and evaluating responses..."):
            # Extract text from both PDFs
            questions_text = extract_text_from_file(questions_file)
            responses_text = extract_text_from_file(responses_file)

            # Ensure both files contain text
            if not questions_text.strip():
                st.error("❗ Failed to extract text from the Questions pdf/image. Please try again with a valid file.")
            elif not responses_text.strip():
                st.error("❗ Failed to extract text from the Responses pdf/image. Please try again with a valid file.")
            else:
                # Start streaming response
                st.markdown("### 📝 Evaluation Results")
                feedback_area = st.empty()  # Placeholder for dynamic updates

                response_stream = evaluate_responses_stream(questions_text, responses_text)
                response_text = ""

                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        # Append new content to response text
                        response_text += chunk.choices[0].delta.content
                        # Display updated text dynamically
                        feedback_area.markdown(response_text)

                # Final display of complete feedback
                st.success("Evaluation completed!")

# Footer

st.markdown(
    """
    <div class="footer">
        ---
    </div>
    """,
    unsafe_allow_html=True,
)
