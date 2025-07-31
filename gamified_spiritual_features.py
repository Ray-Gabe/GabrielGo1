"""
GABE Faith-in-Action Gamified Framework
Transforms spiritual growth into engaging, trackable experiences
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

# Global session storage for user data
SESSION_STORAGE = {}

class GamifiedSpiritualFeatures:
    def __init__(self):
        """Initialize the gamified spiritual features system"""
        self.logger = logging.getLogger(__name__)
        
        # XP and Level System
        self.level_thresholds = {
            'Seed': 0,
            'Shepherd': 10,
            'Disciple': 25,
            'Warrior': 50,
            'Servant Leader': 100
        }
        
        # Badge definitions
        self.badge_definitions = {
            'Faith Seed': {'description': 'Started your spiritual journey', 'requirement': 'first_action'},
            'Devotion Keeper': {'description': '3-day devotion streak', 'requirement': 'devotion_streak_3'},
            'Prayer Warrior': {'description': '5 prayer challenges completed', 'requirement': 'prayer_count_5'},
            'Verse Sage': {'description': 'Mastered 10 verses', 'requirement': 'verse_mastery_10'},
            'Peacemaker': {'description': 'Completed a forgiveness prayer challenge', 'requirement': 'forgiveness_prayer'},
            'Shepherd': {'description': 'Reached Shepherd level', 'requirement': 'level_shepherd'},
            'Scripture Explorer': {'description': 'Completed 5 adventure stops', 'requirement': 'adventure_stops_5'},
            'Emotional Resilience': {'description': 'Completed mood missions for 3 different emotions', 'requirement': 'mood_variety_3'}
        }
        
        # Morning & Evening Devotions
        self.devotions = {
            'morning': {
                'title': '🌅 MORNING DEVOTION: "Start with Stillness"',
                'greeting': 'Good morning, {name}. Time to pray and start your day with God.',
                'verse_reference': 'Psalm 46:10',
                'verse_text': 'Be still, and know that I am God.',
                'word': 'Before the day demands your attention, God invites you to stillness — not silence, but surrender. In the quiet, He strengthens you. You don\'t need to rush — you need to rest in Him first.',
                'application': 'Take 3 deep breaths and whisper, "God, I trust You today." That moment of peace can shape your entire day.',
                'prayer': 'Heavenly Father, Thank You for the gift of today. As I step into the hours ahead, I choose stillness before You. Quiet my heart from anxiety and noise. Help me walk with peace, speak with kindness, and act with purpose. Let my choices reflect Your wisdom and my heart reflect Your love. Be with me in every moment, and lead me where You want me to go. In Jesus\' name, Amen.',
                'closing': '📖 GABE is always by your side — you are never alone.'
            },

        'evening': {
                'title': '🌙 EVENING DEVOTION: "Lay It Down"',
                'greeting': 'Good evening, {name}. You\'ve made it through the day. Let\'s pause, reflect, and pray together.',
                'verse_reference': '1 Peter 5:7',
                'verse_text': 'Cast all your anxiety on Him because He cares for you.',
                'word': 'You weren\'t meant to carry it all. God sees the pressure, the thoughts, the unspoken worries — and He\'s asking you to hand them over. Lay it down tonight. Rest in Him, not just sleep.',
                'application': 'Think of one thing that\'s weighing on your heart. Whisper it to God. Then say, "I release it to You." That\'s how peace begins.',
                'prayer': 'Lord, Thank You for walking with me today — through the joys, the stress, the quiet moments, and the mess. As night falls, I place my thoughts, my worries, and my plans in Your hands. Refresh my body, renew my mind, and fill my heart with peace. Watch over me and those I love. In Jesus\' name, Amen.',
                'closing': '💬 GABE is always by your side — you are never alone.'
            }
        }
        
        # Prayer challenges bank
        self.prayer_challenges = [
            'Pray for someone who has hurt you and ask God to heal their heart',
            'Write a prayer of gratitude for three specific things from this week',
            'Pray for a world leader or someone in authority',
            'Ask God to show you how to serve someone in need today',
            'Pray for wisdom in a decision you\'re facing',
            'Thank God for His faithfulness in a difficult season of your life',
            'Pray for peace in a conflict situation you know about',
            'Ask God to help you forgive yourself for something you regret'
        ]
        
        # Interactive Bible Studies
        self.bible_studies = {
            'trusting_god': {
                'id': 'trusting_god',
                'title': 'Trusting God in Difficult Times',
                'description': 'Learn to trust God\'s goodness when life feels uncertain',
                'sessions': 3,
                'duration': '10-15 min each',
                'xp_reward': 5,
                'sessions_data': [
                    {
                        'session_number': 1,
                        'title': 'God\'s Faithfulness in the Past',
                        'scripture_reference': 'Psalm 77:11-12',
                        'scripture_text': 'I will remember the deeds of the Lord; yes, I will remember your miracles of long ago. I will consider all your works and meditate on all your mighty deeds.',
                        'questions': [
                            'When have you seen God\'s faithfulness in your life before?',
                            'How can remembering God\'s past goodness help you trust Him today?',
                            'What "mighty deeds" of God do you want to remember more often?'
                        ],
                        'xp_reward': 4
    def get_user_progress(self, session_id: str) -> Dict:
        """Get complete user progress overview"""
        user_data = self.get_user_data(session_id)
        
        # Calculate next level progress
        current_level = user_data['level']
        level_names = list(self.level_thresholds.keys())
        current_index = level_names.index(current_level)
        
        if current_index < len(level_names) - 1:
            next_level = level_names[current_index + 1]
            next_threshold = self.level_thresholds[next_level]
            progress_to_next = user_data['xp'] - self.level_thresholds[current_level]
            needed_for_next = next_threshold - self.level_thresholds[current_level]
            progress_percentage = (progress_to_next / needed_for_next) * 100
        else:
            next_level = "Max Level Reached"
            progress_percentage = 100
        
        return {
            'level': user_data['level'],
            'xp': user_data['xp'],
            'next_level': next_level,
            'progress_percentage': min(progress_percentage, 100),
            'badges': user_data['badges'],
            'streaks': user_data['streak'],
            'adventure_progress': user_data['scripture_adventure_position'],
            'verses_mastered': len(user_data['verse_mastery_progress']),
            'total_actions': user_data['total_actions'],
            'studies_completed': user_data.get('studies_completed', 0)
        }
