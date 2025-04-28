import json
import subprocess
import os
import sys
import argparse
from datetime import timedelta

def convert_ms_to_srt_time(ms):
    """Convert milliseconds to SRT time format (HH:MM:SS,mmm)"""
    td = timedelta(milliseconds=ms)
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = td.seconds % 60
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def json_to_srt(json_file, output_srt):
    """Convert YouTube JSON subtitle format to SRT format"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    raw_events = []
    for event in data['events']:
        if 'segs' not in event:
            continue
            
        text = ''.join(seg.get('utf8', '') for seg in event['segs'])
        if not text.strip():
            continue
        
        if not event.get('aAppend'):
            raw_events.append({
                'start': event['tStartMs'],
                'duration': event.get('dDurationMs', 3000),
                'text': text.strip()
            })
        elif raw_events:
            raw_events[-1]['text'] += text
    
    subtitle_events = []
    for i, event in enumerate(raw_events):
        start_time = event['start']
        end_time = start_time + event['duration']
        
        if i < len(raw_events) - 1:
            next_start = raw_events[i + 1]['start']
            if end_time >= next_start:
                end_time = next_start - 10
        
        if end_time > start_time:
            subtitle_events.append({
                'start': start_time,
                'end': end_time,
                'text': event['text']
            })
    
    with open(output_srt, 'w', encoding='utf-8') as f:
        for i, event in enumerate(subtitle_events, 1):
            start_time = convert_ms_to_srt_time(event['start'])
            end_time = convert_ms_to_srt_time(event['end'])
            
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{event['text']}\n\n")
    
    return len(subtitle_events)

def embed_subtitles(video_file, srt_file, output_file):
    """Embed subtitles into video using ffmpeg"""
    cmd = [
        'ffmpeg',
        '-i', video_file,
        '-vf', f'subtitles={srt_file}',
        '-c:a', 'copy',
        output_file
    ]
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description='Embed subtitles into video')
    parser.add_argument('--source', required=True,
                      help='Input video file')
    parser.add_argument('--json', required=True,
                      help='JSON subtitle file')
    parser.add_argument('--output', required=True,
                      help='Output video file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"Error: Video file '{args.source}' not found!")
        sys.exit(1)
        
    if not os.path.exists(args.json):
        print(f"Error: JSON subtitle file '{args.json}' not found!")
        sys.exit(1)
    
    srt_file = os.path.splitext(args.output)[0] + '.srt'
    print("Converting JSON to SRT format...")
    num_subtitles = json_to_srt(args.json, srt_file)
    print(f"Generated {num_subtitles} subtitles in {srt_file}")
    
    print("Embedding subtitles into video...")
    embed_subtitles(args.source, srt_file, args.output)
    print(f"Done! Output saved as {args.output}")

if __name__ == "__main__":
    main() 