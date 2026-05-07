import os
import gradio as gr
import google.generativeai as genai

from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT


# LOAD ENV VARIABLES
load_dotenv()

# CONFIGURE GEMINI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# LOAD MODEL
model = genai.GenerativeModel("gemini-2.0-flash")


# MAIN FUNCTION
def diagnose_ad(platform, issue):

    try:

        prompt = f"""
        {SYSTEM_PROMPT}

        Platform: {platform}

        User Issue:
        {issue}
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        if "429" in str(e):
            return """
            ## ⚠️ API Limit Reached

            Your Gemini API free quota has been exceeded.

            ### Fix:
            - Create a new Gemini API key
            - Or wait a few minutes before retrying
            """

        return "Something went wrong. Please try again."


# UI
with gr.Blocks(theme=gr.themes.Soft()) as app:

    gr.Markdown(
        """
        # 🚀 AI Ad Diagnostic Agent

        Analyze Meta and Google Ads using Gemini AI
        """
    )

    # PLATFORM DROPDOWN
    platform = gr.Dropdown(
        ["Meta Ads", "Google Ads"],
        label="Advertising Platform"
    )

    # USER INPUT
    problem = gr.Textbox(
        lines=6,
        placeholder="Describe your ad issue...",
        label="Ad Problem"
    )

    # BUTTON
    diagnose_btn = gr.Button("Analyze Campaign")

    # OUTPUT
    output = gr.Markdown()

    # EXAMPLES
    gr.Examples(
        examples=[
            ["Meta Ads", "My ads are active but not spending"],
            ["Google Ads", "High CPC and low conversions"],
            ["Meta Ads", "My CPM is very high"]
        ],
        inputs=[platform, problem]
    )

    # BUTTON ACTION
    diagnose_btn.click(
        fn=diagnose_ad,
        inputs=[platform, problem],
        outputs=output
    )


# LAUNCH APP
app.launch(share=True)