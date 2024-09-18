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
            background: url('AWL_BUDDY_Logo.png') no-repeat center center fixed;
            background-size: cover;
            background-color: rgba(255, 255, 255, 0.7); /* Ensure text is readable */
            color: #333;
        }

        /* Centered container for logo and title */
        .header-container {
            text-align: center;
            margin-bottom: 20px; /* Space between logo and title */
            margin-top: -50px; /* Shift the container higher */
        }

        /* Image styling for AWL Buddy */
        .awl-buddy-img {
            width: 300px; /* Increased logo size to 300px */
            border-radius: 10px;
            margin-bottom: 10px; /* Reduced bottom margin */
        }

        /* Shiny and Animated Title with Subtle Glow Effect and Larger Font */
        .shiny-title {
            font-weight: bold;
            font-size: 72px;  /* Adjusted font size */
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
            margin-top: -30px; /* Shift the title higher */
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

        /* Modern and Exciting Subtitle with Animation */
        .subtitle {
            font-size: 24px;
            color: #FFF;
            opacity: 0;
            animation: subtitlePopUp 4s ease-in-out forwards, pulse 2s infinite; /* Animate once and pulse */
            margin-top: -20px; /* Shift subtitle higher */
            text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5); /* Shadow for depth */
            line-height: 1.5; /* Line height for better readability */
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

        /* Pulse animation for exciting effect */
        @keyframes pulse {
            0% {
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
            }
            50% {
                text-shadow: 0 0 20px rgba(255, 255, 255, 1);
            }
            100% {
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
            }
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

# Header container with title, image, and message
st.markdown("""
    <div class="header-container">
        <img src="AWL_BUDDY_Logo.png" class="awl-buddy-img" alt="AWL Buddy">
        <h1 class="shiny-title">AWL AI Web Scraper</h1>
        <p class="subtitle">
            <strong>🎉 It's AWL Buddy's First Day at Work! 🎉</strong><br>
            🚀 AWL Buddy is currently preparing for his big day at AWL.<br>
            ⏳ Stay tuned as AWL Buddy will let you know when he clocks in.<br>
            🙏 Thank you for the warm welcome!
        </p>  <!-- Subtitle message -->
    </div>
""", unsafe_allow_html=True)

# Scrape logic removed

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
