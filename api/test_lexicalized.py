from main import check_sentence

# Test lexicalized compounds
test_cases = [
    ("Yüzme havuzu.", "SHOULD PASS - lexicalized"),
    ("Yazma defteri.", "SHOULD FAIL - not lexicalized"),
    ("Koşma parkuru.", "SHOULD PASS - lexicalized"),
    ("Okuma kitabı.", "SHOULD FAIL - not lexicalized"),
]

print("=" * 70)
print("LEXICALIZED COMPOUND TEST")
print("=" * 70)

for sentence, expectation in test_cases:
    r = check_sentence(sentence)
    has_errors = len(r['errors']) > 0
    status = "❌ PREFERENCE" if has_errors else "✅ NO PREFERENCE"
    
    print(f"\n{status} {sentence}")
    print(f"   Expected: {expectation}")
    if has_errors:
        for e in r['errors']:
            print(f"   • {e['word']}: {e['type']}")
    else:
        print(f"   ✓ Correctly identified as lexicalized or UD-compliant")
