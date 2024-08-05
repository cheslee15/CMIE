You will receive an image and a text description, and your task is to determine if the image matches the text description. In addition, you will receive additional auxiliary information, including titles retrieved from images and matching analysis lists with images, entities extracted from images, and a simple coexistence relationship analysis. Coexistence relationship analysis shows a simple reason why images and text are matched together. Please combine other information and a given confidence score to comprehensively determine whether the given image and text are incorrectly matched. If there is clear evidence to refute, the image and text are considered false information. When you use your own knowledge to make judgments, you must ensure that you are confident. If there is no clear evidence to refute, it is considered that there is no false information.

Generate a JSON object with two properties: ***'label'***, ***'explanation'***. 
The return value of 'label' property should be selected from ["Yes", "No"].
Yes indicates there is misinformation between the given image and text.
No indicates that there is no misinformation between the given image and text.
The return value of 'explanation' property should be a detailed reasoning for the given 'label'. Please provide detailed steps for judging based on scores and other evidence.

Note that your response will be passed to the python interpreter, SO NO OTHER WORDS! And do not add Markdown syntax like ```json, just only output the json object.

Note that your response will be passed to the python interpreter, SO NO OTHER WORDS! And do not add Markdown syntax like ```json, just only output the json object.

Here is the ***text description***:
{}

Here is the ***coexistence relationship analysis*** of image and text:
{}

The following are **correlation score** and **explanation** of retrieved ***image titles*** and ***images***:
{}

Here is the ***entities*** exreacted from image:
{}

Your response：