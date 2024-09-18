import streamlit as st 
from scrape import (
    scrape_website, 
    split_dom_content,
    clean_body_content,
    extract_body_content,
)
from parse import parse_with_ollama

# Set page config for better aesthetics
st.set_page_config(page_title="AWL AI Web Scraper", page_icon="🕸️", layout="wide")

# Test to ensure the logo loads
st.image("AWL_BUDDY_Logo.png", width=300)  # Increased the width to 300px

# Custom CSS for modern and exciting text effects
st.markdown("""
    <style>
        /* General Styles */
        body {
            font-family: 'Helvetica', sans-serif;
            color: #333;
        }

        /* Centered container for logo and title */
        .header-container {
            text-align: center;
            margin-top: -50px; /* Shift the container higher */
        }

        /* Image styling for AWL Buddy */
        .awl-buddy-img {
            width: 300px;
            margin-bottom: 20px; /* Increased bottom margin */
        }

        /* Bigger and Higher Title */
        .shiny-title {
            font-weight: bold;
            font-size: 80px;  /* Increased font size */
            color: #333;
            text-shadow: 0 0 8px rgba(0, 0, 0, 0.3), 0 0 16px rgba(0, 0, 0, 0.2);
            margin-top: -40px; /* Further shift title higher */
        }

        /* Modern and Exciting Subtitle */
        .subtitle {
            font-size: 24px;
            color: #333;
            margin-top: -20px; /* Shift subtitle higher */
            line-height: 1.5;
        }

        /* Gradient Footer */
        footer {
            text-align: center;
            padding: 10px;
            font-size: 14px;
            background: linear-gradient(90deg, #FF0000, #1E90FF);  /* Red to Blue gradient */
            color: white;
            position: fixed;
            width: 100%;
            bottom: 0;
        }
    </style>
""", unsafe_allow_html=True)

# Header container with title and message
st.markdown("""
    <div class="header-container">
        <h1 class="shiny-title">AWL AI Web Scraper</h1>
        <p class="subtitle">
            <strong>🎉 It's AWL Buddy's First Day at Work! 🎉</strong><br>
            🚀 AWL Buddy is currently preparing for his big day at AWL.<br>
            ⏳ Stay tuned as AWL Buddy will let you know when he clocks in.<br>
            🙏 Thank you for the warm welcome!
        </p>
    </div>
""", unsafe_allow_html=True)

# Parsing logic if DOM content exists
if "dom_content" in st.session_state:
    parse_description = st.text_area("(App Created by: AWL) Describe what you want to parse:")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)
        else:
            st.error("Please enter a description to parse.")

# Footer section
st.markdown("""
    <footer>
        AWL AI Web Scraper Tool © 2024 | Only Used by The American Wholesalers LLC
    </footer>
""", unsafe_allow_html=True)
