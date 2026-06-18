#!/usr/bin/env python3
"""Main script to update YouTube description with current ranking"""

import sys
import os
from youtube_api import authenticate, update_channel_description, get_subscriber_count
from ranking_service import track_channel_name, format_description

def main():
    try:
        # Authenticate with YouTube API
        print("🔐 Authenticating with YouTube API...")
        youtube = authenticate()
        
        # Track channel name changes
        print("📌 Tracking channel information...")
        channel, history = track_channel_name(youtube)
        current_name = channel['snippet']['title']
        print(f"✅ Channel: {current_name}")
        
        # Get current subscriber count
        print("📊 Fetching subscriber count...")
        subscriber_count = get_subscriber_count(youtube)
        
        if subscriber_count is None:
            print("⚠️  Could not fetch subscriber count (may be hidden in channel settings)")
            print("   Please enable 'Display subscriber count' in YouTube Studio settings")
            return 1
        
        print(f"✅ Current subscribers: {subscriber_count:,}")
        
        # Format new description
        print("📝 Generating new description...")
        new_description = format_description(subscriber_count)
        print(f"\nNew description:\n{new_description}\n")
        
        # Update YouTube channel
        print("🚀 Updating YouTube channel description...")
        update_channel_description(youtube, new_description)
        
        print("✨ Done!")
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
