import os
import json
import logging
from datetime import datetime
from openai import OpenAI
try:
    import google.generativeai as genai
except ImportError:
    genai = None

class GabeCompanion:
    """
    A naturally conversational spiritual AI companion that feels personal and intuitive,
    like talking to a wise, caring friend who remembers your conversations and truly listens.
    """
    
    def __init__(self):
        # Initialize Gemini as primary
        self.gemini_client = None
        self.openai_client = None
        
        gemini_key = os.environ.get("GEMINI_API_KEY")
        if gemini_key and genai and hasattr(genai, 'configure'):
            try:
                genai.configure(api_key=gemini_key)
                if hasattr(genai, 'GenerativeModel'):
                    self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                    self.gemini_client = True
                    logging.info("Gemini client initialized successfully (PRIMARY)")
                else:
                    logging.warning("GenerativeModel not available in genai module")
                    self.gemini_client = None
            except Exception as e:
                logging.warning(f"Failed to initialize Gemini: {e}")
                self.gemini_client = None
        else:
            self.gemini_client = None
        
        # Initialize OpenAI as fallback
        openai_key = os.environ.get("OPENAI_API_KEY")
        if openai_key:
            try:
                self.openai_client = OpenAI(api_key=openai_key)
                # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
                self.openai_model = "gpt-4o"
                logging.info("OpenAI client initialized successfully (FALLBACK)")
            except Exception as e:
                logging.warning(f"Failed to initialize OpenAI: {e}")
        
        if not self.gemini_client and not self.openai_client:
            logging.warning("No AI provider available - conversations will use fallback responses")
        
        # Dynamic conversation memory
        self.conversation_memory = {}
        self.user_insights = {}
        
        # Enhanced conversation state management (inspired by JavaScript flow)
        self.conversation_states = {}
        self.voice_mode_enabled = {}  # Track voice mode per session
        self.chunked_conversations = {}  # Track multi-part conversations
        
        # Story continuation system
        self.story_contexts = {}  # Track ongoing stories per session
        },
        'david_goliath': {
            'parts': [
                "Let me tell you about young David facing Goliath. Everyone saw a giant - David saw an opportunity to trust God.",
                "David didn't need fancy armor. He picked up smooth stones because he knew God was with him.",
                "One stone, one shot, and the giant fell. Not because David was strong, but because God was faithful.",
                "Your giants might feel overwhelming, but God sees them differently. Would you like another story or a prayer?"
            ],
            'name': 'David and Goliath'
        },
        'red_sea': {
            'parts': [
                "Picture Moses at the Red Sea - enemy behind, impossible waters ahead. Nowhere to go but through.",
                "God didn't remove the sea. He split it wide open, making a way where there was no way.",
                "The same waters that saved God's people destroyed their enemies. God turned the obstacle into victory.",
                "Sometimes God doesn't remove our challenges - He walks through them with us. Want to hear more?"
            ],
            'name': 'Moses and the Red Sea'
        }
    }
    
    def is_story_request(self, user_message):
        """Check if user is asking for a Bible story"""
        story_keywords = [
            'story', 'tell me a story', 'bible story', 'share a story',
            'david and goliath', 'moses', 'daniel', 'noah', 'jesus',
            'parable', 'tell me about', 'biblical story'
        ]
        return any(keyword in user_message.lower() for keyword in story_keywords)
    
    def get_response(self, user_message, user_name=None, age_range=None, conversation_history=None, session_id=None):
        """
        Get a naturally conversational response that feels personal and intuitive
        """
        try:
            # PRAYER INTERCEPTOR: Handle prayer requests immediately with short prayers
            user_msg_lower = user_message.lower().strip()
            name = user_name or 'friend'
            
            logging.info(f"INTERCEPTOR: Checking message: '{user_msg_lower}'")
            
            # If it's a direct prayer request, return short prayer immediately
            prayer_triggers = ['pray for', 'say a prayer', 'please pray', 'pray that', 'father help', 'lord help', 'jesus help', 'pray with me', 'can you pray']
            triggered = any(trigger in user_msg_lower for trigger in prayer_triggers)
            
            logging.info(f"INTERCEPTOR: Prayer triggers found: {triggered}")
        # Filter out recently used responses
        available_prompts = [prompt for prompt in gentle_prompts 
                           if not any(prompt in recent for recent in recent_auto_responses)]

        # If all prompts were used recently, use the full list
        if not available_prompts:
            available_prompts = gentle_prompts

        import random
        return random.choice(available_prompts)
    
    def toggle_voice_mode(self, session_id, enable=None):
        """Toggle or set voice mode for a session"""
        if session_id not in self.voice_mode_enabled:
            self.voice_mode_enabled[session_id] = False
        
        if enable is not None:
            self.voice_mode_enabled[session_id] = enable
        else:
            self.voice_mode_enabled[session_id] = not self.voice_mode_enabled[session_id]
        
        return self.voice_mode_enabled[session_id]
    
    def chunk_and_deliver_response(self, full_text, user_name="friend", max_chars=350):
        """Split long responses into digestible chunks for voice-friendly delivery"""
        if not full_text or len(full_text) <= max_chars:
            return [full_text] if full_text else []
        
        # Split by sentences first
        import re
        sentences = re.split(r'[.!?]+', full_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ''
        
        for sentence in sentences:
            if sentence and not sentence[-1] in '.!?':
                sentence += '.'
            
            test_chunk = current_chunk + ' ' + sentence if current_chunk else sentence
            
            if len(test_chunk) <= max_chars:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [full_text]


