from unittest import TestCase
import random
import urllib.request
# from stack overflow link posted in the discord chat
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

ROMEO_SOLILOQUY = """
        But, soft! what light through yonder window breaks?
        It is the east, and Juliet is the sun.
        Arise, fair sun, and kill the envious moon,
        who is already sick and pale with grief,
        That thou her maid art far more fair than she:
        be not her maid, since she is envious;
        her vestal livery is but sick and green
        and none but fools do wear it; cast it off.
        It is my lady, O, it is my love!
        O, that she knew she were!
        She speaks yet she says nothing: what of that?
        Her eye discourses; I will answer it.
        I am too bold, 'tis not to me she speaks:
        two of the fairest stars in all the heaven,
        having some business, do entreat her eyes
        to twinkle in their spheres till they return.
        What if her eyes were there, they in her head?
        The brightness of her cheek would shame those stars,
        as daylight doth a lamp; her eyes in heaven
        would through the airy region stream so bright
        that birds would sing and think it were not night.
        See, how she leans her cheek upon her hand!
        O, that I were a glove upon that hand,
        that I might touch that cheek!"""

################################################################################
# EXERCISE 1
################################################################################
# Implement this function
def compute_ngrams(toks, n=2):
    """Returns an n-gram dictionary based on the provided list of tokens."""
    # step 1: create a dictionary with all possible key values using a dictionary comprehension 
    # (ex. if n = 3, ignores last two elements which can't create full 3-grams)
    ngram_dict = {k:[] for k in toks[:-n+1]}

    # step 2: loop through values that represent keys in toks
    for i in range(len(toks)-n+1):
        # checks if the selected value is indeed a key
        if toks[i] in ngram_dict: 
            # adds ngram value to the tuple of the key:value pair
            ngram_dict[toks[i]].append(tuple(toks[i+1:i+n]))
    
    # step 3: return the dictionary of ngram combos
    return ngram_dict

def test1():
    test1_1()
    test1_2()

# 20 Points
def test1_1():
    """A smaller test case for your ngram function."""
    tc = TestCase()
    simple_toks = [t.lower() for t in 'I really really like cake.'.split()]

    compute_ngrams(simple_toks)
    tc.assertEqual(compute_ngrams(simple_toks),
                   {'i': [('really',)], 'like': [('cake.',)], 'really': [('really',), ('like',)]})
    tc.assertEqual(compute_ngrams(simple_toks, n=3),
                   {'i': [('really', 'really')],
                    'really': [('really', 'like'), ('like', 'cake.')]})

    romeo_toks = [t.lower() for t in ROMEO_SOLILOQUY.split()]

    dct = compute_ngrams(romeo_toks, n=4)
    tc.assertEqual(dct['but'], [('sick', 'and', 'green'), ('fools', 'do', 'wear')])
    tc.assertEqual(dct['it'],
                   [('is', 'the', 'east,'),
                    ('off.', 'it', 'is'),
                    ('is', 'my', 'lady,'),
                    ('is', 'my', 'love!'),
                    ('were', 'not', 'night.')])

# 30 Points
def test1_2():
    """Test your code on Peter Pan."""
    PETER_PAN_URL = 'https://moss.cs.iit.edu/cs331/data/peterpan.txt'
    peter_pan_text = urllib.request.urlopen(PETER_PAN_URL).read().decode()
    tc = TestCase()
    pp_toks = [t.lower() for t in peter_pan_text.split()]
    dct = compute_ngrams(pp_toks, n=3)
    tc.assertEqual(dct['crocodile'],
                   [('passes,', 'but'),
                    ('that', 'happened'),
                    ('would', 'have'),
                    ('was', 'in'),
                    ('passed', 'him,'),
                    ('is', 'about'),
                    ('climbing', 'it.'),
                    ('that', 'was'),
                    ('pass', 'by'),
                    ('and', 'let'),
                    ('was', 'among'),
                    ('was', 'waiting')])
    tc.assertEqual(len(dct['wendy']), 202)
    tc.assertEqual(len(dct['peter']), 243)

################################################################################
# EXERCISE 2
################################################################################
# Implement this function
def gen_passage(ngram_dict, length=100):
    # step 1: select a random key to serve as the first token
    token = random.choice(sorted(ngram_dict.keys()))

    # step 2: set that token as the first word of the passage
    passage = [token]

    # step 3: select random tuple from the list associated with the token
    # and append the sequence to the passage separated by spaces
    while len(passage) < length:
        passage.append(''.join(random.choice(ngram_dict[token])))
        # step 4: set last token of selected sequence as new token
        token = passage[-1]
        # step 5: if current token is a key in the dictionary, continue
        # otherwise select another random key from the map as the current token
        # add append it to the passage before continuing
        if token not in ngram_dict:
            token = random.choice(sorted(ngram_dict.keys()))
            passage.append(token)
    
    # step 6: return passage with words sepatated by spaces
    return " ".join(passage)

# 50 Points
def test2():
    """Test case for random passage generation."""
    tc = TestCase()
    random.seed(1234)
    simple_toks = [t.lower() for t in 'I really really like cake.'.split()]
    tc.assertEqual(gen_passage(compute_ngrams(simple_toks), 10),
                   'like cake. i really really really really like cake. i')

    random.seed(1234)
    romeo_toks = [t.lower() for t in ROMEO_SOLILOQUY.split()]
    tc.assertEqual(gen_passage(compute_ngrams(romeo_toks), 10),
                   'too bold, \'tis not night. see, how she leans her')

def main():
    test1()
    test2()

if __name__ == '__main__':
    main()