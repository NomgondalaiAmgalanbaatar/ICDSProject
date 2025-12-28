# How to Configure Environment Variables for AI Features

To enable AI features (Summary, Keywords, Sentiment Analysis, Image Generation), you need to set up your API keys.

1.  **Open the `.env` file** in this directory.
2.  **Add your OpenAI API Key**:
    ```
    OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
    ```
    *Note: A key is already present in your `.env` file. If it is valid, you are good to go!*

3.  **Run the Application**:
    When you start `GUI.py` or the client, the application will automatically load these variables.

4.  **Troubleshooting**:
    If AI features don't work, ensure:
    -   You have internet access.
    -   Your API key is valid and has credits.
    -   You have installed the requirements: `pip install -r requirements.txt`
