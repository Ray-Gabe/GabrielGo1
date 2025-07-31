import os
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseService:
    def __init__(self):
        """Initialize Firebase connection"""
        self.db = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase with service account or use Firestore emulator"""
        try:
            # Check if Firebase is already initialized
            if firebase_admin._apps:
                app = firebase_admin.get_app()
                self.db = firestore.client(app)
                return
            
            # Try to initialize with service account
            firebase_creds = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
            if firebase_creds:
                try:
                    cred_dict = json.loads(firebase_creds)
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred)
                    self.db = firestore.client()
                    logging.info("Firebase initialized with service account")
                    return
                except Exception as e:
                    logging.warning(f"Failed to initialize with service account: {e}")
            
            # Check for environment project ID
            project_id = os.environ.get('FIREBASE_PROJECT_ID') or os.environ.get('GOOGLE_CLOUD_PROJECT')
            if project_id:
                try:
                    firebase_admin.initialize_app(options={'projectId': project_id})
                    self.db = firestore.client()
                    logging.info(f"Firebase initialized with project ID: {project_id}")
                    return
                except Exception as e:
                    logging.warning(f"Failed to initialize with project ID: {e}")
            
            # Gracefully handle no Firebase configuration
            logging.info("No Firebase configuration found - running without persistent memory")
            self.db = None
            
        except Exception as e:
            logging.warning(f"Firebase initialization failed - running without persistent memory: {e}")
            self.db = None
    
    def is_connected(self) -> bool:
        """Check if Firebase is properly connected"""
        return self.db is not None
    
    def get_user_id(self, user_name: str, session_id: str = None) -> str:
        """Generate a consistent user ID from name and session"""
        # Simple user ID generation - in production, use proper auth
        if user_name:
            return f"user_{user_name.lower().replace(' ', '_')}"
        elif session_id:
            return f"session_{session_id}"
        else:
            return f"anonymous_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    async def save_user_profile(self, user_id: str, name: str, **kwargs) -> bool:
        """Save or update user profile in Firestore"""
