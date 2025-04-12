import streamlit as st
import hashlib
import base64
import os
from cryptography.fernet import Fernet
import time
import uuid

# Set page configuration
st.set_page_config(
    page_title="Secure Data Storage",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2563EB;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #3B82F6;
    }
    .success-card {
        background-color: #ECFDF5;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #10B981;
    }
    .warning-card {
        background-color: #FEF2F2;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #EF4444;
    }
    .btn-primary {
        background-color: #2563EB;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
        color: #6B7280;
        font-size: 0.8rem;
    }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0

if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = True

if 'encryption_key' not in st.session_state:
    # Generate a random encryption key for the session
    st.session_state.encryption_key = Fernet.generate_key()
    st.session_state.cipher_suite = Fernet(st.session_state.encryption_key)

# Helper functions for security operations
def hash_passkey(passkey):
    """Hash the passkey using SHA-256"""
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(data):
    """Encrypt data using Fernet symmetric encryption"""
    return st.session_state.cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    """Decrypt data using Fernet symmetric encryption"""
    try:
        return st.session_state.cipher_suite.decrypt(encrypted_data.encode()).decode()
    except Exception:
        return None

def verify_passkey(stored_hash, provided_passkey):
    """Verify if the provided passkey matches the stored hash"""
    provided_hash = hash_passkey(provided_passkey)
    return provided_hash == stored_hash

def generate_data_id():
    """Generate a unique ID for stored data"""
    return str(uuid.uuid4())

# Navigation functions
def navigate_to_page(page):
    st.session_state.page = page

# Login page
def login_page():
    st.markdown("<h1 class='main-header'>🔒 Secure Data System</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Authentication Required</h2>", unsafe_allow_html=True)
    st.write("You need to authenticate to continue.")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Simple authentication - in a real app, this would be more secure
        if username and password:
            st.session_state.is_authenticated = True
            st.session_state.failed_attempts = 0
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")
    st.markdown("</div>", unsafe_allow_html=True)

