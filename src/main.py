from analyzer.analyze_lyrics import start_analysis
from utils.read_song_metadata import read_metadata

def main():
    metadata = read_metadata()

    if metadata:
        start_analysis(metadata)
    else:
        print("Error: no se pudo obtener los metadatos de la canción.")
    
if __name__ == "__main__":
    main()