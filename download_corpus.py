from datasets import load_dataset
from tqdm import tqdm

def download_data():
    # Download IndicCorp Malayalam
    print("downloading malayalam corpus...")
    
    # Use streaming mode
    # Load IndicCorp dataset
    try:
        dataset = load_dataset("ai4bharat/IndicCorpv2", "indiccorp_v2", split="mal_Mlym", streaming=True)
    except Exception as e:
        print(f"error loading dataset: {e}")
        return
    
    out_file = "malayalam_raw_corpus.txt"
    limit = 200000 # Set line limit
    
    print(f"saving to {out_file} (limit: {limit} lines)")
    
    count = 0
    with open(out_file, 'w', encoding='utf-8') as f:
        for item in tqdm(dataset):
            text = item.get('text', '').strip()
            
            # Skip short lines
            if len(text) < 20:
                continue
                
            f.write(text + '\n')
            count += 1
            
            if count >= limit:
                break
                
    print(f"done. saved {count} lines to {out_file}")

if __name__ == "__main__":
    download_data()
