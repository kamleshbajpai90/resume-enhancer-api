import os
import openai
import json
from typing import Optional

OPENAI_API_KEY = "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"
# openai.api_key = os.getenv("OPENAI_API_KEY") 
openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = """You are a precise, honest resume coach. 
Return JSON only. Do not include commentary.
Focus on clarity, impact, and relevance for the target role."""

USER_PROMPT_TEMPLATE = """Resume:
---
{resume}

Job Description:
---
{jd}

Instructions:
1) Identify missing or weak keywords and competencies from the JD.
2) Suggest concrete bullet-level improvements for Experience, Skills, Summary.
3) Rewrite the Professional Summary for this role (max 90–120 words).
4) Quantify impact where possible (metrics; avoid fabrication).
5) Flag vague phrases and propose stronger alternatives.

Return JSON with keys:
- missing_keywords: string[]
- section_suggestions: {{
    summary: string[]
    experience: string[]
    skills: string[]
  }}
- rewritten_summary: string
- ats_tips: string[]"""


async def enhance_resume(resume_text: str, job_description: str, target_role: Optional[str] = None):
    prompt = USER_PROMPT_TEMPLATE.format(resume=resume_text, jd=job_description)
    if target_role:
        prompt += f"\n\nTarget role: {target_role}"

    resp = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    content = resp.choices[0].message["content"]
    return json.loads(content)
