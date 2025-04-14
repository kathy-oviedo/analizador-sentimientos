from textblob import TextBlob

def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity

    if polaridad > 0:
        return "Positivo 😊"
    elif polaridad < 0:
        return "Negativo 😠"
    else:
        return "Neutral 😐"

if __name__ == "__main__":
    entrada = input("Escribe una frase para analizar su sentimiento: ")
    resultado = analizar_sentimiento(entrada)
    print(f"Sentimiento: {resultado}")
