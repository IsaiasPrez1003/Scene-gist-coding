import json

from clip_embedder import CLIPTextEmbedder
from tqdm import tqdm
import os


INFILE_DIR = r"C:\Users\isaia\OneDrive\Desktop\Academic work\Scholarly activities\Research voluntering\Research voluntering 2024 Dr. Sanocki\Scene gist coding\data\raw_json\Ad_final_cleaned_14_scenes_manually_cleaned.json"
OUTFILE_DIR = r"C:\Users\isaia\OneDrive\Desktop\Academic work\Scholarly activities\Research voluntering\Research voluntering 2024 Dr. Sanocki\Scene gist coding\data\json_with_embeddings"
FILE_BASENAME = "Ad_final_cleaned_14_scenes_manual_encoding_cleanup_emb"

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
        "id": subjdata["Int_id"],
        "response_texts": { k: v.lower() for k, v in subjdata["response_texts"].items() },
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
# Make sure the model path is correct for your system!
print("Loading CLIP...")
clip = CLIPTextEmbedder()

print("Loading json data...")
jdat = json.load(open(INFILE_DIR, 'r'))


print("Processing data...")
newdat = {
    groupname: process_group(groupdata)
    for groupname, groupdata
    in jdat.items()
}

output_file_path = os.path.join(OUTFILE_DIR, FILE_BASENAME + ".json")

print("Writing new data...")
with open(output_file_path, "w") as out:
    out.write(json.dumps(newdat, indent=4))
 
print("Done!")


