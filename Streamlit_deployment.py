import os
import openai
#import pinecone
import streamlit as st


# Assuming you have the secrets manager setup, otherwise replace with your own method for securing API keys
openai.api_key = "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"

#pinecone.init(
#	api_key='',
#	environment='us-east-1'
#)
#index = pinecone.Index('movies')


# AI FUNCTIONS
def generate_blog(topic, additional_text):
    prompt = f"""
    You are a copy writer with years of experience writing impactful blog that converge and help elevate brands.
    Your task is to write a blog on any topic system provides to you. Make sure to write in a format that works for Medium.
    Each blog should be separated into segments that have titles and subtitles. Each paragraph should be three sentences long.
    
    Topic: {topic}
    Additional pointers: {additional_text}
    """
    
    response = openai.Completion.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = prompt,
        max_tokens = 700,
        temperature = 0.9
    )

    return response.choices[0].text.strip()

def generate_image(prompt, number_of_images=1):
    response = openai.Image.create(
        prompt=prompt,
        size="1024x1024",
        n=number_of_images,
    )

    return response
    
# END OF AI FUNCTIONS

st.set_page_config(layout="wide")
st.title("OpenAI API Webapp")
st.sidebar.title("AI Apps")
ai_app = st.sidebar.radio("Choose an AI App", ("Blog Generator", "Image Generator", "Movie Recommender"))

if ai_app == "Blog Generator":
    st.header("Blog Generator")
    st.write("Input a topic to generate a blog about it using OpenAI API")
    
    topic = st.text_area("Topic", height=30)
    additional_text = st.text_area("Additional Text", height=30)
    
    if st.button("Generate Blog"):
        with st.spinner("Generating..."):
            value = generate_blog(topic, additional_text)
            st.text_area("Generated blog", value, height=700)

elif ai_app == "Image Generator":
    st.header("Image Generator")
    st.write("Add a prompt to generate an image using OpenAI API and DALLE model")

    prompt = st.text_area("Enter text for image generation:")

    number_of_images = st.slider("Choose the number of images to generate", 1, 5, 1) 
    if st.button("Generate Image") and prompt != "":
        with st.spinner("Generating..."):
            outputs = generate_image(prompt, number_of_images)
            for output in outputs.data:
                st.image(output.url)
    
elif ai_app == "Movie Recommender":
    st.header("Movie Recommender")
    st.write("Describe a movie that you would like to see")

    movie_description = st.text_area("Movie Description", height=30)
    
    if st.button("Get Movie Recommendations") and movie_description != "":
        with st.spinner("Generating..."):
            user_vector = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=movie_description)

            user_vector = user_vector.data[0].embedding
            matches = index.query(
                      user_vector,
                      top_k=10,
                      include_metadata=True)

            for match in matches:
                st.write(match['metadata']['title'])