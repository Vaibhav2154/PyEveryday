import yt_dlp
import os
import sys
import json
from urllib.parse import urlparse, parse_qs

class YouTubeDownloader:
    def __init__(self, download_path="downloads"):
        self.download_path = download_path
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        self.ydl_opts_video = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'format': 'best[height<=720]',
            'writeinfojson': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
        }
        
        self.ydl_opts_audio = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        self.ydl_opts_playlist = {
            'outtmpl': os.path.join(download_path, '%(playlist_title)s/%(title)s.%(ext)s'),
            'format': 'best[height<=720]',
            'writeinfojson': True,
        }
    
    def get_video_info(self, url):
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                
                video_info = {
                    'title': info.get('title', 'Unknown'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', 'Unknown'),
                    'description': info.get('description', '')[:500] + '...' if info.get('description') else '',
                    'formats': len(info.get('formats', [])),
                    'thumbnail': info.get('thumbnail', ''),
                    'webpage_url': info.get('webpage_url', url)
                }
                
                return video_info
        
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
    
    def download_video(self, url, quality='720p'):
        quality_map = {
            '1080p': 'best[height<=1080]',
            '720p': 'best[height<=720]',
            '480p': 'best[height<=480]',
            '360p': 'best[height<=360]',
            'best': 'best',
            'worst': 'worst'
        }
        
        opts = self.ydl_opts_video.copy()
        opts['format'] = quality_map.get(quality, 'best[height<=720]')
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
                print(f"Video downloaded successfully in {quality} quality")
                return True
        
        except Exception as e:
            print(f"Error downloading video: {e}")
            return False
    
    def download_audio(self, url, format='mp3'):
        opts = self.ydl_opts_audio.copy()
        
        if format == 'wav':
            opts['postprocessors'][0]['preferredcodec'] = 'wav'
        elif format == 'm4a':
            opts['postprocessors'][0]['preferredcodec'] = 'm4a'
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
                print(f"Audio downloaded successfully in {format} format")
                return True
        
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return False
    
    def download_playlist(self, url, max_videos=None, video_quality='720p'):
        opts = self.ydl_opts_playlist.copy()
        opts['format'] = f'best[height<={video_quality[:-1]}]' if video_quality != 'best' else 'best'
        
        if max_videos:
            opts['playlistend'] = max_videos
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
                print("Playlist downloaded successfully")
                return True
        
        except Exception as e:
            print(f"Error downloading playlist: {e}")
            return False
    
    def download_subtitles_only(self, url, languages=['en']):
        opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': languages,
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
        }
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
                print("Subtitles downloaded successfully")
                return True
        
        except Exception as e:
            print(f"Error downloading subtitles: {e}")
            return False
    
    def get_available_formats(self, url):
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                video_formats = []
                audio_formats = []
                
                for fmt in formats:
                    if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                        video_formats.append({
                            'format_id': fmt['format_id'],
                            'ext': fmt['ext'],
                            'resolution': fmt.get('resolution', 'Unknown'),
                            'filesize': fmt.get('filesize', 'Unknown')
                        })
                    elif fmt.get('acodec') != 'none':
                        audio_formats.append({
                            'format_id': fmt['format_id'],
                            'ext': fmt['ext'],
                            'abr': fmt.get('abr', 'Unknown'),
                            'filesize': fmt.get('filesize', 'Unknown')
                        })
                
                return {'video': video_formats, 'audio': audio_formats}
        
        except Exception as e:
            print(f"Error getting formats: {e}")
            return None
    
    def download_custom_format(self, url, format_id):
        opts = {
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'format': format_id,
        }
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
                print(f"Downloaded with format ID: {format_id}")
                return True
        
        except Exception as e:
            print(f"Error downloading with custom format: {e}")
            return False
    
    def search_youtube(self, query, max_results=10):
        search_url = f"ytsearch{max_results}:{query}"
        
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(search_url, download=False)
                
                results = []
                for entry in info.get('entries', []):
                    results.append({
                        'title': entry.get('title', 'Unknown'),
                        'uploader': entry.get('uploader', 'Unknown'),
                        'duration': entry.get('duration', 0),
                        'view_count': entry.get('view_count', 0),
                        'url': entry.get('webpage_url', ''),
                        'thumbnail': entry.get('thumbnail', '')
                    })
                
                return results
        
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def format_duration(self, seconds):
        if not seconds:
            return "Unknown"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def display_video_info(self, info):
        if not info:
            print("No video information available")
            return
        
        print("\n" + "="*60)
        print("📹 VIDEO INFORMATION")
        print("="*60)
        print(f"Title: {info['title']}")
        print(f"Uploader: {info['uploader']}")
        print(f"Duration: {self.format_duration(info['duration'])}")
        print(f"Views: {info['view_count']:,}" if info['view_count'] else "Views: Unknown")
        print(f"Upload Date: {info['upload_date']}")
        print(f"Available Formats: {info['formats']}")
        print(f"URL: {info['webpage_url']}")
        print("="*60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_downloader.py <command> [args]")
        print("Commands:")
        print("  info <url>                    - Get video information")
        print("  video <url> [quality]         - Download video (quality: 1080p, 720p, 480p, 360p)")
        print("  audio <url> [format]          - Download audio (format: mp3, wav, m4a)")
        print("  playlist <url> [max_videos]   - Download playlist")
        print("  subtitles <url> [languages]   - Download subtitles only")
        print("  formats <url>                 - Show available formats")
        print("  custom <url> <format_id>      - Download with custom format")
        print("  search <query> [max_results]  - Search YouTube")
        sys.exit(1)
    
    command = sys.argv[1]
    downloader = YouTubeDownloader()
    
    if command == "info":
        if len(sys.argv) < 3:
            print("Usage: info <url>")
            sys.exit(1)
        
        url = sys.argv[2]
        info = downloader.get_video_info(url)
        downloader.display_video_info(info)
    
    elif command == "video":
        if len(sys.argv) < 3:
            print("Usage: video <url> [quality]")
            sys.exit(1)
        
        url = sys.argv[2]
        quality = sys.argv[3] if len(sys.argv) > 3 else '720p'
        downloader.download_video(url, quality)
    
    elif command == "audio":
        if len(sys.argv) < 3:
            print("Usage: audio <url> [format]")
            sys.exit(1)
        
        url = sys.argv[2]
        format_type = sys.argv[3] if len(sys.argv) > 3 else 'mp3'
        downloader.download_audio(url, format_type)
    
    elif command == "playlist":
        if len(sys.argv) < 3:
            print("Usage: playlist <url> [max_videos]")
            sys.exit(1)
        
        url = sys.argv[2]
        max_videos = int(sys.argv[3]) if len(sys.argv) > 3 else None
        downloader.download_playlist(url, max_videos)
    
    elif command == "subtitles":
        if len(sys.argv) < 3:
            print("Usage: subtitles <url> [languages]")
            sys.exit(1)
        
        url = sys.argv[2]
        languages = sys.argv[3].split(',') if len(sys.argv) > 3 else ['en']
        downloader.download_subtitles_only(url, languages)
    
    elif command == "formats":
        if len(sys.argv) < 3:
            print("Usage: formats <url>")
            sys.exit(1)
        
        url = sys.argv[2]
        formats = downloader.get_available_formats(url)
        
        if formats:
            print("\nAvailable Video Formats:")
            for fmt in formats['video'][:10]:
                print(f"ID: {fmt['format_id']}, Resolution: {fmt['resolution']}, Ext: {fmt['ext']}")
            
            print("\nAvailable Audio Formats:")
            for fmt in formats['audio'][:5]:
                print(f"ID: {fmt['format_id']}, ABR: {fmt['abr']}, Ext: {fmt['ext']}")
    
    elif command == "custom":
        if len(sys.argv) < 4:
            print("Usage: custom <url> <format_id>")
            sys.exit(1)
        
        url = sys.argv[2]
        format_id = sys.argv[3]
        downloader.download_custom_format(url, format_id)
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: search <query> [max_results]")
            sys.exit(1)
        
        query = " ".join(sys.argv[2:-1]) if len(sys.argv) > 3 and sys.argv[-1].isdigit() else " ".join(sys.argv[2:])
        max_results = int(sys.argv[-1]) if len(sys.argv) > 3 and sys.argv[-1].isdigit() else 10
        
        results = downloader.search_youtube(query, max_results)
        
        if results:
            print(f"\nSearch Results for: {query}")
            print("="*60)
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['title']}")
                print(f"   Uploader: {result['uploader']}")
                print(f"   Duration: {downloader.format_duration(result['duration'])}")
                print(f"   Views: {result['view_count']:,}" if result['view_count'] else "   Views: Unknown")
                print(f"   URL: {result['url']}")
                print("-" * 60)
        else:
            print("No results found")
    
    else:
        print("Unknown command")