# Home page
def home_page():
    st.markdown("<h1 class='main-header'>🔒 Secure Data Storage System</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Welcome to Secure Data Storage</h2>", unsafe_allow_html=True)
    st.write("""
    This system allows you to securely store and retrieve sensitive data using encryption.
    All data is stored in memory and protected with your unique passkey.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Store New Data", key="store_btn"):
            navigate_to_page("store")
    
    with col2:
        if st.button("Retrieve Data", key="retrieve_btn"):
            navigate_to_page("retrieve")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display stats about stored data
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>System Statistics</h2>", unsafe_allow_html=True)
    st.write(f"Total stored data entries: {len(st.session_state.stored_data)}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Security information
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Security Information</h2>", unsafe_allow_html=True)
    st.write("""
    - All data is encrypted using Fernet symmetric encryption
    - Passkeys are hashed using SHA-256
    - Data is stored in memory only (not persisted)
    - Three failed retrieval attempts will require reauthorization
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Store data page
def store_data_page():
    st.markdown("<h1 class='main-header'>🔒 Store Secure Data</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Enter Data to Encrypt</h2>", unsafe_allow_html=True)
    
    # Data input form
    data_to_store = st.text_area("Enter the data you want to store securely", height=150)
    passkey = st.text_input("Create a passkey for this data", type="password")
    confirm_passkey = st.text_input("Confirm passkey", type="password")
    
    if st.button("Store Data Securely"):
        if not data_to_store or not passkey:
            st.error("Please provide both data and a passkey.")
        elif passkey != confirm_passkey:
            st.error("Passkeys do not match. Please try again.")
        else:
            # Generate a unique ID for this data
            data_id = generate_data_id()
            
            # Hash the passkey
            hashed_passkey = hash_passkey(passkey)
            
            # Encrypt the data
            encrypted_data = encrypt_data(data_to_store)
            
            # Store the data with its hashed passkey
            st.session_state.stored_data[data_id] = {
                "encrypted_text": encrypted_data,
                "passkey": hashed_passkey,
                "timestamp": time.time()
            }
            
            st.markdown("<div class='success-card'>", unsafe_allow_html=True)
            st.success(f"Data stored successfully! Your Data ID is: {data_id}")
            st.info("Please save this ID as you will need it to retrieve your data.")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Display the data ID prominently
            st.markdown(f"<h3 style='text-align: center; background-color: #EFF6FF; padding: 1rem; border-radius: 5px;'>Data ID: {data_id}</h3>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Back button
    if st.button("Back to Home"):
        navigate_to_page("home")

# Retrieve data page
def retrieve_data_page():
    st.markdown("<h1 class='main-header'>🔒 Retrieve Secure Data</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Access Your Encrypted Data</h2>", unsafe_allow_html=True)
    
    # Show warning if there have been failed attempts
    if st.session_state.failed_attempts > 0:
        st.markdown("<div class='warning-card'>", unsafe_allow_html=True)
        st.warning(f"Failed attempts: {st.session_state.failed_attempts}/3. After 3 failed attempts, you will need to re-authenticate.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Data retrieval form
    data_id = st.text_input("Enter your Data ID")
    passkey = st.text_input("Enter your passkey", type="password")
    
    if st.button("Retrieve Data"):
        if not data_id or not passkey:
            st.error("Please provide both Data ID and passkey.")
        elif data_id not in st.session_state.stored_data:
            st.error("Data ID not found. Please check and try again.")
            st.session_state.failed_attempts += 1
        else:
            stored_item = st.session_state.stored_data[data_id]
            
            # Verify the passkey
            if verify_passkey(stored_item["passkey"], passkey):
                # Decrypt the data
                decrypted_data = decrypt_data(stored_item["encrypted_text"])
                
                if decrypted_data:
                    st.markdown("<div class='success-card'>", unsafe_allow_html=True)
                    st.success("Data retrieved successfully!")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Display the decrypted data
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown("<h3>Your Decrypted Data:</h3>", unsafe_allow_html=True)
                    st.text_area("Decrypted content", value=decrypted_data, height=150, disabled=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Reset failed attempts on success
                    st.session_state.failed_attempts = 0
                else:
                    st.error("Error decrypting data. The data may be corrupted.")
                    st.session_state.failed_attempts += 1
            else:
                st.error("Incorrect passkey. Please try again.")
                st.session_state.failed_attempts += 1
        
        # Check if max attempts reached
        if st.session_state.failed_attempts >= 3:
            st.markdown("<div class='warning-card'>", unsafe_allow_html=True)
            st.error("Maximum failed attempts reached. You need to re-authenticate.")
            st.markdown("</div>", unsafe_allow_html=True)
            st.session_state.is_authenticated = False
            time.sleep(1)  # Short delay for user to see the message
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Back button
    if st.button("Back to Home"):
        navigate_to_page("home")

# List all stored data (admin view - in a real app, this would be protected)
def list_data_page():
    st.markdown("<h1 class='main-header'>🔒 Admin: Stored Data</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>All Stored Data Entries</h2>", unsafe_allow_html=True)
    
    if not st.session_state.stored_data:
        st.info("No data has been stored yet.")
    else:
        for data_id, data_item in st.session_state.stored_data.items():
            st.markdown(f"<h3>Data ID: {data_id}</h3>", unsafe_allow_html=True)
            st.write(f"Timestamp: {time.ctime(data_item['timestamp'])}")
            st.write("Passkey hash: ", data_item["passkey"][:10] + "...")
            st.write("Encrypted data: ", data_item["encrypted_text"][:20] + "...")
            st.markdown("---")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Back button
    if st.button("Back to Home"):
        navigate_to_page("home")

# Main app logic
def main():
    # Initialize the page in session state if it doesn't exist
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    
    # Check authentication status
    if not st.session_state.is_authenticated:
        login_page()
        return
    
    # Create a sidebar for navigation
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>Navigation</h2>", unsafe_allow_html=True)
        
        if st.button("🏠 Home"):
            navigate_to_page("home")
        
        if st.button("💾 Store Data"):
            navigate_to_page("store")
        
        if st.button("🔍 Retrieve Data"):
            navigate_to_page("retrieve")
        
        # Admin button - in a real app, this would be protected
        if st.button("👑 Admin View"):
            navigate_to_page("admin")
        
        # Logout button
        if st.button("🚪 Logout"):
            st.session_state.is_authenticated = False
            st.rerun()
        
        # Display current security status
        st.markdown("---")
        st.markdown("<h3 style='text-align: center;'>Security Status</h3>", unsafe_allow_html=True)
        
        auth_status = "✅ Authenticated" if st.session_state.is_authenticated else "❌ Not Authenticated"
        st.markdown(f"<p style='text-align: center;'>{auth_status}</p>", unsafe_allow_html=True)
        
        attempts_color = "#10B981" if st.session_state.failed_attempts == 0 else "#EF4444"
        st.markdown(f"<p style='text-align: center; color: {attempts_color};'>Failed Attempts: {st.session_state.failed_attempts}/3</p>", unsafe_allow_html=True)
    
    # Render the appropriate page based on the current state
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "store":
        store_data_page()
    elif st.session_state.page == "retrieve":
        retrieve_data_page()
    elif st.session_state.page == "admin":
        list_data_page()
    else:
        home_page()
    
    # Footer
    st.markdown("<div class='footer'>", unsafe_allow_html=True)
    st.markdown("Secure Data Storage System | Built with Streamlit", unsafe_allow_html=True)
    st.markdown("All data is stored in memory and will be lost when the session ends", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
