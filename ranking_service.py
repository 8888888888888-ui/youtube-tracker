"""YouTube ranking calculation service"""
import requests
import json
from datetime import datetime

# File to store channel history
CHANNEL_HISTORY_FILE = 'channel_history.json'

def load_channel_history():
    """Load channel history from file"""
    try:
        with open(CHANNEL_HISTORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'channel_names': [],
            'original_name': 'ActuallyDreamz',
            'channel_id': None,
            'ranking_history': []
        }

def save_channel_history(history):
    """Save channel history to file"""
    with open(CHANNEL_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def get_top_youtubers_count():
    """
    Get the total number of tracked YouTubers or fetch ranking data.
    
    Options:
    1. Use Social Blade API (requires API key)
    2. Use local database/cache
    3. Calculate based on known subscriber thresholds
    """
    # Placeholder: you can integrate with:
    # - Social Blade API
    # - VidIQ API
    # - Your own ranking database
    
    # For now, return a mock value
    return 1000000  # Approximate tracked channels

def calculate_rank(subscriber_count):
    """
    Calculate approximate ranking based on subscriber count.
    This is an estimation - actual ranking requires comparing with all channels.
    """
    # These are approximate thresholds (update based on real data)
    thresholds = {
        100000000: 10,          # 100M+ subs = top 10
        50000000: 50,           # 50M+ = top 50
        10000000: 200,          # 10M+ = top 200
        1000000: 1000,          # 1M+ = top 1000
        100000: 10000,          # 100K+ = top 10,000
        10000: 50000,           # 10K+ = top 50,000
    }
    
    for threshold, rank in sorted(thresholds.items(), reverse=True):
        if subscriber_count >= threshold:
            return rank
    
    return 100000  # Default estimate

def track_channel_name(youtube):
    """Track the current channel name"""
    history = load_channel_history()
    
    # Get current channel info
    channels_response = youtube.channels().list(
        part="snippet,statistics",
        mine=True
    ).execute()
    
    if not channels_response['items']:
        raise Exception("No channel found")
    
    channel = channels_response['items'][0]
    current_name = channel['snippet']['title']
    channel_id = channel['id']
    subscriber_count = int(channel['statistics'].get('subscriberCount', 0))
    
    # Update history
    history['channel_id'] = channel_id
    
    # Add to channel names list if new
    if not any(entry['name'] == current_name for entry in history['channel_names']):
        history['channel_names'].append({
            'name': current_name,
            'changed_at': datetime.now().isoformat()
        })
    
    # Add to ranking history
    history['ranking_history'].append({
        'timestamp': datetime.now().isoformat(),
        'channel_name': current_name,
        'subscribers': subscriber_count,
        'rank': calculate_rank(subscriber_count)
    })
    
    # Keep only last 365 entries (1 year of hourly updates)
    if len(history['ranking_history']) > 365 * 24:
        history['ranking_history'] = history['ranking_history'][-365*24:]
    
    save_channel_history(history)
    
    return channel, history

def format_description(subscriber_count, rank=None):
    """Format description with ranking info"""
    if rank is None:
        rank = calculate_rank(subscriber_count)
    
    # Format subscriber count with commas
    subs_formatted = f"{subscriber_count:,}"
    
    # Load history to show all channel names
    history = load_channel_history()
    all_names = " → ".join([entry['name'] for entry in history['channel_names']])
    
    # Create description
    description = f"🎥 I'm the #{rank:,} most subscribed YouTuber!\n"
    description += f"📊 {subs_formatted} subscribers\n"
    description += f"🚀 Channel: {all_names}\n"
    description += f"⏰ Last updated automatically"
    
    return description
