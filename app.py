import streamlit as st
import time
import google.generativeai as genai
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
from contextlib import redirect_stdout


genai.configure(api_key="AIzaSyCCUchiWWxvciW30IxQQ3LIiBgKHlHhGIs")

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini("titanic.csv", mime_type="text/csv"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
      ],
    },
  ]
)

# Streamlit interface
st.title("CSV Agent for Titanic Dataset")
st.write("Ask any question about the Titanic dataset!")

query = st.text_input("Enter your question:")

prompt = """
The colummns of the Titanic.csv are as follows :- 
-PassengerId :- Passenger number(Unique Identifier)
-Survived :- mapping; 0 = Dead 1 = Alive
-Pclass :-mapping; 1 = First class 2 = Second class 3 = Third class
-Name :- Name of passenger
-Sex :- Gender (values : male,female)
-Age :- Age of passenger
-SibSp :- Number of siblings
-Parch
-Ticket
-Fare :- Ticket Fare
NOTE :- if the question has terms like distribution, graph, plot or chart, try giving relevant code for plotting a suitable graph which helps in answering the question, in one continuous python code NOT in segments.
Now answer the following question using Titanic.csv :- 
"""

if query:
    with st.spinner("Processing your question..."):
        try:
            # Use the agent to answer the query
            final_prompt= prompt + query
            # st.write(final_prompt)
            response = chat_session.send_message(final_prompt)
            st.write("### Response:")
            st.write(response.text)
            response_text = response.text
            if "```python" in response_text :
                # Extract the code block
                code_match = re.search(r"```python(.*?)```", response_text, re.DOTALL)
                
                if code_match:
                    plotting_code = code_match.group(1).strip()
                    # st.write(plotting_code)
                    # Display the code snippet
                    # st.code(plotting_code, language="python")
                    # st.write("CODE :- ")
                    # st.code(plotting_code)
                    # Shared namespace for exec
                    shared_namespace = {
                        "plt": plt,
                        "sns": sns,
                        "pd": pd,
                        "io": io,
                    }
                
                    # Redirect stdout to capture print statements
                    output_buffer = io.StringIO()
                    try:
                        with redirect_stdout(output_buffer):
                            # Execute the code block
                            exec(plotting_code, shared_namespace)
                            # Capture and display stdout
                            output_text = output_buffer.getvalue()
                            if output_text:
                                st.text("Code Output:")
                                st.text(output_text)

                            # Display any generated plots
                            if plt.get_fignums():
                                st.write("Executing plot")
                                st.pyplot(plt.gcf())
                                plt.close('all')  # Clear current figure
                            else:
                                st.info("No plots generated by the code.")

                    except Exception as e:
                        st.error("Error while executing the code:")
                        st.text(str(e))

                    finally:
                        output_buffer.close()

            else:
                st.info("No Python code detected in the response.")

        except Exception as e:
            st.error(f"Error processing the query: {e}")

