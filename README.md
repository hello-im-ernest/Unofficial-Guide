# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

The Unofficial St. Philip's College Survival Guide — real student knowledge about surviving and thriving at SPC that never appears in official handbooks or orientation packets. This includes honest professor reviews, financial aid tips, registration frustrations, campus safety concerns, and advice about programs like Alamo Promise. Official sources give the marketing version of college life; this system makes the real student experience searchable and answerable.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Niche.com | Student reviews | https://www.niche.com/colleges/st-philip-s-college/reviews/ |
| 2 | Niche.com Academics | Student reviews | docs/spc_niche_academics.txt |
| 3 | RateMyProfessors | Professor reviews | docs/rmp_mccall.txt |
| 4 | RateMyProfessors | Professor reviews | docs/rmp_rlopez.txt |
| 5 | RateMyProfessors | Professor reviews | docs/rmp_slopez.txt |
| 6 | Google Reviews | Student reviews | docs/spc_google_reviews.txt |
| 7 | Alamo Colleges | Official program info | https://www.alamo.edu/promise/ |
| 8 | SPC Official | Academic calendar | docs/spc_academic_calendar.txt |
| 9 | SPC Official | Campus life | docs/spc_campus_life.txt |
| 10 | SPC Official | Student services | docs/spc_student_services.txt |

---

## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 75 characters

**Why these choices fit your documents:** Most source documents are short student reviews — 2 to 5 sentences expressing a single opinion or experience. A 500-character chunk captures one or two complete reviews without merging unrelated opinions. Overlap of 75 characters ensures that reviews spanning a chunk boundary are not lost. We initially used 300-character chunks but increased to 500 after observing high distance scores in retrieval, indicating chunks were too small to embed meaningfully.

**Final chunk count:** 133 chunks across 10 documents

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key required)

**Production tradeoff reflection:** For a real deployment serving SPC students, I would consider OpenAI's text-embedding-3-small for higher accuracy on domain-specific text, but it costs money per API call and requires an internet connection. all-MiniLM-L6-v2 runs locally with no rate limits, which is ideal for a student project. Since St. Philip's serves a large Spanish-speaking population, a production system would benefit from a multilingual model like paraphrase-multilingual-MiniLM-L12-v2 to handle queries in Spanish. Context length is not a concern here since our chunks are short, but for longer documents a model with a larger context window would be needed.

---

## Grounded Generation

**System prompt grounding instruction:** "You are a helpful student guide for St. Philip's College. Answer using only the information in the provided documents. Do not draw on outside knowledge. If the documents don't contain enough information to answer, say so explicitly. Always state which source document your answer comes from."

**How source attribution is surfaced in the response:** Retrieved chunks are passed to the model labeled as [Source 1 - filename], [Source 2 - filename], etc. The model is instructed to cite these labels in its response. Additionally, the unique source filenames are programmatically extracted from the retrieved chunks and displayed separately in the Sources field of the Gradio interface, independent of what the model writes.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is the Alamo Promise and who is eligible? | Covers tuition gap for Bexar County high school seniors who enroll in fall after graduation and complete FAFSA/TASFA | Correctly described Alamo Promise as a tuition gap program, listed eligibility requirements, cited alamo_promise.txt | Relevant | Accurate |
| 2 | What do students say about Professor McCall's class? | Easy exams, source code required, videos to follow, quick email responses | Correctly described easy exams, source code requirement, Programming II comparison, cited rmp_mccall.txt | Relevant | Accurate |
| 3 | Is St. Philip's College safe at night? | Some students report feeling unsafe due to homeless individuals near campus at night | System said documents did not contain enough information about campus safety at night | Off-target | Partially accurate |
| 4 | What student services are available at St. Philip's College? | Advising, tutoring (Math World, Learning and Writing Center), career services, disability support | Correctly listed Math World, Learning and Writing Center, advisors, MESA, online support options | Relevant | Accurate |
| 5 | What do students say about the registration process? | Students report frustrating portal, hard to reach humans, ambiguous deadlines | System said documents did not mention the registration process | Off-target | Inaccurate |

---

## Failure Case Analysis

**Question that failed:** "What do students say about the registration process at St. Philip's College?"

**What the system returned:** "The provided documents do not contain enough information to answer the question about the registration process at St. Philip's College."

**Root cause (tied to a specific pipeline stage):** This is a retrieval failure. The relevant content exists in spc_niche_reviews.txt — a student review describes the student portal as "extraordinarily frustrating" and mentions ambiguous deadlines and difficulty reaching humans. However, the chunk containing this review lost the semantic search to chunks from spc_niche_academics.txt, which dominated results with generic academic content. The 500-character chunk size caused the registration complaint to be embedded alongside unrelated content, diluting its semantic signal and preventing it from ranking highly for a registration-specific query.

**What you would change to fix it:** Two fixes would help. First, clean spc_niche_reviews.txt to separate individual reviews into clearly labeled sections, so each chunk contains one focused review rather than fragments of multiple reviews. Second, add a dedicated document specifically about registration experiences — either by collecting more targeted reviews mentioning "registration" or "portal" or by writing a summary of common registration complaints from the source material.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the chunking strategy in planning.md before touching any code forced me to think through why 300 characters fit short reviews before discovering through testing that it didn't work well enough. Having the spec meant I had a clear baseline to compare against when retrieval results were poor — I knew exactly what I had intended and could reason about why it wasn't working rather than guessing blindly.

**One way your implementation diverged from the spec, and why:** The spec specified 300-character chunks with 50-character overlap, but during testing the distance scores were consistently high (above 0.85), indicating weak matches. I increased chunk size to 500 characters with 75-character overlap after observing that short chunks were embedding too vaguely to distinguish between different topics. The spec was updated to reflect this change.

---

## AI Usage

**Instance 1**
- *What I gave the AI:* My Chunking Strategy and Documents sections from planning.md, plus the requirement to load .txt files from a /docs folder
- *What it produced:* A complete ingest.py with load_documents() and chunk_text() functions using a sliding window approach with the specified chunk size and overlap
- *What I changed or overrode:* I increased CHUNK_SIZE from 300 to 500 and OVERLAP from 50 to 75 after testing showed the original values produced chunks too small to embed meaningfully

**Instance 2**
- *What I gave the AI:* My Retrieval Approach section from planning.md and the requirement to use ChromaDB and all-MiniLM-L6-v2
- *What it produced:* A complete retriever.py with embed_and_store() and retrieve() functions using ChromaDB's PersistentClient and sentence-transformers
- *What I changed or overrode:* I increased TOP_K from 4 to 6 after observing that relevant chunks were not appearing in the top 4 results for some queries
