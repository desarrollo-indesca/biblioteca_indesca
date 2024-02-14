import yake
from nltk.corpus import stopwords
from PyPDF2 import PdfReader

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

IDIOMA = 'spanish'
STOPWORDS = set(stopwords.words(IDIOMA))

def cargar_texto_publicacion(publicacion, desde = 0, hasta = -1):
    pdf = PdfReader(publicacion.archivo)

    text = ""
    for page in pdf.pages[desde:hasta]:
        text += page.extract_text()

    text = text.upper().replace("INVESTIGACIÓN Y DESARROLLO", '').replace("INFORME FINAL", '').replace(publicacion.titulo.upper(), '')

    return text

def generar_descriptores_publicacion(publicacion):
    try:
        # Primero, obtener el texto. Arrojar None si ocurre un error
        text = cargar_texto_publicacion(publicacion)

        # Segundo, crear objeto KeywordExtractor
        kw_exractor = yake.KeywordExtractor(top=10, stopwords=STOPWORDS, n = 3)

        # Tercero, obtener palabras clave y devolver 
        keywords = [x[0] for x in kw_exractor.extract_keywords(text)]
        print(keywords)
        return keywords
    
    except Exception as e:
        print(str(e))
        return None
    
def generar_resumen_publicacion(publicacion):
    try:
        text = cargar_texto_publicacion(publicacion, 5, -1)
        parser = PlaintextParser.from_string(text, Tokenizer('spanish'))
        stemmer = Stemmer('spanish')
        summarizer = LsaSummarizer(stemmer)

        N = 10
        summary = ""
        for sentence in summarizer(parser.document, N):
            summary += str(sentence)
            summary += " "   

        return summary     
    except Exception as e:
        print(str(e))
        return None