from sentence_transformers import SentenceTransformer,util
from utils import content_dict,get_content_from_selected_headings,get_all_content
import json
import time

with open('temp/1.json') as f:
    output_1a = json.load(f)

with open('input_1b_json/1.json') as f:
    input_1b = json.load(f)

start = time.time()

# load model
model = SentenceTransformer('semantic_heading_ranker')

k = 5

pdf_names = list(output_1a.keys())

all_content = get_all_content(output_1a)

all_headings = [ele['heading'] for ele in all_content]
all_page_numbers = [ele['page_number'] for ele in all_content]
all_pdf_names = [ele['filename'] for ele in all_content]
heading_content_mapper = content_dict(all_content)

persona = input_1b['persona']['role']
job_to_be_done = input_1b['job_to_be_done']['task']

heading_model_input = persona + ' ' + job_to_be_done

# 1. Embed the persona+job
job_embedding = model.encode(heading_model_input, convert_to_tensor=True)

# 2. Embed all headings (say 100 from all PDFs)
heading_embeddings = model.encode(all_headings, convert_to_tensor=True)

# 3. Compute cosine similarity
cos_scores = util.pytorch_cos_sim(job_embedding, heading_embeddings).squeeze(0)

# 4. Get top-k matches
top_indices = cos_scores.argsort(descending=True)[:k]
selected_headings = [all_headings[i] for i in top_indices]
selected_pdf_names = [all_pdf_names[i] for i in top_indices]
selected_page_numbers = [all_page_numbers[i] for i in top_indices]

answer = get_content_from_selected_headings(
    headings=selected_headings, 
    pdf_names=pdf_names, 
    heading_content_mapper=heading_content_mapper, 
    input_1b=input_1b, 
    selected_headings=selected_headings,
    selected_page_numbers=selected_page_numbers,
    selected_pdf_names=selected_pdf_names,

)

# print(json.dumps(selected_headings, indent=2))

with open('output/output.json','w') as file:
    file.write(json.dumps(answer, indent=2))

# print(f"This step took {time.time() - start:4f} seconds")