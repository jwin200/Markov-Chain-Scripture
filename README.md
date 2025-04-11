**The Torah** is one of the greatest works in literary history, yet with a small amount of effort we can mar this masterpiece and transform it into incomprehensible gibberish. Lo, I have done just that!

The first step on our journey towards heretical genius is to scrape an online archive of the Old Testament to download it locally, this was done with `build_corpus.py`. The output corpora (only the five books of Moses) were saved into the `corpus` folder. To add a little spice to our holy text the `build_corpus.py` script also scrapes the entire text of Tolkien's The Lord of the Rings from a similar archive. These two texts blend into a wonderful melange of high fantasy and grumpy people running around in the desert.

With our need for inputs sated, we turn to the creation of a most unholy Markov Chain in `markov.py`. In the `create_markov()` method, all text from our corpora is loaded, parsed, tokenized, and evaluated in the form of a 3-gram model (structure shown below). The frequency of word groups is determined and saved in a dictionary object, stored locally as `markov_chain.json`. 

We can then generate our new scripture, one chapter at a time. In `create_text()`, chapter names are chosen randomly from a list of proper nouns in the corpus. Verses are then generated until a certain number (adjustable) have been written. Each verse is preceded by its number in brackets (`[1], [2], [3]` etc.).

Once all verses have been written, our text is saved into the `output` folder for future worship and study.

---

**Markov Chain Structure:**

```
Markov Chain object stores key words and a list of following words 
with their chance of occurence

markov_chain = {
    'I': {
        'am': {
            'not': .24,
            'the': .45,
            'tired': .31
        }, 
        'will': {
            'try': .65,
            'not': .35
        }, 
        'do': {
            'not': .98,
            'think': .02
        }
    }, 
    'will': {
        'not': {
            'do': .14,
            'be': .45,
            'say': .41
        }
    }
}
```

---

Jonah Winchell
Code as a Liberal Art, Spring 2025