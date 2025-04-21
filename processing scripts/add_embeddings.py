import json

from clip_embedder import CLIPTextEmbedder
from langchain.embeddings import LlamaCppEmbeddings
from tqdm import tqdm

INFILE_DIR = "raw_json/"
OUTFILE_DIR = "emb_json/"
FILE_BASENAME = "exp4-9-scene-pn23-update-3-22"

# Traverse through JSON file of the following format.
# {
#   <group> : [
#       {
#           "id" : <id>,
#           "response_texts": {
#               ...
#           }
#       },
#       ...
#   ],
#   ...
# }

#
# Helper functions.
#
def process_subject(subjdata):
    return {
        "pid": subjdata["id"],
        "response_texts": { k: v.lower() for k, v in subjdata["response_texts"].items() },
        "llama2_embs": {
            imglabel: llama2.embed_query(response.lower()) # Generate embedding
            for imglabel, response
            in subjdata["response_texts"].items()
        },
        "mistral_embs": {
            imglabel: mistral.embed_query(response.lower()) # Generate embedding
            for imglabel, response
            in subjdata["response_texts"].items()
        },
        "clip_embs": {
            imglabel: [x.item() for x in clip(response.lower()).cpu().detach()[0].numpy()] # Generate embedding
            for imglabel, response
            in subjdata["response_texts"].items()
        }
    }

def process_group(groupdata):
    return [process_subject(subjdata) for subjdata in tqdm(groupdata)]

#
# Main script.
#

print("Loading Llama 2...")
# Make sure the model path is correct for your system!
llama2 = LlamaCppEmbeddings(
    model_path="/home/gene/research/llama-2/models/llama-2-13b.Q4_K_M.gguf",
    verbose=False,
    n_ctx=2048,
    n_gpu_layers=43,
)

print("Loading Mistral...")
mistral = LlamaCppEmbeddings(
    model_path="/home/gene/research/llms/gguf_llms/models/mistral-7b-v0.1.Q4_K_M.gguf",
    verbose=False,
    n_ctx=2048,
    n_gpu_layers=31,
)

print("Loading CLIP...")
clip = CLIPTextEmbedder()

print("Loading json data...")
jdat = json.load(open(INFILE_DIR + FILE_BASENAME + ".json", 'r'))


print("Processing data...")
newdat = {
    groupname: process_group(groupdata)
    for groupname, groupdata
    in jdat.items()
}

print("Writing new data...")
with open(OUTFILE_DIR + FILE_BASENAME + "+llama2+mistral+clip_lowercase.json", "w") as out:
    out.write(json.dumps(newdat, indent=4))

print("Done!")

