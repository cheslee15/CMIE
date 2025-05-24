import base64
import requests
from openai import OpenAI
import sys
OPENAI_KEY = "Your OPENAI_KEY"

client = OpenAI(
    api_key=OPENAI_KEY,  # this is also the default, it can be omitted
)


def offlineImg_process(prompt, image_path, model="gpt-4o", max_tokens=1000, temperature=0.1):
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_KEY}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

f_direct = open("./prompts/direct_prompt.md")
prompt_direct = f_direct.read()


def direct_prompt(caption, image_path):
    prompt = prompt_direct.format(caption)
    res = offlineImg_process(prompt, image_path)
    return res


f_evidence_enhanced = open("./prompts/evidence_enhanced_prompt.md")
prompt_evidence_enhanced = f_evidence_enhanced.read()


def evidence_enhanced_prompt(caption, image_path, img_evidence_list):
    prompt = prompt_evidence_enhanced.format(caption, img_evidence_list)
    res = offlineImg_process(prompt, image_path)
    return res


f_coexistence = open("./prompts/coexistence.md")
prompt_coexistence = f_coexistence.read()


def coexistence_prompt(caption, image_path,tmp):
    prompt = prompt_coexistence.format(caption)
    res = offlineImg_process(prompt, image_path,tmp)
    return res


f_score = open("./prompts/image_title_score.md")
prompt_score = f_score.read()


def score_generate(type, image_path, to_be_scored, caption, entities,coexistence):
    f_example = open("./prompts/example_string.md")
    example_string = f_example.read()
    prompt = prompt_score.format(example_string, to_be_scored, caption,coexistence)
    res = offlineImg_process(prompt, image_path)
    return res


f_CMIE = open("./prompts/final_decision.md")
prompt_CMIE = f_CMIE.read()


def Final_Pred(caption, coexistence, image_title_score, entity, image_path):
    f = open("./prompts/final_decision.md", encoding='utf-8')
    prompt = prompt_CMIE.format(caption, coexistence, image_title_score, entity)
    res = offlineImg_process(prompt, image_path)
    return res