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
st.image("AWL_Logo.png", width=150)  # This helps verify the image path

# Custom CSS for glow effect, shiny intro, and subtitle animation
st.markdown("""
    <style>
        /* General Styles */
        body {
            font-family: 'Helvetica', sans-serif;
            background: url('AWL_Logo.png') no-repeat center center fixed;
            background-size: cover;
            background-color: rgba(255, 255, 255, 0.7); /* Ensure text is readable */
            color: #333;
        }

        /* Centered container for logo and title */
        .header-container {
            text-align: center;
            margin-bottom: 20px; /* Space between logo and title */
        }

        /* Shiny and Animated Title with Subtle Glow Effect and Larger Font */
        .shiny-title {
            font-weight: bold;
            font-size: 96px;  /* Bigger font size */
            color: white;  /* White color for the text */
            background: linear-gradient(90deg, white, white) 0% 0% no-repeat;
            background-size: 100% 100%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.6), 0 0 16px rgba(255, 255, 255, 0.4);  /* Subtle Glow effect */
            position: relative;
            overflow: hidden;
            animation: fadeInBounce 3s ease;
            transition: transform 0.3s ease; /* Smooth transition for hover effect */
        }

        .shiny-title::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.8), transparent);
            animation: shiny 4s ease-in-out forwards; /* Play only once, for 4 seconds */
        }

        /* Keyframe animation for shiny effect, 4 seconds and then stops */
        @keyframes shiny {
            0% {
                left: -100%;
            }
            100% {
                left: 100%;
            }
        }

        /* Keyframe animation for title bounce */
        @keyframes fadeInBounce {
            0% { opacity: 0; transform: translateY(-20px); }
            50% { opacity: 0.5; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* Interactive movement effect on hover for title */
        .shiny-title:hover {
            transform: scale(1.05) translateY(-10px); /* Slight zoom and move up effect */
            text-shadow: 0 0 12px rgba(255, 255, 255, 0.8), 0 0 24px rgba(255, 255, 255, 0.5); /* Slight increase in glow on hover */
        }

        /* Subtitle Animation for smooth pop-up effect */
        .subtitle {
            font-size: 24px;
            color: #FFF;
            opacity: 0;
            animation: subtitlePopUp 4s ease-in-out forwards; /* Animate once with ease */
            margin-top: -10px;
            text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5); /* Shadow for depth */
        }

        @keyframes subtitlePopUp {
            0% {
                opacity: 0;
                transform: translateY(20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Interactive Button Styling */
        .stButton button {
            background: linear-gradient(90deg, #FF0000, #1E90FF);  /* Red to Blue gradient */
            border: none;
            color: white;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
            transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth transition */
        }

        /* Interactive movement effect on hover for buttons */
        .stButton button:hover {
            transform: scale(1.05) translateY(-3px); /* Slight zoom and move up effect */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Add shadow on hover */
        }

        /* Text Area Styling */
        .stTextArea textarea {
            border-radius: 12px;
            border: 1px solid #ccc;
            font-size: 14px;
            padding: 12px;
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

# Header container with title and subtitle
st.markdown("""
    <div class="header-container">
        <h1 class="shiny-title">AWL AI Web Scraper</h1>
        <p class="subtitle">Exclusively for AWL</p>  <!-- Subtitle pop-up under the title -->
    </div>
""", unsafe_allow_html=True)

# URL input
url = st.text_input("Enter a website URL:")

# Scrape button
if st.button("Scrape Site"):
    if url:
        st.write("Scraping the website...")

        # Scrape the website
        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)

        st.session_state.dom_content = cleaned_content

        # Show DOM content in an expandable section
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)
    else:
        st.error("Please enter a valid URL.")

# Parsing logic
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
