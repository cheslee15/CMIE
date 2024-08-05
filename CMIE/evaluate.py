
import argparse
import json
from sklearn.metrics import classification_report, confusion_matrix


def main(args):
    pre_result_path = open(f"./result/{args.methods}_testSplit.json", encoding='utf-8')
    pre_results = json.load(pre_result_path)

    labels = []
    predictions = []
    current_index = 0

    for index, item in enumerate(pre_results):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file_name', type=str, default='data_testSplit.json', help='Input file name')
    parser.add_argument('--use_cache', action='store_true', default=False,
                        help='Use cache for modules except final prediction')
    parser.add_argument('--resume', action='store_true', default=True, help='Resume from the last time')
    parser.add_argument('--img_evidence_path', type=str,
                        default='E:\multi-fk\MC_online\data\\visual_search_testSplit_.json',
                        help='retrievaled image related titles')
    parser.add_argument('--methods', type=str, default='4o-CMIE', help='base model', choices=['4o-direct','4o-evidence-enhanced', '4o-CMIE', 'gemini-evidence-enhanced', 'gemini-CMIE'])

    args = parser.parse_args()
    print(args)
    main(args)