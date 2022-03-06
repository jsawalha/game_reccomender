import re
import bs4 as BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize,sent_tokenize, WhitespaceTokenizer, wordpunct_tokenize, TreebankWordTokenizer
from nltk.stem import WordNetLemmatizer
import nltk
import warnings
warnings.filterwarnings('ignore')

#Import stopword list from NLTK
# stopword_list=nltk.corpus.stopwords.words('english')


#NLP CLEANING FUNCTIONS
def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# Removing the square brackets
def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

# Removing the noisy text
def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text

# 2) Remove special characters
def rem_special_char(text, remove_digits=True):
    pattern = r'[^a-zA-z0-9\s]'
    text = re.sub(pattern, '', text)
    return text

# 3) Remove all upper case words
def lower_case(text):
    text = text.lower()
    return text

# 4) Stemming
def stemmer(text):
    ps = PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text

# 5) Lemmatization
def lemmo(text):
    lemma = WordNetLemmatizer()
    text = lemma.lemmatize(text)
    return text

# 6) Stop-words - Tokenization
def stop_word_token(text, is_lower_case=True):
    tk = WhitespaceTokenizer()
    text = tk.tokenize(text)
    filtered_text = [w for w in text if w not in stopword_list]
    filtered_text = ' '.join(filtered_text)
    return filtered_text
