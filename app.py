import json
from datetime import datetime
import sys
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from pdf_utils import extract_sections_from_pdfs
from embedding import get_embedder
from ranking import rank_sections
from summarise import summarize_subsections
from schemas import OutputSchema, Metadata, ExtractedSection, SubsectionAnalysis

def main(input_path: str, pdf_dir: str, output_path: str):
    with open(input_path, 'r') as f:
        input_data = json.load(f)
    
    documents = [doc['filename'] for doc in input_data['documents']]
    persona = input_data['persona']['role']
    job = input_data['job_to_be_done']['task']
    
    # Extract sections
    all_sections = extract_sections_from_pdfs(pdf_dir, documents)
    
    # Filter sections with non-empty text
    filtered_sections = [s for s in all_sections if s['text'].strip()]
    if not filtered_sections:
        raise ValueError("No text extracted from PDFs")
    
    # Embeddings
    embedder = get_embedder()
    query = f"Persona: {persona}. Job: {job}"
    query_emb = embedder(query)
    section_embs = embedder([s['text'] for s in filtered_sections])
    
    # Rank
    top_sections = rank_sections(filtered_sections, section_embs, query_emb)
    
    # Summarize subsections (here, treating sections as subsections for simplicity)
    subsection_analysis = summarize_subsections(top_sections)
    
    # Prepare output
    metadata = Metadata(
        input_documents=documents,
        persona=persona,
        job_to_be_done=job,
        processing_timestamp=datetime.now().isoformat()
    )
    extracted_sections = [
        ExtractedSection(
            document=s['document'],
            section_title=s['section_title'],
            importance_rank=s['importance_rank'],
            page_number=s['page_number']
        ) for s in top_sections
    ]
    subsection_summaries = [
        SubsectionAnalysis(
            document=s['document'],
            refined_text=s['refined_text'],
            page_number=s['page_number']
        ) for s in subsection_analysis
    ]
    output_data = OutputSchema(
        metadata=metadata,
        extracted_sections=extracted_sections,
        subsection_analysis=subsection_summaries
    )
    
    with open(output_path, 'w') as f:
        json.dump(output_data.model_dump(), f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python app.py <input_json> <pdf_dir> <output_json>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
