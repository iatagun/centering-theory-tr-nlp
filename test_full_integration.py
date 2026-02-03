"""
Centering Theory + Stanza JSON Format entegrasyon testi
"""
import os
os.environ['TORCH_FORCE_WEIGHTS_ONLY_LOAD'] = '0'

from api.pos_semantic_analyzer import analyze_text
import json

# Test cümleleri
test_texts = [
    "Ali kitabı okudu.",
    "Ali'nin okuduğu kitap burada.",
    "Kuşlar uçar.",
    "Ali sabahları erken kalkar.",
    "Yüzme havuzu temiz."
]

print("=" * 100)
print("STANZA JSON FORMAT + CENTERING THEORY - Full Integration Test")
print("=" * 100)

for i, text in enumerate(test_texts, 1):
    print(f"\n{'='*100}")
    print(f"Test {i}: {text}")
    print('='*100)
    
    result = analyze_text(text)
    
    # JSON çıktısı
    json_output = json.dumps(result, indent=2, ensure_ascii=False)
    print(json_output)
    
    # Önemli alanları vurgula
    sent = result["sentences"][0]
    
    print(f"\n{'─'*100}")
    print("📊 ÖZET:")
    print('─'*100)
    
    # Preferences
    if sent["preferences"]:
        print(f"\n✅ PREFERENCES ({len(sent['preferences'])} kelime):")
        for pref in sent["preferences"]:
            print(f"  • {pref['word']}: {pref['stanza_pos']} → {pref['suggested_pos']}")
            print(f"    Discourse: {pref['discourse_role']}, Referential: {pref['referential_status']}")
    else:
        print("\n✅ PREFERENCES: None (Stanza doğru etiketlemiş)")
    
    # Semantics - Discourse
    if sent["semantics"] and "discourse" in sent["semantics"]:
        disc = sent["semantics"]["discourse"]
        print(f"\n💬 DISCOURSE:")
        print(f"  • Topics (Cb): {disc['topic_candidates']}")
        print(f"  • Focus (Cf): {disc['focus_entities']}")
        print(f"  • Referential density: {disc['referential_density']}")
        print(f"  • Roles: {disc['discourse_role_distribution']}")
    
    # Semantics - Information Structure
    if sent["semantics"] and "information_structure" in sent["semantics"]:
        info = sent["semantics"]["information_structure"]
        print(f"\n📋 INFORMATION STRUCTURE:")
        print(f"  • Given: {info['given_entities']}")
        print(f"  • New: {info['new_entities']}")
        print(f"  • Topic position: {info['topic_position']}")
        print(f"  • Packaging: {info['information_packaging']}")
    
    # Semantics - Propositional
    if sent["semantics"]:
        sem = sent["semantics"]
        print(f"\n🔬 PROPOSITIONAL SEMANTICS:")
        print(f"  • Type: {sem['proposition_type']}")
        print(f"  • Predicate: {sem['predicate_type']}")
        print(f"  • Finiteness: {sem['clause_finiteness']}")
        if sem['generic_encoding']:
            print(f"  • Generic: Yes (verifiability: {sem['verifiability']})")

print(f"\n{'='*100}")
print("✅ Entegrasyon testi tamamlandı!")
print("=" * 100)

# JSON dosyasına kaydet
output_file = "centering_stanza_output.json"
final_result = {
    "test_description": "Turkish POS Semantic Analyzer with Centering Theory",
    "format": "Stanza JSON + Extensions",
    "tests": []
}

for text in test_texts:
    result = analyze_text(text)
    final_result["tests"].append(result)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(final_result, f, indent=2, ensure_ascii=False)

print(f"\n💾 JSON çıktı kaydedildi: {output_file}")
