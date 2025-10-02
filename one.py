import streamlit as st
import requests

st.title("AI Utility Tool")


mode = st.radio("Choose an AI Task", ["Image Generation (Hugging Face)", "Realtime Query (Groq)"])


if mode == "Image Generation (Hugging Face)":
    huggingface_api_key = st.text_input("Hugging Face API Key", type="password")
    st.markdown("🔑 [Get Hugging Face API Key](https://huggingface.co/settings/tokens)")
else:
    groq_api_key = st.text_input("Groq API Key", type="password")
    st.markdown("🔑 [Get Groq API Key](https://console.groq.com/)")


def generate_image(prompt, api_key):
    if not api_key:
        st.error("Please enter your Hugging Face API Key.")
        return None

    headers = {"Authorization": f"Bearer {api_key}"}
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    payload = {"inputs": prompt}

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.content  # Return image content
    elif response.status_code == 503:
        st.error("Hugging Face service is temporarily unavailable. Try again later.")
    else:
        st.error(f"API Error: {response.status_code}, Message: {response.text}")

    return None

def get_groq_response(query, api_key):
    if not api_key:
        st.error("Please enter your Groq API Key.")
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    api_url = "https://api.groq.com/openai/v1/chat/completions"

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": query}],
        "temperature": 0.7,
        "max_tokens": 500
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]

    elif response.status_code == 404:
        st.error("Invalid Groq API key or model not found. Check your API key and model name.")
    elif response.status_code == 429:
        st.warning("You exceeded your Groq API quota. Try again later.")
    else:
        st.error(f"Groq API Error: {response.status_code}, Message: {response.text}")

    return None


if mode == "Image Generation (Hugging Face)":
    st.subheader("Generate Images using Hugging Face")
    
    prompt = st.text_input("Enter Image Prompt")

    if st.button("Generate Image"):
        image = generate_image(prompt, huggingface_api_key)
        if image:
            st.image(image, caption="Generated Image")


elif mode == "Realtime Query (Groq)":
    st.subheader("Ask Anything using Groq API")

    query = st.text_area("Enter your question")

    if st.button("Get Answer"):
        answer = get_groq_response(query, groq_api_key)
        if answer:
            st.success(answer)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")



