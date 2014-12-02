#! /usr/bin/python

import sys, re

def process_text(textfile, keywords, dictionary, prob_file=False):
    sentences = textfile.split(".")
    filtered_sentences = []
    for sentence in sentences:
        for word in keywords:
            if re.search(word, sentence):
                context = has_context(sentence, keywords, dictionary)
                if len(context) > 0:
                    filtered_sentences.append(context)
    filtered_sentences = [" ".join(contexts) for contexts in filtered_sentences]
    filtered_sentences = list(set(filtered_sentences))
    if prob_file:
        for i in range(len(filtered_sentences)):
            filtered_sentences[i] = "Context Words: " + filtered_sentences[i] + "\n" + prob_file
    return "\n".join(filtered_sentences)

def has_context(sentence, keywords, dictionary):
    sentence_words = sentence.split()
    if len(sentence) < 5:
        return []
    for i in range(4, len(sentence_words)):
        for word in keywords:
            if re.search(word, sentence_words[i]):
                context = sentence_words[(i-4):(i)]
                if context_allowed(context, dictionary):
                    return context
    return []     

def context_allowed(context, dictionary):
    for word in context:
        if word not in dictionary:
            return False
    return True

def main():
    if len(sys.argv) < 5:
        print("Usage: extract_context.py <dictionary> <text> <keywords> <output_file> \n")
        return

    dict_file = open(sys.argv[1], 'r')
    text_file = open(sys.argv[2], 'r')
    keyword_file = open(sys.argv[3], 'r')
    out_file = open(sys.argv[4], 'w')

    dictionary_string = dict_file.read()
    dictionary = dictionary_string.split()
    words = text_file.read()
    keywords = keyword_file.read()
    keywords_list = keywords.split()
    if len(sys.argv) == 6:
        prob_file = open(sys.argv[5], 'r')
        prob = prob_file.read()
        out_file.write(process_text(words, keywords_list, dictionary, prob))

main()
