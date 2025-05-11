### Secure Data Storage and Retrieval System

I'll create a Streamlit application that securely stores and retrieves data using in-memory storage with encryption and authentication features.

```python project="Secure Data Storage" file="app.py"
...
```

## System Features and Security Implementation

### 1. In-Memory Data Storage

- All data is stored in Streamlit's session state as an in-memory dictionary
- Data structure follows the required format with encrypted text and hashed passkeys
- Each data entry has a unique UUID identifier


### 2. Security Measures

#### Encryption and Hashing

- **Passkey Hashing**: Uses SHA-256 to securely hash all passkeys
- **Data Encryption**: Implements Fernet symmetric encryption (from the cryptography library)
- **Unique Keys**: Each session generates a unique encryption key


#### Authentication System

- Tracks failed authentication attempts (limited to 3)
- Forces reauthorization after 3 failed attempts
- Provides visual feedback on remaining attempts
- Simple login page for reauthorization


### 3. User Interface

#### Home Page

- Clear navigation options
- System statistics
- Security information


#### Store Data Page

- Text area for data input
- Passkey creation with confirmation
- Secure storage with feedback
- Unique Data ID generation and display


#### Retrieve Data Page

- Data ID and passkey input
- Decryption and display of retrieved data
- Failed attempt tracking and warnings
- Automatic redirection to login after 3 failed attempts


#### Admin View (for demonstration)

- Lists all stored data entries (without revealing actual content)
- Shows timestamps and partial hashes


### 4. User Experience

- Clean, modern UI with consistent styling
- Clear feedback messages (success, error, warning)
- Intuitive navigation
- Security status indicators

## Security Notes

1. This system operates entirely in memory - all data is lost when the session ends
2. For a production system, additional security measures would be recommended:

1. More sophisticated authentication
2. Rate limiting
3. Session timeouts
4. Audit logging
5. Stronger encryption key management





The application meets all the specified requirements while providing a user-friendly interface and robust security features."# Secure-Data-Encryption-System-Using-Streamlit" 
"# Assignment_5" 
