import pdfplumber
from collections import Counter
import re
import json
import os

def extract_text_excluding_headers_and_footers(pdf_path, header_height=60, footer_height=60, repeat_threshold=0.7):
    header_lines = Counter()
    footer_lines = Counter()
    all_pages_text = []

    # First pass: Identify repeated header/footer lines
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        
        for page in pdf.pages:
            height = page.height
            lines = page.extract_text().split('\n')

            header = [line.strip() for line in lines if page.extract_words() and page.extract_words()[0]["top"] < header_height]
            footer = [line.strip() for line in lines if page.extract_words() and page.extract_words()[-1]["top"] > height - footer_height]

            header_lines.update(header)
            footer_lines.update(footer)

        common_headers = {line for line, count in header_lines.items() if count / total_pages >= repeat_threshold}
        common_footers = {line for line, count in footer_lines.items() if count / total_pages >= repeat_threshold}

    # Second pass: extract without header/footer
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            lines = page.extract_text().split('\n')
            cleaned = [
                line for line in lines
                if line.strip() not in common_headers and line.strip() not in common_footers
            ]
            all_pages_text.append("\n".join(cleaned))

    return "\n\n".join(all_pages_text)

def remove_frequent_header_footer(pages_text_lines, threshold=0.7):
    header_counter = Counter()
    footer_counter = Counter()
    total_pages = len(pages_text_lines)

    # First pass: count top and bottom lines across all pages
    for lines in pages_text_lines:
        if len(lines) == 0:
            continue
        header_counter[lines[0].strip()] += 1  # first line = potential header
        footer_counter[lines[-1].strip()] += 1  # last line = potential footer

    # Identify frequent headers/footers
    frequent_headers = {line for line, count in header_counter.items() if count / total_pages >= threshold}
    frequent_footers = {line for line, count in footer_counter.items() if count / total_pages >= threshold}

    # Second pass: remove them
    cleaned_pages = []
    for lines in pages_text_lines:
        new_lines = lines[:]
        if new_lines and new_lines[0].strip() in frequent_headers:
            new_lines = new_lines[1:]  # remove header
        if new_lines and new_lines[-1].strip() in frequent_footers:
            new_lines = new_lines[:-1]  # remove footer
        cleaned_pages.append("\n".join(new_lines))

    return "\n\n".join(cleaned_pages)

def pair_headings(headings):
    """
    Pair headings where each heading is paired with the next heading of same or higher level
    H1 pairs with next H1
    H2 pairs with next H2 or H1  
    H3 pairs with next H3, H2, or H1
    H4 pairs with next H4, H3, H2, or H1
    """
    pairs = []
    
    for i, current in enumerate(headings):
        current_level = int(current['level'][1])  # Extract number from 'H1', 'H2', etc.
        
        # Find next heading of same or higher level
        paired_with = None
        for j in range(i + 1, len(headings)):
            next_heading = headings[j]
            next_level = int(next_heading['level'][1])
            
            # If next heading is same or higher level (lower number), pair with it
            if next_level <= current_level:
                paired_with = next_heading
                break
        
        # Create pair
        if paired_with:
            pairs.append([current, paired_with])
        else:
            # Last heading or no matching pair
            pairs.append([current, None])
    
    return pairs

def getIndexOfMatch(s: str):
    """
    Find the index where heading s is found in lines
    Handle cases where heading might be split across multiple lines
    """
    s = s.strip()
    
    # First try exact match
    for i, line in enumerate(lines):
        if line.strip() == s:
            return i
    
    # Try building up text from consecutive lines
    for i in range(len(lines)):
        if not lines[i].strip():  # Skip empty lines
            continue
            
        # Start with current line
        combined = lines[i].strip()
        
        # Check if any part of the heading matches
        if any(word.lower() in combined.lower() for word in s.split()[:2]):  # First 2 words
            # Try combining with next lines
            for j in range(i + 1, min(i + 5, len(lines))):  # Look ahead max 5 lines
                if lines[j].strip():  # Only add non-empty lines
                    combined += " " + lines[j].strip()
                
                # Check if we found the complete heading
                if combined == s:
                    return j
                
                # Also check normalized versions (remove extra spaces, etc.)
                if " ".join(combined.split()) == " ".join(s.split()):
                    return j
    
    # If not found, return None instead of undefined behavior
    return None

final_dic = {}

# Usage
for file,json_output_1a in zip(sorted(os.listdir('input_1b_pdfs')),sorted(os.listdir('headings_classified'))):
    pdf_path = os.path.join('input_1b_pdfs',file)
    clean_text = extract_text_excluding_headers_and_footers(pdf_path)
    clean_text = re.sub(r'(.)\1{3,}', r'\1', clean_text)

    final_dic[file] = []

    with open(os.path.join('headings_classified',json_output_1a),'r') as f:
        data = json.load(f)

    headers_array = data['outline']

    pairs = pair_headings(headers_array)

    lines = clean_text.split('\n')
    lines = [ele.strip() for ele in lines]

    heading_to_content = {}

    # Updated main loop with better error handling
    heading_to_content = {}

    for header1, header2 in pairs:
        t1 = header1['text'].strip()
        t2 = header2['text'].strip() if header2 else None
        
        # print(f"Looking for: '{t1}'")
        
        idx1 = getIndexOfMatch(t1)
        
        if idx1 is None:
            # print(f"WARNING: Could not find heading '{t1}'")
            # Try to find partial matches for debugging
            # print("Searching for partial matches...")
            for i, line in enumerate(lines[:20]):  # Check first 20 lines
                if any(word.lower() in line.lower() for word in t1.split()[:2]):
                    print(f"  Line {i}: {line}")
            continue
        
        # Find end index
        if header2 is None:
            idx2 = len(lines)
        else:
            idx2 = getIndexOfMatch(t2) # type: ignore
            if idx2 is None:
                # print(f"WARNING: Could not find next heading '{t2}', using end of document")
                idx2 = len(lines)
        
        # print(f"Found '{t1}' at index {idx1}")
        # if header2:
        #     print(f"Found '{t2}' at index {idx2}")
        # else:
        #     print(f"Using end of document at index {idx2}")
        
        # Extract content between headings
        if idx1 is not None and idx2 is not None and idx1 < idx2:
            content_lines = []
            for i in range(idx1 + 1, idx2):
                if i < len(lines) and lines[i].strip():  # Skip empty lines
                    content_lines.append(lines[i])
            
            heading_to_content[t1] = '\n'.join(content_lines)
            # print(f"Extracted {len(content_lines)} lines of content")
        else:
            print(f"ERROR: Invalid indices - idx1: {idx1}, idx2: {idx2}")
        
        # print('=' * 50)
        final_dic[file].append({"heading":t1,"content":heading_to_content[t1],"page_number":header1['page']})

# Debug: Print first few headings and their content
# print("\nFirst few headings and their content:")
# for i, (heading, content) in enumerate(heading_to_content.items()):
#     if i >= 3:  # Only show first 3
#         break
#     print(f"\nHeading: {heading}")
#     print(f"Content preview: {content[:200]}...")

with open('temp/1.json','w') as file:
    file.write(json.dumps(final_dic,indent=2))