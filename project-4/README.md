# Image Analyzer

A desktop application that uses Google's Gemini AI to analyze images based on custom prompts. Built with Python and Tkinter, this tool provides an intuitive graphical interface for image analysis tasks.

## Features

- **Custom Prompts**: Enter any prompt to guide the AI's analysis of your images
- **Easy Image Selection**: Browse and select images using a file dialog
- **Real-time Analysis**: Get detailed AI-powered analysis of your images
- **User-Friendly Interface**: Clean, modern GUI built with Tkinter
- **Secure API Key Management**: Uses environment variables to store your Google API key securely

## Requirements

- Python 3.7 or higher
- Google Generative AI API key
- Internet connection (for API calls)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd project-4
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   - Create a `.env` file in the project directory (if it doesn't exist)
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_actual_api_key_here
     ```
   - Replace `your_actual_api_key_here` with your actual Google Generative AI API key
   - You can get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

1. **Run the application:**
   ```bash
   python image_analyzer.py
   ```

2. **Using the GUI:**
   - **Enter a Prompt**: Type your analysis prompt in the "Prompt" field (e.g., "Describe the contents of the following image in detail", "What objects are in this image?", "Analyze the colors and composition")
   - **Select an Image**: Click the "Browse" button to select an image file, or manually type the path in the "Image Path" field
   - **Analyze**: Click the "Analyze Image" button to start the analysis
   - **View Results**: The analysis results will appear in the "Analysis Results" text area below

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)

## How It Works

1. The application loads your Google API key from the `.env` file
2. When you click "Analyze Image", it:
   - Validates the image path and prompt
   - Opens and processes the image
   - Sends the image and prompt to Google's Gemini 2.5 Flash Lite model
   - Displays the AI-generated analysis in the results area

## API Model

This tool uses Google's **Gemini 2.5 Flash Lite** model, which is optimized for fast image analysis tasks.

## Error Handling

The application includes comprehensive error handling for:
- Missing or invalid image files
- API connection issues
- Missing API keys
- Invalid prompts

## Security Notes

- **Never commit your `.env` file** to version control
- Keep your API key secure and don't share it publicly
- The `.env` file is already in `.gitignore` to prevent accidental commits

## Troubleshooting

- **"GOOGLE_API_KEY not found"**: Make sure your `.env` file exists and contains a valid API key
- **"File not found"**: Verify the image path is correct and the file exists
- **API Errors**: Check your internet connection and ensure your API key is valid and has sufficient quota

## Dependencies

- `google-generativeai`: Google's Generative AI SDK
- `Pillow`: Image processing library
- `python-dotenv`: Environment variable management
- `tkinter`: GUI framework (included with Python)

## License

This project is provided as-is for educational and personal use.

