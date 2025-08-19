import wave
import sys
import os
import struct

class AudioProcessor:
    def __init__(self):
        self.supported_formats = ['.wav']
    
    def get_audio_info(self, file_path):
        try:
            with wave.open(file_path, 'rb') as wav_file:
                info = {
                    'filename': os.path.basename(file_path),
                    'channels': wav_file.getnchannels(),
                    'sample_width': wav_file.getsampwidth(),
                    'frame_rate': wav_file.getframerate(),
                    'frames': wav_file.getnframes(),
                    'duration': wav_file.getnframes() / wav_file.getframerate(),
                    'file_size': os.path.getsize(file_path)
                }
                return info
        except Exception as e:
            print(f"Error getting audio info: {e}")
            return None
    
    def convert_to_mono(self, input_path, output_path):
        try:
            with wave.open(input_path, 'rb') as input_wav:
                if input_wav.getnchannels() == 1:
                    print("Audio is already mono")
                    return False
                
                params = input_wav.getparams()
                frames = input_wav.readframes(params.nframes)
                
                audio_data = struct.unpack(f'{params.nframes * params.nchannels}h', frames)
                
                mono_data = []
                for i in range(0, len(audio_data), params.nchannels):
                    mono_sample = sum(audio_data[i:i+params.nchannels]) // params.nchannels
                    mono_data.append(mono_sample)
                
                with wave.open(output_path, 'wb') as output_wav:
                    output_wav.setnchannels(1)
                    output_wav.setsampwidth(params.sampwidth)
                    output_wav.setframerate(params.framerate)
                    output_wav.writeframes(struct.pack(f'{len(mono_data)}h', *mono_data))
                
                print(f"Converted {input_path} to mono: {output_path}")
                return True
        except Exception as e:
            print(f"Error converting to mono: {e}")
            return False
    
    def change_volume(self, input_path, output_path, volume_factor):
        try:
            with wave.open(input_path, 'rb') as input_wav:
                params = input_wav.getparams()
                frames = input_wav.readframes(params.nframes)
                
                if params.sampwidth == 2:
                    audio_data = struct.unpack(f'{params.nframes * params.nchannels}h', frames)
                    adjusted_data = [int(sample * volume_factor) for sample in audio_data]
                    adjusted_data = [max(-32768, min(32767, sample)) for sample in adjusted_data]
                    packed_data = struct.pack(f'{len(adjusted_data)}h', *adjusted_data)
                else:
                    print("Only 16-bit audio is supported")
                    return False
                
                with wave.open(output_path, 'wb') as output_wav:
                    output_wav.setparams(params)
                    output_wav.writeframes(packed_data)
                
                print(f"Adjusted volume by factor {volume_factor}: {output_path}")
                return True
        except Exception as e:
            print(f"Error changing volume: {e}")
            return False
    
    def trim_audio(self, input_path, output_path, start_time, end_time):
        try:
            with wave.open(input_path, 'rb') as input_wav:
                params = input_wav.getparams()
                
                start_frame = int(start_time * params.framerate)
                end_frame = int(end_time * params.framerate)
                
                input_wav.setpos(start_frame)
                frames_to_read = end_frame - start_frame
                frames = input_wav.readframes(frames_to_read)
                
                with wave.open(output_path, 'wb') as output_wav:
                    output_wav.setparams(params)
                    output_wav.writeframes(frames)
                
                print(f"Trimmed audio from {start_time}s to {end_time}s: {output_path}")
                return True
        except Exception as e:
            print(f"Error trimming audio: {e}")
            return False
    
    def concatenate_audio(self, file_list, output_path):
        try:
            output_frames = []
            params = None
            
            for file_path in file_list:
                with wave.open(file_path, 'rb') as wav_file:
                    if params is None:
                        params = wav_file.getparams()
                    else:
                        current_params = wav_file.getparams()
                        if (current_params.nchannels != params.nchannels or
                            current_params.sampwidth != params.sampwidth or
                            current_params.framerate != params.framerate):
                            print(f"Audio parameters mismatch in {file_path}")
                            return False
                    
                    frames = wav_file.readframes(wav_file.getnframes())
                    output_frames.append(frames)
            
            with wave.open(output_path, 'wb') as output_wav:
                output_wav.setparams(params)
                for frames in output_frames:
                    output_wav.writeframes(frames)
            
            print(f"Concatenated {len(file_list)} files: {output_path}")
            return True
        except Exception as e:
            print(f"Error concatenating audio: {e}")
            return False
    
    def generate_silence(self, output_path, duration, sample_rate=44100, channels=1):
        try:
            num_frames = int(duration * sample_rate)
            silence_data = [0] * (num_frames * channels)
            
            with wave.open(output_path, 'wb') as wav_file:
                wav_file.setnchannels(channels)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(struct.pack(f'{len(silence_data)}h', *silence_data))
            
            print(f"Generated {duration}s of silence: {output_path}")
            return True
        except Exception as e:
            print(f"Error generating silence: {e}")
            return False
    
    def generate_tone(self, output_path, frequency, duration, sample_rate=44100, amplitude=0.3):
        try:
            import math
            
            num_frames = int(duration * sample_rate)
            tone_data = []
            
            for i in range(num_frames):
                t = i / sample_rate
                sample = int(amplitude * 32767 * math.sin(2 * math.pi * frequency * t))
                tone_data.append(sample)
            
            with wave.open(output_path, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(struct.pack(f'{len(tone_data)}h', *tone_data))
            
            print(f"Generated {frequency}Hz tone for {duration}s: {output_path}")
            return True
        except Exception as e:
            print(f"Error generating tone: {e}")
            return False
    
    def analyze_audio(self, file_path):
        try:
            with wave.open(file_path, 'rb') as wav_file:
                params = wav_file.getparams()
                frames = wav_file.readframes(params.nframes)
                
                if params.sampwidth == 2:
                    audio_data = struct.unpack(f'{params.nframes * params.nchannels}h', frames)
                    
                    max_amplitude = max(abs(sample) for sample in audio_data)
                    avg_amplitude = sum(abs(sample) for sample in audio_data) / len(audio_data)
                    
                    analysis = {
                        'max_amplitude': max_amplitude,
                        'avg_amplitude': avg_amplitude,
                        'dynamic_range': max_amplitude / max(avg_amplitude, 1),
                        'peak_percentage': (max_amplitude / 32767) * 100,
                        'rms': (sum(sample**2 for sample in audio_data) / len(audio_data)) ** 0.5
                    }
                    
                    return analysis
                else:
                    print("Only 16-bit audio analysis is supported")
                    return None
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            return None

if __name__ == "__main__":
    processor = AudioProcessor()
    
    if len(sys.argv) < 2:
        print("Usage: python audio_processor.py <command> [args]")
        print("Commands:")
        print("  info <file>                           - Get audio information")
        print("  mono <input> <output>                 - Convert to mono")
        print("  volume <input> <output> <factor>      - Change volume (0.5=half, 2.0=double)")
        print("  trim <input> <output> <start> <end>   - Trim audio (seconds)")
        print("  concat <output> <file1> <file2> ...   - Concatenate audio files")
        print("  silence <output> <duration>           - Generate silence")
        print("  tone <output> <frequency> <duration>  - Generate tone")
        print("  analyze <file>                        - Analyze audio properties")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "info":
        if len(sys.argv) < 3:
            print("Usage: info <file>")
            sys.exit(1)
        
        info = processor.get_audio_info(sys.argv[2])
        if info:
            print(f"\nAudio Information:")
            print(f"Filename: {info['filename']}")
            print(f"Channels: {info['channels']}")
            print(f"Sample Width: {info['sample_width']} bytes")
            print(f"Frame Rate: {info['frame_rate']} Hz")
            print(f"Duration: {info['duration']:.2f} seconds")
            print(f"Total Frames: {info['frames']:,}")
            print(f"File Size: {info['file_size']:,} bytes")
    
    elif command == "mono":
        if len(sys.argv) < 4:
            print("Usage: mono <input> <output>")
            sys.exit(1)
        processor.convert_to_mono(sys.argv[2], sys.argv[3])
    
    elif command == "volume":
        if len(sys.argv) < 5:
            print("Usage: volume <input> <output> <factor>")
            sys.exit(1)
        processor.change_volume(sys.argv[2], sys.argv[3], float(sys.argv[4]))
    
    elif command == "trim":
        if len(sys.argv) < 6:
            print("Usage: trim <input> <output> <start_time> <end_time>")
            sys.exit(1)
        processor.trim_audio(sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5]))
    
    elif command == "concat":
        if len(sys.argv) < 5:
            print("Usage: concat <output> <file1> <file2> [file3...]")
            sys.exit(1)
        processor.concatenate_audio(sys.argv[3:], sys.argv[2])
    
    elif command == "silence":
        if len(sys.argv) < 4:
            print("Usage: silence <output> <duration>")
            sys.exit(1)
        processor.generate_silence(sys.argv[2], float(sys.argv[3]))
    
    elif command == "tone":
        if len(sys.argv) < 5:
            print("Usage: tone <output> <frequency> <duration>")
            sys.exit(1)
        processor.generate_tone(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
    
    elif command == "analyze":
        if len(sys.argv) < 3:
            print("Usage: analyze <file>")
            sys.exit(1)
        
        analysis = processor.analyze_audio(sys.argv[2])
        if analysis:
            print(f"\nAudio Analysis:")
            print(f"Max Amplitude: {analysis['max_amplitude']}")
            print(f"Average Amplitude: {analysis['avg_amplitude']:.1f}")
            print(f"Dynamic Range: {analysis['dynamic_range']:.2f}")
            print(f"Peak Percentage: {analysis['peak_percentage']:.1f}%")
            print(f"RMS: {analysis['rms']:.1f}")
    
    else:
        print("Unknown command")
