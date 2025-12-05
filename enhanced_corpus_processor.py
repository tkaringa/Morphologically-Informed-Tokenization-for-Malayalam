import os
import re
from collections import Counter
from enhanced_segmenter import MalayalamMorphologicalSegmenter

def process_corpus():
    # Initialize processor
    segmenter = MalayalamMorphologicalSegmenter()
    in_file = 'malayalam_raw_corpus.txt'
    out_file = 'enhanced_hybrid_training_data.txt'
    
    if not os.path.exists(in_file):
        print(f"error: {in_file} not found")
        return None
    
    print(f"processing {in_file} -> {out_file}")
    
    # Initialize counters
    total_lines = 0
    processed_lines = 0
    total_words = 0
    segmented_words = 0
    morphemes = Counter()
    
    with open(in_file, 'r', encoding='utf-8') as f_in, \
         open(out_file, 'w', encoding='utf-8') as f_out:
        
        for i, line in enumerate(f_in, 1):
            total_lines += 1
            line = line.strip()
            
            # Skip invalid lines
            if not line or len(line) < 10:
                continue
                
            # Check Malayalam content
            mal_chars = sum(1 for c in line if '\u0D00' <= c <= '\u0D7F')
            if mal_chars < len(line) * 0.3:
                continue
            
            try:
                # Segment text
                seg_line = segmenter.segment_text(line)
                
                # Update statistics
                words = re.findall(r'(?:[\u0D00-\u0D7F]|\w)+', line)
                segs = re.findall(rf'\w*_SEP_\w*', seg_line)
                
                total_words += len(words)
                segmented_words += len(segs)
                
                # Count morpheme types
                for w in segs:
                    if '_SEP_' in w:
                        parts = w.split('_SEP_')
                        if len(parts) == 2:
                            morphemes[parts[1]] += 1
                
                f_out.write(seg_line + '\n')
                processed_lines += 1
                
                if i % 20000 == 0:
                    rate = (segmented_words / total_words * 100) if total_words > 0 else 0
                    print(f"processed {i} lines | kept {processed_lines} | seg rate: {rate:.1f}%")
                    
            except Exception as e:
                print(f"error on line {i}: {e}")
                continue

    # Print final statistics
    seg_rate = (segmented_words / total_words * 100) if total_words > 0 else 0
    print("\ndone.")
    print(f"kept: {processed_lines}/{total_lines} ({processed_lines/total_lines*100:.1f}%)")
    print(f"seg rate: {seg_rate:.1f}%")
    
    return {
        'total_lines': total_lines,
        'processed_lines': processed_lines,
        'total_words': total_words,
        'segmented_words': segmented_words,
        'seg_rate': seg_rate,
        'unique_morphemes': len(morphemes)
    }

def save_metrics(stats):
    # Save LaTeX table
    print("saving metrics table...")
    
    content = f"""
\\begin{{table}}[h]
\\centering
\\caption{{Enhanced Morphological Segmentation Results}}
\\begin{{tabular}}{{lll}}
\\toprule
\\textbf{{Metric}} & \\textbf{{Value}} & \\textbf{{Interpretation}} \\\\
\\midrule
Input corpus size & {stats['total_lines']:,} lines & Large-scale evaluation \\\\
Processing efficiency & {stats['processed_lines']/stats['total_lines']*100:.1f}\\% & Quality filtering \\\\
Morphological coverage & {stats['seg_rate']:.1f}\\% & {stats['segmented_words']:,} words \\\\
Morpheme type diversity & {stats['unique_morphemes']} types & Rich morphological analysis \\\\
\\bottomrule
\\end{{tabular}}
\\label{{tab:enhanced-results}}
\\end{{table}}
"""
    
    with open('enhanced_results_table.tex', 'w') as f:
        f.write(content.strip())
    print("saved enhanced_results_table.tex")

if __name__ == "__main__":
    stats = process_corpus()
    if stats:
        save_metrics(stats)
