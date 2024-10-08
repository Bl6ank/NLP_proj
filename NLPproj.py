import re
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import tkinter as tk
from tkinter import filedialog, messagebox

# Load the multilingual spaCy model
nlp = spacy.load("xx_ent_wiki_sm")

# Expanded training data: Dictionary of topics with corresponding keywords
train_data = {
    "Sports": [
        "सचिन तेंदुलकर", "विराट कोहली", "कबड्डी", "महेंद्र सिंह धोनी", "रोहित शर्मा", "पीवी सिंधु", 
        "सौरव गांगुली", "विरेंद्र सहवाग", "बॉक्सिंग", "टेनिस", "क्रिकेट", "फुटबॉल", "हॉकी", 
        "बैडमिंटन", "एथलेटिक्स", "बास्केटबॉल", "गोल्फ", "स्विमिंग", "विंटर ओलंपिक्स", 
        "कोचिंग", "स्पोर्ट्स उपकरण", "फुटबॉल किट", "क्रिकेट बैट", "बैडमिंटन रैकेट"
    ],
    "Politics": [
        "किरण बेदी", "इंदिरा गांधी", "नरेंद्र मोदी", "कन्हैया कुमार", "शिवसेना", "आम आदमी पार्टी",
        "भाजपा", "कांग्रेस", "बसपा", "जदयू", "राहुल गांधी", "सोनिया गांधी", "ममता बनर्जी", 
        "नितीश कुमार", "पी चिदंबरम", "यशवंत सिन्हा", "सिर्फ सच्चाई", "तृणमूल कांग्रेस", 
        "लालू प्रसाद यादव", "शरद पवार", "आंध्र प्रदेश", "राजस्थान", "मध्य प्रदेश"
    ],
    "Literature": [
        "रवींद्रनाथ ठाकुर", "महादेवी वर्मा", "गुरुदेव रविंद्रनाथ ठाकुर", "फिराक गोरखपुरी", 
        "गुलजार", "सत्यजीत रे", "हरिवंश राय बच्चन", "कबीर", "कालिदास", "सूरदास", 
        "विस्वनाथ सचदेव", "धर्मवीर भारती", "जगदीश चंद्र चतुर्वेदी", "शमशेर बहादुर सिंह",
        "सुमित्रानंदन पंत", "प्रेमचंद", "निर्मल वर्मा", "शिवानी", "कन्हैया लाल नंदन", 
        "रामधारी सिंह 'दिनकर'", "सर्वेश्वर दयाल सक्सेना", "राजेंद्र यादव"
    ],
    "Music": [
        "ए. आर. रहमान", "लता मंगेशकर", "किशोर कुमार", "मोहमद रफी", "सोनू निगम", 
        "संगीतकार", "राग", "सिंफनी", "फिल्म संगीत", "शास्त्रीय संगीत", 
        "गज़ल", "भजन", "कर्नाटिक", "हिंदुस्तानी", "सुर", "ताला", "वाद्य यंत्र",
        "गिटार", "तबला", "साज़", "ड्रम", "पियानो"
    ],
    "Business": [
        "मुकेश अंबानी", "रतन टाटा", "नंदन नीलेकणी", "संदीप अग्रवाल", "इंफोसिस", 
        "टाटा समूह", "आदित्य बिड़ला समूह", "महिंद्रा एंड महिंद्रा", "फ्लिपकार्ट", 
        "ओला", "जियो", "स्नैपडील", "क्विकर", "जेडब्ल्यू मैरियट", "होटेल ताज", 
        "हिंदुस्तान यूनिलीवर", "कंपनी अधिनियम", "बाजार", "व्यापार", "मार्केटिंग"
    ],
    "Film": [
        "दीपिका पादुकोण", "अमिताभ बच्चन", "शाहरुख़ ख़ान", "सलमान ख़ान", "रानी मुखर्जी", 
        "काजोल", "आलिया भट्ट", "ऋतिक रोशन", "नसीरुद्दीन शाह", "अनुपम खेर", 
        "राजकुमार राव", "रणवीर सिंह", "आमिर खान", "करीना कपूर", "वीरेंद्र सहवाग", 
        "कला", "सिनेमाई", "फिल्मफेयर", "आस्कर", "सीरियल", "थियेटर"
    ],
    "Technology": [
        "मार्क जुकरबर्ग", "एलोन मस्क", "स्टीव जॉब्स", "गूगल", "एप्पल", 
        "फेसबुक", "इंटरनेट", "मोबाइल", "कंप्यूटर", "सॉफ्टवेयर", 
        "हैकर", "बिग डेटा", "आर्टिफिशियल इंटेलिजेंस", "क्लाउड कंप्यूटिंग", 
        "ब्लॉकचेन", "इलेक्ट्रॉनिक्स", "ड्रोन", "रोबोटिक्स", "साइबर सुरक्षा"
    ],
    "History": [
        "महात्मा गांधी", "जवाहरलाल नेहरू", "सुभाष चंद्र बोस", "सरदार वल्लभभाई पटेल", 
        "डॉ. भीमराव आंबेडकर", "मौलाना अबुल कलाम आज़ाद", "छत्रपति शिवाजी", 
        "कृष्णा दत्त", "गुरुदेव रवींद्रनाथ ठाकुर", "चाणक्य", "अकबर", 
        "शेर शाह सूरी", "मुगल साम्राज्य", "विजयनगर साम्राज्य", "युद्ध", "संविधान", 
        "भारतीय स्वतंत्रता संग्राम", "पश्चिमी प्रभाव", "हिंदू-मुस्लिम एकता", 
        "काले पानी", "भारतीय संस्कृति", "राष्ट्रीय ध्वज"
    ],
    "Geography": [
        "हिमालय", "गंगा नदी", "दिल्ली", "कोलकाता", "बैंगलोर", 
        "चंडीगढ़", "वाराणसी", "जोधपुर", "जयपुर", "रांची", 
        "आसमान", "गर्मी", "सर्दी", "बारिश", "तापमान", 
        "पर्यटन", "पर्यावरण", "जंगल", "नदियाँ", "पहाड़"
    ],
    "Health": [
        "आयुर्वेद", "योग", "स्वास्थ्य", "मेडिसिन", "डॉक्टर", 
        "पोषण", "फिटनेस", "व्यायाम", "रोग", "शारीरिक स्वास्थ्य", 
        "मानसिक स्वास्थ्य", "उपचार", "योगासन", "स्वस्थ आहार", 
        "मोहित", "शुगर", "हृदय रोग", "बीमारियाँ", "वजन", "जागरूकता"
    ],
    "Environment": [
        "जलवायु परिवर्तन", "वृक्षारोपण", "प्लास्टिक", "इकोलॉजी", 
        "संवर्धन", "वायु प्रदूषण", "जल प्रदूषण", "पारिस्थितिकी", 
        "संरक्षण", "भू-स्खलन", "वन्यजीव", "धरा", "पर्यावरणीय संकट", 
        "पारिस्थितिकी तंत्र", "पर्यावरणीय नीतियाँ", "सौर ऊर्जा", "नवीकरणीय ऊर्जा"
    ],
    "Agriculture": [
        "फसलों", "कृषि", "पशुपालन", "मौसम", "सिंचाई", 
        "बीज", "कृषि यंत्र", "फसल चक्र", "खेत", "खेतिहर मजदूर", 
        "सिंचाई", "जैविक खेती", "रासायनिक खाद", "उद्यानिकी", 
        "पशुपालन", "कृषि अनुसंधान", "धान", "गेहूं", "बागवानी"
    ],
    "Weather": [
        "गर्मी", "सर्दी", "बारिश", "तापमान", "मौसम विज्ञान", 
        "जलवायु", "तूफान", "मौसम पूर्वानुमान", "हवा", "बर्फ", 
        "बादल", "आंधी", "वृष्टि", "सूखा", "नमी", 
        "बर्फबारी", "तापमान रिकॉर्ड", "कुदरती आपदा", "अनियमित मौसम"
    ],
    "Travel": [
        "पर्यटन", "यात्रा", "सैर", "अंतरराष्ट्रीय यात्रा", "स्थानीय यात्रा", 
        "ट्रैवल एजेंसी", "होटल", "रेस्तरां", "संग्रहालय", "पर्यटन स्थल", 
        "रोड ट्रिप", "फ्लाइट", "सड़क यात्रा", "हाइकिंग", "ट्रेन यात्रा", 
        "बैकपैकिंग", "सेफ ट्रैवल", "सड़क के नियम", "यातायात", "यात्री"
    ],
}


