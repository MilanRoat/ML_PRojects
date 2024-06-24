import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
genai.configure(api_key=os.getenv('Google_API'))

### to run this model you need to haye these libraries installed in your system - 
# youtube_transcript_api
#streamlit
#google_generativeai
#python-dotenv
#pathlib

### also use your own google gemini pro api key in .env file


from youtube_transcript_api import YouTubeTranscriptApi

def extract_transcript(URL):
    try:
        video_id = URL.split('=')[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id,languages=['en','hi'])
        transcript = ''
        for i in transcript_text:
            transcript += i['text'] + ' '

        return transcript

    except Exception as e:
        raise e

prompt = 'you are a youtube video summerizer. you will be taking the transcript text and summerizing the entire video and providing the important summery point wise within 200 words. the transcript text is - '
def generate_gemini(transcript_text,prompt):

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(prompt+transcript_text)

    return response.text


st.title("Youtube video transcript summerizer")
youtube_link = st.text_input("Enter Youtube Video Link here: ")

if youtube_link:
    video_id = youtube_link.split('=')[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

if st.button('Get notes'):
    transcript_text = extract_transcript(youtube_link)

    if transcript_text:
        summery = generate_gemini(transcript_text,prompt)

        st.markdown("## Detailed Notes : ")
        st.write(summery)



