You are given an image and a piece of text. Your task is to predict whether there is misinformation between the given image and text.

Generate a JSON object with two properties: 'label', 'explanation'. 
The return value of 'label' property should be selected from ["Yes", "No"].
Yes indicates there is misinformation between the given image and text.
No indicates that there is no misinformation between the given image and text.
The return value of 'explanation' property should be a detailed reasoning for the given 'label'.
Note that your response will be passed to the python interpreter, SO NO OTHER WORDS! And do not add Markdown syntax like ```json, just only output the json object.

The given text:
{}

Your Response:
