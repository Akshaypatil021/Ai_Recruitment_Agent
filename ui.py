import streamlit as st
import pandas as pd
import base64
import io
import matplotlib.pyplot as plt

def setup_page():
    """Apply custom CSS and setup page (without setting page config)"""
    # Apply custom CSS only
    apply_custom_css()
    
    # Add local logo handling via JavaScript
    st.markdown(""" 
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Try to load the logo, if it fails, show fallback
            var logoImg = document.querySelector('.logo-image');
            if (logoImg) {
                logoImg.onerror = function() {
                    var logoContainer = document.querySelector('.logo-container');
                    if (logoContainer) {
                        logoContainer.innerHTML = '<div style="font-size: 40px;">💨</div>';
                    }
                };
            }
        });
    </script>
    """, unsafe_allow_html=True)


def display_header():
    try:
        with open("euron.jpg", "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
            logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Euron Logo" class="logo-image" style="max-height: 100px;">'
    except:
        logo_html = '<div style="font-size: 50px; text-align: center;">💨</div>'
    
    st.markdown(f"""
    <div class="main-header">
        <div class="header-container">
            <div class="logo-container" style="text-align: center; margin-bottom: 20px;">
                {logo_html}
            </div>
            <div class="title-container" style="text-align: center;">
                <h1>Recruitment Agent</h1>
                <p>Smart Resume Analysis & Interview Preparation System</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_header():
    try:
        with open("euron.jpg", "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
            logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Euron Logo" class="logo-image" style="max-height: 100px;">'
    except:
        logo_html = '<div style="font-size: 50px; text-align: center;">🤖</div>'
    
    st.markdown(f"""
    <div class="main-header">
        <div class="header-container">
            <div class="logo-container" style="text-align: center; margin-bottom: 20px;">
                {logo_html}
            </div>
            <div class="title-container" style="text-align: center;">
                <h1>Recruitment Agent</h1>
                <p>Smart Resume Analysis & Interview Preparation System</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
