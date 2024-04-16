import requests, uuid, json
import streamlit as st
# Add your key and endpoint
key = "657bb53b734b4e29942ccac64f8c5c97"
endpoint = "https://api.cognitive.microsofttranslator.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "eastus"

# Input text box for user to input text
input_text = st.text_area("Enter text to translate", "I would really like to drive your car around the block a few times!")

# Dropdown to select target languages
target_languages = st.multiselect("Select target languages", ["French (fr)", "Zulu (zu)","Afrikaans(af)","Punjabi","Hindi","Urdu"])

# Convert language codes
#Punjabi (Eastern)	pa
lang_map = {"French (fr)": "fr", "Zulu (zu)": "zu","Afrikaans(af)":'af',"Punjabi":'pa','Hindi':'hi',"Urdu":'ur'}
target_lang_codes = [lang_map[lang] for lang in target_languages]

if st.button("Translate"):
    # Construct URL and headers
    path = '/translate'
    constructed_url = endpoint + path
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Construct request body
    body = [{
        'text': input_text
    }]

    # Make API request
    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': target_lang_codes
    }
    response = requests.post(constructed_url, params=params, headers=headers, json=body)

    # Display translation results
    if response.status_code == 200:
        translation_results = response.json()
        for idx, translation in enumerate(translation_results):
            st.subheader(f"Translation ({target_languages[idx]})")
            st.write(translation['translations'][0]['text'])
    else:
        st.error("Translation failed. Please check your input and try again.")