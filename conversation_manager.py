# This module manages conversation state with users
import time

class ConversationManager:
    def __init__(self):
        # Stores user states: {user_id: {'options': [...], 'timestamp': time.time()}}
        self.user_states = {}

    def update_user_options(self, user_id, options):
        self.user_states[user_id] = {
            'options': options,
            'timestamp': time.time()
        }

    def get_user_options(self, user_id):
        user_state = self.user_states.get(user_id)
        if user_state and time.time() - user_state['timestamp'] < 3600:
            return user_state['options']
        else:
            return None

    def clear_user_state(self, user_id):
        if user_id in self.user_states:
            del self.user_states[user_id]
