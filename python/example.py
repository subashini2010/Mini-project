import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from gtts import gTTS

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to summarize text
def summarize_text(text, num_sentences=5):
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    word_freq = Counter()
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word not in stop_words:
                word_freq[word] += 1
    sentence_scores = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_freq:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_freq[word]
                else:
                    sentence_scores[sentence] += word_freq[word]
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    summarized_text = ' '.join(summarized_sentences)
    return summarized_text

# Function to generate voice-over
def generate_voice_over(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("summary_audio.mp3")
    print("Voice-over saved as summary_audio.mp3")

# Main function
def main():
    pdf_file_path = input("Enter the path to the PDF file: ")
    try:
        with open(pdf_file_path, 'rb') as pdf_file:
            text = extract_text_from_pdf(pdf_file)
            summary = summarize_text(text)
            print("Summary:")
            print(summary)
            generate_voice_over(summary)
    except FileNotFoundError:
        print("The specified file was not found. Please check the path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Execute the program
if __name__ == "__main__":
    main()


