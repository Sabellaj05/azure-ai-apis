"""
    Conversational Language Understanding:
    Three key components

    Utterances: something someone might say for the app to interpret `switch on the fan`

    Entities: an item to which the utterances refers, ie: `fan`

    Intents: what the app should do, ie: `switch on`

    We have previously train and deploy a model on on 
    entities and intents along with sample utterances labeled for training and we want
    to predict entities and intents for a given utterance. the output will contain the top intent, recognize
    entities and confidence scores. 


    TO-DO:
        add more funcions, modularize the code


"""

import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

def clu_analyze_convo():


    load_dotenv()
    # secrets
    clu_endpoint = os.environ["AZURE_CONVERSATIONS_ENDPOINT"]
    clu_key = os.environ["AZURE_CONVERSATIONS_KEY"]
    project_name = os.environ["AZURE_CONVERSATIONS_PROJECT_NAME"]
    deployment_name = os.environ["AZURE_CONVERSATIONS_DEPLOYMENT_NAME"]

    client = ConversationAnalysisClient(clu_endpoint, AzureKeyCredential(clu_key))
    with client:
        query = "Switch on the light please"
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": query
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": project_name,
                    "deploymentName": deployment_name,
                    "verbose": True
                }
            }
        )

    # view result
    print(f"query: {result['result']['query']}")
    print(f"project kind: {result['result']['prediction']['projectKind']}\n")

    print(f"top intent: {result['result']['prediction']['topIntent']}")
    print(f"category: {result['result']['prediction']['intents'][0]['category']}")
    print(f"confidence score: {result['result']['prediction']['intents'][0]['confidenceScore']}\n")

    print("entities:")
    for entity in result['result']['prediction']['entities']:
        print(f"\ncategory: {entity['category']}")
        print(f"text: {entity['text']}")
        print(f"confidence score: {entity['confidenceScore']}")
        if "resolutions" in entity:
            print("resolutions")
            for resolution in entity['resolutions']:
                print(f"kind: {resolution['resolutionKind']}")
                print(f"value: {resolution['value']}")
        if "extraInformation" in entity:
            print("extra info")
            for data in entity['extraInformation']:
                print(f"kind: {data['extraInformationKind']}")
                if data['extraInformationKind'] == "ListKey":
                    print(f"key: {data['key']}")
                if data['extraInformationKind'] == "EntitySubtype":
                    print(f"value: {data['value']}")


clu_analyze_convo()
