from mutagen.easyid3 import EasyID3
from mutagen import File
from pathlib import Path

def detect_audio_format(file_path):
    try:
        # Use mutagen to load the file
        audio = File(file_path)
        if audio is None:
            print("Unsupported or invalid file format.")
            return None

        # Detect the format based on the file type
        file_format = audio.__class__.__name__  # Class name corresponds to the format
        extension = {
            "MP3": "mp3",
            "MP4": "mp4",
            "ID3": "mp3",  # For files with only ID3 metadata
            "FLAC": "flac",
            "WAVE": "wav",
            "OggVorbis": "ogg",
            "OggOpus": "opus",
        }.get(file_format, None)  # Default to None if format is unknown

        if extension:
            print(f"Detected format: {file_format}, extension: .{extension}")
            return extension
        else:
            print(f"Unsupported format: {file_format}")
            return None
    except Exception as e:
        print(f"Error detecting format: {e}")
        return None

def read_metadata():
    try:
        print("Analizando metadatos de la canción...")

        # Get the root directory (assumes this file is in the `utils` folder)
        root_dir = Path(__file__).resolve().parents[2]

        # Build the path to the sample folder
        sample_dir = root_dir / "sample"

        # Example: Access a file in the sample folder
        sample_file_path = next(sample_dir.glob("*"), None)
        if not sample_file_path:
            print("No audio files found in the sample directory.")
            return

        # Detect file format and adjust extension if needed
        detected_extension = detect_audio_format(sample_file_path)
        if detected_extension:
            sample_file_path = sample_file_path.with_suffix(f".{detected_extension}")

        print(f"Sample file path with detected extension: {sample_file_path}")

        # Load the file (supports multiple formats)
        audio = File(sample_file_path, easy=True)

        if audio:
            print("Metadata:")
            print(f"- Title: {audio.get('title')}")
            print(f"- Artist: {audio.get('artist')}")
            print(f"- Album: {audio.get('album')}")
            print(f"- Genre: {audio.get('genre')}")

            metadata = {
                "title": audio.get("title", [None])[0],
                "artist": audio.get("artist", [None])[0],
                "album": audio.get("album", [None])[0],
                "genre": audio.get("genre", [None])[0]
            }
            return metadata

        else:
            print("No metadata found or unsupported file format.")
    except Exception as e:
        print(f"Error reading metadata: {e}")
