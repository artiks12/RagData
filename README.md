# RagData
This is the repository to retrieve data from Latvian laws stored in Likumi.lv. It is a part of the master thesis "Evaluation and Adaptation of Large Language Models for Question-Answering on Legislation" made in University of Latvia.

### How to Use
This script was used with Python 3.10 so it is recomended to use this version of python. You also need to install PyQuery and requests packages.

LikumuSaraksts.json file is provided as an example of what is expected as input for the script. You need to specify the full list of urls on your own in the same format. List of Laws used in thesis is available here: https://html-preview.github.io/?url=https://github.com/artiks12/CitationsToMaster/blob/main/laws.html. Once it is done, run the likumi.py file and you should get every single law separately in Laws folder, as well as all of them combined in CombinedLaws.json file.

The CombinedLaws.json file was used to build a RAG framework as part of the thesis. The code to build the RAG framework is here: https://github.com/artiks12/RagCreationPipeline
