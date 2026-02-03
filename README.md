# Turkish POS & Semantic Analyzer

> **Stanza-based Turkish NLP with POS preferences detection and propositional semantics analysis**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Stanza](https://img.shields.io/badge/stanza-1.5+-green.svg)](https://stanfordnlp.github.io/stanza/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Overview

This project provides a comprehensive Turkish NLP analysis toolkit that combines:

- **POS Tagging** with Stanza parser
- **POS Preference Detection** using Minimalist Program theory
- **Propositional Semantics** analysis (analytic vs synthetic)
- **JSON & CONLL-U** structured output formats

### What Makes This Different?

Traditional POS taggers assign universal tags (NOUN, VERB, ADJ) based on syntax. Our system goes deeper:

1. **Detects nominal domain preferences** - Identifies when VERB-origin words prefer nominal behavior
2. **Semantic validation** - Analyzes whether propositions are analytic (generic) or synthetic (time-bound)
3. **Clause finiteness** - Distinguishes finite clauses from embedded non-finite structures
4. **Lexicalization filtering** - Recognizes frozen compounds vs. productive derivations

**Example:**
```
"Ali'nin okuduğu kitap burada."
         ↓
"okuduğu" (read-DIK-his):
  - Stanza tags: VERB (syntactically correct)
  - Our detection: NOUN preference (90% confidence)
  - Reason: Nominal suffix -DIK → partitive predicate → specificity → nominal domain
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/centering_test.git
cd centering_test

# Install dependencies
pip install stanza

# Download Turkish model
python -c "import stanza; stanza.download('tr')"

# PyTorch 2.6+ compatibility (if needed)
# Add to your script before importing:
import os
os.environ['TORCH_FORCE_WEIGHTS_ONLY_LOAD'] = '0'
```

### Basic Usage

```python
import os
os.environ['TORCH_FORCE_WEIGHTS_ONLY_LOAD'] = '0'  # PyTorch 2.6+ compatibility

from api.pos_semantic_analyzer import analyze_text
import json

# Analyze a sentence
result = analyze_text("Kuşlar uçtu.")

# Pretty print JSON
print(json.dumps(result, indent=2, ensure_ascii=False))
```

**Output:**
```json
{
  "text": "Kuşlar uçtu.",
  "sentences": [{
    "words": [{
      "id": 2,
      "text": "uçtu",
      "upos": "VERB",
      "feats": "Aspect=Perf|Tense=Past",
      "is_finite": true,
      "morphology": [],
      "preference": null
    }],
    "semantics": {
      "proposition_type": "synthetic",
      "predicate_type": "partitive",
      "clause_finiteness": "finite",
      "generic_encoding": false,
      "time_bound": true,
      "verifiability": 0.8
    }
  }]
}
```

---

## 📊 Features

### 1. POS Preference Detection

Identifies when words show preference for different POS categories:

**Supported Patterns:**
- **-DIK suffix**: VERB → NOUN preference (partitive predicate nominalization)
- **-mA suffix**: Productive vs lexicalized distinction
- **-Iş suffix**: VERB → NOUN (action nominalization)
- **-mAk suffix**: Infinitive forms

**Confidence Levels:**
- `-DIK` with semantic validation: **90-95%**
- `-mA` productive: **80-85%**
- `-mA` lexicalized: **No preference** (filtered out)

### 2. Propositional Semantics

Analyzes propositions using semantic theory:

**Proposition Types:**
- **Analytic**: Generic, always true/false (e.g., "Kuşlar uçar" - Birds fly)
- **Synthetic**: Time-bound, verifiable (e.g., "Kuşlar uçtu" - Birds flew)

**Predicate Types:**
- **Holistic** (bütüncül): State/property, no time point (e.g., habitual, copula)
- **Partitive** (parçalı): Event, specific time point (e.g., past, future)
- **Habitual** (alışkanlık): Recurring pattern (e.g., "Ali sabahları erken kalkar")

**Clause Finiteness:**
- **Finite**: Independent clause with tensed verb
- **Non-finite**: Embedded clause, copula, or nominal predicate

### 3. Structured Output Formats

#### JSON Format (Stanza-compatible)
Complete linguistic annotation with extensions:
- Word-level: `morphology`, `is_finite`, `preference`
- Sentence-level: `semantics` (proposition analysis)

#### CONLL-U Format
Standard format with preferences in MISC field:
```
# text = Ali'nin okuduğu kitap burada.
2  okuduğu  oku  VERB  ...  Preference=NOUN|Confidence=0.90|Morphology=-DIK
```

---

## 📁 Project Structure

```
centering_test/
├── api/
│   ├── pos_semantic_analyzer.py      # 🚢 Main API (flagship)
│   ├── simple_check.py               # Simple POS preference check
│   ├── enhanced_analysis.py          # Full semantic integration
│   └── main.py                       # Legacy API functions
│
├── error_detection/
│   └── minimalist_pos_error_detection.py  # Minimalist Program detector
│
├── src/
│   └── propositional_semantics.py    # Semantic analysis module
│
├── tests/
│   ├── test_comprehensive.py         # Full integration tests
│   ├── test_semantic_integration.py  # Semantic tests
│   ├── test_minimalist.py           # Minimalist Program tests
│   ├── test_lexicalized.py          # Lexicalized compound tests
│   └── test_pos_fixes.py            # POS fixes validation (17 tests)
│
├── data/
│   └── ud_tr_imst/                   # UD Turkish-IMST corpus
│
├── example_usage.py                  # Usage examples
└── README.md                         # This file
```

---

## 🔬 Theoretical Background

### Minimalist Program (Chomsky 1995)

Our POS preference detection is based on Minimalist syntax theory:

**Core Principles:**
1. **Feature Checking**: Nominal suffixes (-DIK, -mA) trigger N-features
2. **Merge Operation**: Builds binary-branching syntactic structures
3. **Movement Theory**: Tracks derivational history (VERB-origin → NOUN)

**Key Insight:**
> Morphologically derived nominals retain verbal semantics but show nominal syntactic distribution. This creates a **preference** rather than an error.

### Propositional Semantics

Based on analytic/synthetic proposition distinction:

**Analytic Propositions:**
- Generic reference (bare plurals: "Kuşlar" without specificity)
- Holistic predicates (aorist/habitual: "uçar")
- Always true/false (100% verifiability)
- Example: "Kuşlar uçar" (Birds fly - generic property)

**Synthetic Propositions:**
- Specific reference (demonstratives, accusative case)
- Partitive predicates (past, future, progressive)
- Time-bound truth value
- Example: "Kuşlar uçtu" (Birds flew - specific event)

---

## 💡 Usage Examples

### Example 1: Detect POS Preferences

```python
from api.pos_semantic_analyzer import analyze_text

text = "Ali'nin okuduğu kitap burada."
result = analyze_text(text)

# Check for preferences
for word in result["sentences"][0]["words"]:
    if word["preference"]:
        print(f"{word['text']}: {word['upos']} → {word['preference']['expected_pos']}")
        print(f"  Confidence: {word['preference']['confidence']:.0%}")
        print(f"  Reason: {word['preference']['reason']}")

# Output:
# okuduğu: VERB → NOUN
#   Confidence: 90%
#   Reason: Nominal suffix detected: ['-DIK']
```

### Example 2: Analyze Semantics

```python
from api.pos_semantic_analyzer import analyze_text

sentences = [
    "Kuşlar uçar.",           # Analytic
    "Kuşlar uçtu.",           # Synthetic
    "Ali sabahları kalkar."   # Habitual
]

for text in sentences:
    result = analyze_text(text)
    sem = result["sentences"][0]["semantics"]
    
    print(f"{text}")
    print(f"  Type: {sem['proposition_type']}")
    print(f"  Predicate: {sem['predicate_type']}")
    print(f"  Finite: {sem['clause_finiteness']}")
```

### Example 3: CONLL-U Export

```python
from api.pos_semantic_analyzer import analyze_to_conllu

text = "Ali'nin okuduğu kitap burada."
conllu = analyze_to_conllu(text)
print(conllu)

# Output:
# # text = Ali'nin okuduğu kitap burada.
# 1  Ali'nin  Ali  PROPN  ...
# 2  okuduğu  oku  VERB   ...  Preference=NOUN|Confidence=0.90|Morphology=-DIK
# 3  kitap    kitap NOUN  ...
# ...
```

### Example 4: Lexicalized vs Productive

```python
from api.pos_semantic_analyzer import analyze_text

# Lexicalized (no preference)
result1 = analyze_text("Yüzme havuzu temiz.")
# "Yüzme" → No preference (frozen compound)

# Productive (preference detected)
result2 = analyze_text("Yazma defteri aldım.")
# "Yazma" → NOUN preference (85% confidence)
```

---

## 🧪 Testing

### Run All Tests

```bash
# Comprehensive integration test
python tests/test_comprehensive.py

# Semantic integration test
python tests/test_semantic_integration.py

# Minimalist Program test
python tests/test_minimalist.py

# Lexicalized compound test
python tests/test_lexicalized.py

# POS fixes validation (all fixes verified)
python tests/test_pos_fixes.py
```

### Test Results

**test_pos_fixes.py**: 17/17 tests passed (100% success) ⭐
- ✅ -DIK suffix nominal preference (3 tests)
- ✅ -mA productive vs lexicalized (2 tests)
- ✅ Generic vs specific propositions (2 tests)
- ✅ Holistic/Partitive/Habitual predicates (3 tests)
- ✅ Finite vs non-finite detection (3 tests)
- ✅ Confidence scoring accuracy (2 tests)
- ✅ English output format (2 tests)

**test_comprehensive.py**: 10/13 tests passed (76.9% success)
- ✅ -DIK detection with 95% confidence
- ✅ Productive -mA detection (80-85%)
- ✅ Lexicalized filtering (no false positives)
- ✅ Generic vs specific distinction
- ✅ Semantic validation boosts confidence

**test_minimalist.py**: All tests passed
- ✅ Propositional semantics available
- ✅ Detection working (1 error found)
- ✅ Lexicalized filtering (0 errors for "Yüzme")

---

## 📖 API Reference

### Main Functions

#### `analyze_text(text: str, include_semantics: bool = True) -> Dict`

Analyzes Turkish text with full linguistic annotation.

**Parameters:**
- `text`: Input Turkish text
- `include_semantics`: Include propositional semantics (default: True)

**Returns:**
```python
{
  "text": str,
  "sentences": [
    {
      "text": str,
      "words": [
        {
          "id": int,
          "text": str,
          "lemma": str,
          "upos": str,
          "feats": str,
          "morphology": List[str],
          "is_finite": bool,
          "preference": {
            "type": str,
            "expected_pos": str,
            "confidence": float,
            "reason": str
          } | None
        }
      ],
      "semantics": {
        "proposition_type": "analytic" | "synthetic",
        "predicate_type": "holistic" | "partitive" | "habitual",
        "generic_encoding": bool,
        "time_bound": bool,
        "verifiability": float,
        "clause_finiteness": "finite" | "non-finite"
      } | None
    }
  ]
}
```

#### `analyze_to_conllu(text: str) -> str`

Exports analysis to CONLL-U format.

**Parameters:**
- `text`: Input Turkish text

**Returns:** CONLL-U formatted string with preferences in MISC field

---

## 🔍 Detection Examples

### Example 1: Nominal Domain Preference

**Input:** "Ali'nin okuduğu kitap burada."

**Analysis:**
- `okuduğu`: VERB (Stanza)
- **Preference**: NOUN (90% confidence)
- **Reason**: `-DIK` suffix → partitive predicate → nominal domain
- **Semantic validation**: Partitive predicate in nominal position

### Example 2: Lexicalized Compound

**Input:** "Yüzme havuzu temiz."

**Analysis:**
- `Yüzme`: NOUN (Stanza)
- **Preference**: None (lexicalized)
- **Reason**: "yüzme havuzu" is a frozen compound (swimming pool)
- No semantic shift detected

### Example 3: Productive Derivation

**Input:** "Yazma defteri aldım."

**Analysis:**
- `Yazma`: VERB (Stanza)
- **Preference**: NOUN (85% confidence)
- **Reason**: `-mA` suffix, productive derivation
- "yazma defteri" = notebook (compositional meaning)

### Example 4: Generic vs Specific

**Input 1:** "Kuşlar uçar." (Birds fly)
- **Proposition**: Analytic
- **Predicate**: Holistic
- **Generic**: True
- **Verifiability**: 1.0 (always true)

**Input 2:** "Kuşlar uçtu." (Birds flew)
- **Proposition**: Synthetic
- **Predicate**: Partitive
- **Generic**: False
- **Time-bound**: True
- **Verifiability**: 0.8 (context-dependent)

---

## 🛠️ Advanced Configuration

### Custom Stanza Pipeline

```python
import stanza
from api.pos_semantic_analyzer import analyze_text

# Custom pipeline (advanced users)
nlp = stanza.Pipeline('tr', 
    processors='tokenize,pos,lemma,depparse',
    tokenize_pretokenized=True  # If pre-tokenized
)

# Use default pipeline
result = analyze_text("Ali geldi.")
```

### Disable Semantics

```python
# Only POS preferences, no semantics
result = analyze_text("Kuşlar uçar.", include_semantics=False)
```

---

## 📚 Theoretical References

### Minimalist Program
- Chomsky, N. (1995). *The Minimalist Program*. MIT Press.
- Kornfilt, J. (1997). *Turkish*. Routledge.

### Propositional Semantics
- Carlson, G. N. (1977). *Reference to Kinds in English*. UMass dissertation.
- Chierchia, G. (1998). Reference to kinds across languages. *Natural Language Semantics* 6.

### Turkish Linguistics
- Göksel, A., & Kerslake, C. (2005). *Turkish: A Comprehensive Grammar*. Routledge.
- Kornfilt, J. (1997). *Turkish*. Routledge Descriptive Grammars.

### UD Turkish
- Universal Dependencies Turkish-IMST corpus
- [UD Turkish Documentation](https://universaldependencies.org/tr/index.html)

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. **Morphological Analysis**: Better Turkish morphology extraction
2. **Semantic Features**: Expand propositional analysis
3. **Error Detection**: More nominal suffix patterns
4. **Performance**: Optimize Stanza integration
5. **Testing**: More edge cases and corpus evaluation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Stanza NLP**: Stanford NLP Group
- **Universal Dependencies**: UD Turkish-IMST corpus
- **Theoretical foundations**: Chomsky's Minimalist Program, Carlson's Generic Reference

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

## 🗂️ Project History

### Recent Updates (February 2025)

- ✅ **Comprehensive test suite**: test_pos_fixes.py with 17 tests (100% passing)
- ✅ **PyTorch 2.6 compatibility**: Added workaround for Stanza models
- ✅ **Renamed flagship API**: `structured_output.py` → `pos_semantic_analyzer.py`
- ✅ **English output**: All semantic fields now in English (holistic/partitive/habitual)
- ✅ **Fixed imports**: Resolved module path issues in api/main.py
- ✅ **Aspect=Hab support**: Habitual verbs now correctly detected as finite
- ✅ **Type safety**: Added getattr for Stanza document access
- ✅ **Project cleanup**: Removed centering theory module (18 files deleted)
- ✅ **Test reorganization**: All tests moved to `tests/` directory
- ✅ **Import fixes**: Updated all import paths
- ✅ **Lexicalized filtering**: Improved compound detection
- ✅ **Semantic validation**: 90% → 95% confidence boost for -DIK
- ✅ **Propositional semantics**: Full integration with POS analysis

### Core Features

1. **POS Preference Detection** (Minimalist Program)
   - Nominal suffix detection (-DIK, -mA, -Iş, -mAk)
   - Confidence scoring with semantic validation
   - Lexicalized compound filtering

2. **Propositional Semantics**
   - Analytic vs Synthetic propositions
   - Holistic vs Partitive predicates
   - Generic encoding detection
   - Clause finiteness analysis

3. **Output Formats**
   - JSON (Stanza-compatible with extensions)
   - CONLL-U (standard format with MISC annotations)

4. **Testing Suite**
   - Comprehensive integration tests
   - Semantic validation tests
   - Lexicalized compound tests
   - Minimalist Program validation

---

**Built with ❤️ for Turkish NLP**
