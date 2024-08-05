
import argparse
import json
from openai import OpenAI

import ast

from utils import *
from sklearn.metrics import classification_report, confusion_matrix


def direct_reasoning(args, caption, image_path):
    for repeat in range(args.max_repeat):
        try:
            response = json.loads(direct_prompt(caption, image_path))
            print(response)
            return response
        except:
            continue
    return ""


def evidence_enhanced_reasoning(args, caption, image_path, img_evidence_list):
    for repeat in range(args.max_repeat):
        try:
            response = json.loads(evidence_enhanced_prompt(caption, image_path, img_evidence_list))
            print(response)
            return response
        except:
            continue
    return ""


def CMIE_reasoning(caption, image_path, visual_evidence, entity):
    for repeat in range(args.max_repeat):
        try:
            coexistence = json.loads(coexistence_prompt(caption, image_path))
            image_title_score = score_generate("image_title", image_path, visual_evidence, caption=caption, entities=entity, coexistence=coexistence)
            response = json.loads(CMIE(caption, coexistence, image_title_score, entity, image_path))
            print(response)
            return response
        except:
            continue
    return ""


def list_visual_evidence(visual_evidence):
    if visual_evidence['retrieved_text'] == "Nothing found":
        return []
    else:
        visual_evidence = visual_evidence['retrieved_text'][17:]
        visual_evidence = ast.literal_eval(visual_evidence)
        print(len(visual_evidence))
        for index in range(len(visual_evidence)):
            visual_evidence[index] = visual_evidence[index].replace("Title", f"{index+1}")
        return visual_evidence

def main(args):
    input_file = args.input_file_path
    with open(input_file, encoding='utf-8') as file:
        data = json.load(file)
    total_data_size = len(data)
    current_index = 0

    image_evidence_path = open(args.img_evidence_path, encoding='utf-8')
    image_evidence = json.load(image_evidence_path)

    labels = []
    predictions = []
    results_log = []

    if args.resume:
        pre_result_path = open(f"./result/{args.methods}_testSplit.json", encoding='utf-8')
        pre_results = json.load(pre_result_path)
        for index, item in enumerate(pre_results):
            result = {
                "image_id": item['image_id'], "article_id": item['article_id'], "falsified": item['falsified'],
                "caption": item['caption'],
                "image_title_score": item['image_title_score'],
                "coexistence": item['coexistence'],
                "entity": item['entity'],
                "prediction": item['prediction'],
                "explanation": item['explanation'],
            }
            results_log.append(result)
            if item['falsified'] == True:
                labels.append(1)
            else:
                labels.append(0)
            if item['prediction'] == 'Yes':
                predictions.append(1)
            else:
                predictions.append(0)
            current_index += 1

        print("Methods: ", args.methods)
        target_names = ['TrueInformation', 'MisInformation']
        print(classification_report(labels, predictions, target_names=target_names, digits=2))
        print(confusion_matrix(labels, predictions))
        print(current_index)

    for index in range(len(data)):
        if index < current_index:
            continue

        current_index += 1
        item = data[index]

        try:
            visual_evidence = list_visual_evidence(image_evidence[index])
        except:
            visual_evidence = []

        print("*" * 100)
        print('Processing index {}/{}'.format(current_index, total_data_size))

        image_path = item["image_url"]
        caption = item['caption']
        falsified = item["falsified"]
        print("image_path: ", image_path, "\n", "caption: ", caption, "\n", "falsified: ", falsified)
        entity = str(item['entity'])
        print(entity)
        print("*" * 20)

        if item['falsified'] == True:
            labels.append(1)
        else:
            labels.append(0)

        print("visual_evidence: ", visual_evidence)

        image_title_score = []
        coexistence = []

        if args.type == 'direct':
            response = direct_reasoning(args, caption, image_path)
        elif args.type == 'evidence-enhanced':
            if visual_evidence == []:
                response = direct_reasoning(args, caption, image_path)
            else:
                response = evidence_enhanced_reasoning(args, caption, image_path, visual_evidence)
        elif args.type == 'CMIE':
            if visual_evidence == []:
                response = direct_reasoning(args, caption, image_path)
            else:
                response = CMIE_reasoning(caption, image_path, visual_evidence, entity)

        try:
            if response['label'] == 'Yes':
                predictions.append(1)
            else:
                predictions.append(0)
        except:
            labels.pop()
            continue

        result = {
            "image_id": item['image_id'], "article_id": item['article_id'], "falsified": item['falsified'],"caption": item['caption'],
            "image_title_score": image_title_score,
            "coexistence": coexistence,
            "entity": entity,
            "prediction": response['label'],
            "explanation": response['explanation"'],
        }
        results_log.append(result)
        if current_index % 10 == 0:
            print("Proceccing evaluating...")
            print("Methods: ", args.methods)
            target_names = ['TrueInformation', 'MisInformation']
            print(classification_report(labels, predictions, target_names=target_names, digits=2))
            print(confusion_matrix(labels, predictions))

            with open(f"./result/{args.methods}_testSplit.json", 'w+', encoding='utf-8') as f:
                f.write(json.dumps(results_log, ensure_ascii=False, indent=4))

    print("Final evaluating...")
    print("Methods: ", args.methods)
    target_names = ['TrueInformation', 'MisInformation']
    print(classification_report(labels, predictions, target_names=target_names, digits=2))
    print(confusion_matrix(labels, predictions))
    with open(f"./result/{args.methods}_testSplit.json", 'w+', encoding='utf-8') as f:
        f.write(json.dumps(results_log, ensure_ascii=False, indent=4))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file_path', type=str, default='data_testSplit_entity.json', help='Input file name')
    parser.add_argument('--use_cache', action='store_true', default=False,
                        help='Use cache for modules except final prediction')
    parser.add_argument('--resume', action='store_true', default=True, help='Resume from the last time')
    parser.add_argument('--max_repeat', type=int, default=5)
    parser.add_argument('--img_evidence_path', type=str, default='',help='retrievaled image related titles')
    parser.add_argument('--type', type=str, default='CMIE')
    parser.add_argument('--methods', type=str, default='4o-CMIE', help='base model', choices=['4o-direct','4o-evidence-enhanced', '4o-CMIE', 'gemini-evidence-enhanced', 'gemini-CMIE'])

    args = parser.parse_args()
    print(args)
    main(args)