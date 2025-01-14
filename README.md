# music-emotion-analyzer

 Music classification ML project.

## Setup

1. Create conda environment:
   ```bash
   conda env create -f environment.yml
   ```

2. Activate environment:
   ```bash
   conda activate music-analyzer
   ```

3. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the main script:
```bash
python src/main.py
```
