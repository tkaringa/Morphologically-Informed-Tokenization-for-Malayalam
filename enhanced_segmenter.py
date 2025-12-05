import re
from functools import lru_cache
from mlmorph import Analyser

# Define morphological rules
# Pattern replacement pairs
MORPH_RULES = [
    # Plural markers
    (r'(.{3,})കൾ$', r'\1_SEP_കൾ'),
    (r'(.{4,})മാർ$', r'\1_SEP_മാർ'),
    (r'(.{3,})ങ്ങൾ$', r'\1_SEP_ങ്ങൾ'),
    
    # Case markers
    (r'(.{3,})ിൽ$', r'\1_SEP_ിൽ'),
    (r'(.{3,})ില്‍$', r'\1_SEP_ില്‍'),
    (r'(.{3,})യിൽ$', r'\1_SEP_യിൽ'),
    (r'(.{3,})ിന്$', r'\1_SEP_ിന്'),
    (r'(.{3,})ിനു$', r'\1_SEP_ിനു'),
    (r'(.{3,})ിന്ന്$', r'\1_SEP_ിന്ന്'),
    (r'(.{4,})ുടെ$', r'\1_SEP_ുടെ'),
    (r'(.{3,})യുടെ$', r'\1_SEP_യുടെ'),
    (r'(.{3,})ിന്റെ$', r'\1_SEP_ിന്റെ'),
    (r'(.{3,})ാൽ$', r'\1_SEP_ാൽ'),
    (r'(.{3,})ിനാൽ$', r'\1_SEP_ിനാൽ'),
    (r'(.{3,})കൊണ്ട്$', r'\1_SEP_കൊണ്ട്'),
    (r'(.{4,})ിൽനിന്ന്$', r'\1_SEP_ിൽനിന്ന്'),
    (r'(.{3,})യിൽനിന്ന്$', r'\1_SEP_യിൽനിന്ന്'),
    
    # Verb endings
    (r'(.{4,})ുന്നു$', r'\1_SEP_ുന്നു'),
    (r'(.{4,})ുന്ന$', r'\1_SEP_ുന്ന'),
    (r'(.{4,})ുകയാണ്$', r'\1_SEP_ുകയാണ്'),
    (r'(.{4,})ുകയാണു$', r'\1_SEP_ുകയാണു'),
    (r'(.{4,})ിച്ചു$', r'\1_SEP_ിച്ചു'),
    (r'(.{4,})ിച്ച്$', r'\1_SEP_ിച്ച്'),
    (r'(.{3,})ന്നു$', r'\1_SEP_ന്നു'),
    (r'(.{3,})യി$', r'\1_SEP_യി'),
    (r'(.{3,})ും$', r'\1_SEP_ും'),
    (r'(.{4,})യും$', r'\1_SEP_യും'),
    
    # Miscellaneous suffixes
    (r'(.{3,})ായി$', r'\1_SEP_ായി'),
    (r'(.{4,})ായിട്ട്$', r'\1_SEP_ായിട്ട്'),
    (r'(.{3,})ാതെ$', r'\1_SEP_ാതെ'),
    (r'(.{4,})ങ്കിൽ$', r'\1_SEP_ങ്കിൽ'),
    (r'(.{4,})ുന്നത്$', r'\1_SEP_ുന്നത്'),
    (r'(.{4,})ിയത്$', r'\1_SEP_ിയത്'),
    (r'(.{3,})ൽ$', r'\1_SEP_ൽ'),
    (r'(.{3,})ോ$', r'\1_SEP_ോ'),
    (r'(.{3,})യോ$', r'\1_SEP_യോ'),
    (r'(.{3,})തന്നെ$', r'\1_SEP_തന്നെ'),
    (r'(.{3,})കൂടി$', r'\1_SEP_കൂടി'),
    (r'(.{3,})കൂടെ$', r'\1_SEP_കൂടെ'),
    (r'(.{4,})ിനേക്കാൾ$', r'\1_SEP_ിനേക്കാൾ'),
    
    # Compound suffixes
    (r'(.{4,})കാർ$', r'\1_SEP_കാർ'),
    (r'(.{4,})വാദി$', r'\1_SEP_വാദി'),
    (r'(.{4,})വാദം$', r'\1_SEP_വാദം'),
    (r'(.{4,})ശാല$', r'\1_SEP_ശാല'),
    (r'(.{4,})ശാലാ$', r'\1_SEP_ശാലാ'),
    (r'(.{4,})ജി$', r'\1_SEP_ജി'),
    (r'(.{4,})സാർ$', r'\1_SEP_സാർ'),
]

class MalayalamMorphologicalSegmenter:
    def __init__(self):
        self.analyser = Analyser()
        # Compile regex patterns
        self.rules = []
        for pat, repl in MORPH_RULES:
            self.rules.append((re.compile(pat), repl))
            
    @lru_cache(maxsize=50000)
    def segment_word(self, word):
        # Skip short words
        if not word or len(word) <= 2:
            return word
            
        # Check Malayalam script
        is_malayalam = False
        for char in word:
            if '\u0D00' <= char <= '\u0D7F':
                is_malayalam = True
                break
        if not is_malayalam:
            return word
            
        # Validate with mlmorph
        # Optional validation step
        try:
            self.analyser.analyse(word)
        except:
            pass
            
        # Apply segmentation rules
        curr = word
        for pat, repl in self.rules:
            match = pat.match(curr)
            if match:
                curr = pat.sub(repl, curr)
                break
                
        return curr
    
    def segment_text(self, text):
        # Tokenize preserving punctuation
        # Regex handles Malayalam
        pattern = r'(?:[\u0D00-\u0D7F]|\w)+|[^\w\u0D00-\u0D7F]+'
        tokens = re.findall(pattern, text)
        out = []
        
        for t in tokens:
            # Segment word tokens
            if re.match(r'(?:[\u0D00-\u0D7F]|\w)+$', t):
                out.append(self.segment_word(t))
            else:
                out.append(t)
                
        return ''.join(out)

if __name__ == "__main__":
    # Run basic tests
    seg = MalayalamMorphologicalSegmenter()
    test_words = ["കേരളത്തിൽ", "വന്നപ്പോൾ", "കുട്ടികൾ", "അവരോട്"]
    
    print("testing segmenter...")
    for w in test_words:
        print(f"{w} -> {seg.segment_word(w)}")