# Prepare the training data
train_texts = []
train_labels = []

for topic, keywords in train_data.items():
    for keyword in keywords:
        train_texts.append(keyword)
        train_labels.append(topic)

# Create a Count Vectorizer to convert text to feature vectors
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_texts)
y_train = train_labels

# Train a Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Function to infer topics and their probabilities from Hindi text
def infer_topics(hindi_text):
    # Process the Hindi text with spaCy
    doc = nlp(hindi_text)
    # Extract tokens and remove stopwords
    words = [token.text for token in doc if not token.is_stop and not token.is_punct]
    
    text = ' '.join(words)
    X_test = vectorizer.transform([text])
    probabilities = classifier.predict_proba(X_test)[0]

    # Create a dictionary to hold topics and their probabilities
    topic_dict = {}
    for i, topic in enumerate(classifier.classes_):
        topic_dict[topic] = probabilities[i]

    # Sort topics by probability and select the top 3
    top_topics = dict(sorted(topic_dict.items(), key=lambda item: item[1], reverse=True)[:3])
    
    return top_topics

# Function to display inferred topics in a pop-up window
def show_inferred_topics(inferred_topics):
    # Prepare a string to display only the topics
    topics_str = "\n".join([f"{topic}" for topic in inferred_topics.keys()])
    
    #  to include probabilities, uncomment down comment up
    # topics_str = "\n".join([f"{topic}: {prob:.4f}" for topic, prob in inferred_topics.items()])
    
    # Show pop-up
    messagebox.showinfo("Top 3 Inferred Topics", topics_str)

# Function to open a file dialog and read the selected file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path: 
        with open(file_path, 'r', encoding='utf-8') as file:
            hindi_content = file.read()

        inferred_topics = infer_topics(hindi_content)
        show_inferred_topics(inferred_topics)

# Initialize the Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Call the file selection function
select_file()

# Destroy the Tkinter root window after processing
root.destroy()