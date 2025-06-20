import streamlit as st
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

ytt_api = YouTubeTranscriptApi(    proxy_config=GenericProxyConfig(
        http_url="http://user:pass@my-custom-proxy.org:port",
        https_url="https://user:pass@my-custom-proxy.org:port",
    ))

def main():
    st.title("Marizer")
    st.markdown("### YouTube Video Summarizer")

    url = st.text_input("Enter YouTube URL")
    transcript = fetch_transcript(video_id(url))


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
    print(ytt_api.fetch(id_).snippets)

fetch_transcript("god33lcDUmM")