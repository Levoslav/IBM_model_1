#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", default="czenali", type=str, help="Input file of data")
parser.add_argument("--output_file", default="output.txt", type=str, help="Output file name")
parser.add_argument("--iterations", default=20, type=int, help="number of iterations of EM algo")

def main(args):
    
    english_all_words = set()
    foreign_all_words = set()
    english_sentences = []
    foreign_sentences = [] 
    #Read data from the file
    with open(file=args.input_file, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.lower().split("\t")
            english_tokens = re.findall(r'\w+',line[0].strip())
            foreign_tokens = re.findall(r'\w+',line[1].strip())
    
            for e in english_tokens:
                english_all_words.add(e)
            for f in foreign_tokens:
                foreign_all_words.add(f)

            english_sentences.append(english_tokens)  
            foreign_sentences.append(foreign_tokens)  
   

    # Initialize t[e|f] uniformly 
    t = dict()
    for english_s, foreign_s in zip(english_sentences,foreign_sentences):
        for english_w in english_s:
            if not english_w in t:
                t[english_w] = dict()
            for foreign_w in foreign_s:
                t[english_w][foreign_w] = 1/len(foreign_s)

    
    # Repeat until convergence
    for iter in range(args.iterations):
        print("Iteration " + str(iter + 1))
        # Set count[e|f] to 0 for all e,f     &     set total(f) to 0 for all f
        count = dict()
        total = dict()
        for e in english_all_words:
            count[e] = dict()
            for f in foreign_all_words:
                total[f] = 0.0
                count[e][f] = 0.0
       
        # For all sentence pairs
        for english_s, foreign_s in zip(english_sentences, foreign_sentences):
    
            total_s = dict()
            for e in english_s:
                total_s[e] = 0.0
                for f in foreign_s:
                    total_s[e] += t[e][f]

            for e in english_s:
                for f in foreign_s:
                    count[e][f] += t[e][f] / total_s[e]
                    total[f] += t[e][f] / total_s[e]
        # Update t[e|f] 
        for e in t:
            for f in t[e]:
                t[e][f] = count[e][f] / total[f]
    
    # Output 
    with open(args.output_file, "w") as f:
        for english_word in t:
            translations = sorted(t[english_word].items(), key=lambda x: x[1], reverse=True)[:3]
            

            # Write English word and translations to file
            f.write(english_word + " "*(18-len(english_word)) + "- ")
            for i, (foreign_word, prob) in enumerate(translations):
                f.write(foreign_word + " "*(18-len(foreign_word)) + str(prob)[:4])
                if i < 2:
                    f.write(" | ")
            f.write("\n")



        


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)