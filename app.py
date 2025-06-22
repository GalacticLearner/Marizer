import streamlit as st
from transformers import pipeline
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
ytt_api = YouTubeTranscriptApi()

def main():
    st.title("Marizer")
    st.markdown("### YouTube Video Summarizer")

    url = st.text_input("Enter YouTube URL")
    transcript = process_transcript(fetch_transcript(video_id(url)))
    summary = summarizer(transcript)
    st.text(summary)

def video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]
        elif parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]
        elif parsed_url.path.startswith("/v/"):
            return parsed_url.path.split("/")[2]
    return None

def fetch_transcript(id_):
    return ytt_api.fetch(id_).snippets

def process_transcript(transcript):
    text = ""
    for snippet in transcript.snippets:
        text.append(snippet.text)
    return text