import nltk # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import string

nltk.download('punkt')
nltk.download('stopwords')
faq_data = {
    "What is your return policy?": "You can return any item within 30 days of purchase.",
    "How can I contact customer support?": "You can contact our support team via email at support@example.com.",
    "Where is your company located?": "Our headquarters are in New York City.",
    "What payment methods do you accept?": "We accept credit cards, PayPal, and UPI.",
    "Do you ship internationally?": "Yes, we ship to most countries worldwide."
}

def preprocess(text):
    text = text.lower()
    tokens = wordpunct_tokenize(text)
    tokens = [word for word in tokens if word not in string.punctuation]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return " ".join(tokens)

questions = list(faq_data.keys())
preprocessed_questions = [preprocess(q) for q in questions]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(preprocessed_questions)

def get_answer(user_input):
    user_input_processed = preprocess(user_input)
    user_vector = vectorizer.transform([user_input_processed])
    similarity = cosine_similarity(user_vector, tfidf_matrix)
    max_index = similarity.argmax()
    if similarity[0, max_index] > 0.3:
        return list(faq_data.values())[max_index]
    else:
        return "Sorry, I couldn't find a relevant answer to your question."

def on_ask():
    user_q = entry.get()
    if user_q.lower() == 'exit':
        root.destroy()
        return
    response = get_answer(user_q)
    chat_log.config(state='normal')
    chat_log.insert(tk.END, "You: " + user_q + "\n")
    chat_log.insert(tk.END, "Bot: " + response + "\n\n")
    chat_log.config(state='disabled')
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("FAQ Chatbot")

chat_log = tk.Text(root, state='disabled', width=80, height=20, wrap='word')
chat_log.pack(padx=10, pady=10)

entry = tk.Entry(root, width=70)
entry.pack(padx=10, pady=5)

ask_button = tk.Button(root, text="Ask", command=on_ask)
ask_button.pack()

root.mainloop()
