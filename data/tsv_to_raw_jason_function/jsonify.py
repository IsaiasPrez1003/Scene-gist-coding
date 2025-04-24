import json
import os

INFILE_DIR = r"C:\Users\isaia\OneDrive\Desktop\Academic work\Scholarly activities\Research voluntering\Research voluntering 2024 Dr. Sanocki\Scene gist coding\data\tsv\Ad_Final_cleaned_14_scenes.tsv"
OUTFILE_DIR = r"C:\Users\isaia\OneDrive\Desktop\Academic work\Scholarly activities\Research voluntering\Research voluntering 2024 Dr. Sanocki\Scene gist coding\data\raw_json"
FILE_BASENAME = "Ad_final_cleaned_14_scenes_manually_cleaned"

DATA_IDX = (2, 51)

# Windoes encoding since I generated the tsv files on a Windows machine this
# time.
lines = open(INFILE_DIR, "r", encoding='utf-8').read().splitlines()

# Remove non-breaking spaces
lines = [line.replace('\u00a0', '').replace('\u2019', "'") for line in lines]

data_lines = lines[DATA_IDX[0]:DATA_IDX[1]+1]

def process_lines(lines):
    dat = []
    for line in lines:
        elems = line.split('\t')
        print(line)
        assert(len(elems) == 15)
        pid, Scene_1_Campsite, Scene_2_Woman_above_Canyon, Scene_3_Brick_Town_Wall, Scene_4_Surfers, Scene_5_Zero_Bench, Scene_6_Old_White_Wall, Scene_7_Deck_Lights, Scene_8_Dark_Alley, Scene_9_Bundled_Toddler, Scene_10_Mountains_and_Blue_Lake, Scene_11_Polluted_Lake, Scene_12_Man_in_Desert_with_Fire, Scene_13_Orange_Brick_City, Scene_14_Cobblestone_with_Trees = elems
        dat.append({
            "Int_id": pid,
            "response_texts": {
                "Scene_1_Campsite": Scene_1_Campsite,
                "Scene_2_Woman_above_Canyon": Scene_2_Woman_above_Canyon,
                "Scene_3_Brick_Town_Wall": Scene_3_Brick_Town_Wall,
                "Scene_4_Surfers" : Scene_4_Surfers,
                "Scene_5_Zero_Bench" : Scene_5_Zero_Bench,
                "Scene_6_Old_White_Wall" : Scene_6_Old_White_Wall,
                "Scene_7_Deck_Lights" : Scene_7_Deck_Lights,
                "Scene_8_Dark_Alley" : Scene_8_Dark_Alley,
                "Scene_9_Bundled_Toddler" : Scene_9_Bundled_Toddler,
                "Scene_10_Mountains_and_Blue_Lake": Scene_10_Mountains_and_Blue_Lake,
                "Scene_11_Polluted_Lake": Scene_11_Polluted_Lake,
                "Scene_12_Man_in_Desert_with_Fire": Scene_12_Man_in_Desert_with_Fire,
                "Scene_13_Orange_Brick_City": Scene_13_Orange_Brick_City,
                "Scene_14_Cobblestone_with_Trees": Scene_14_Cobblestone_with_Trees
            }
        })
    return dat

print("Processing lines...")
proc_data = process_lines(data_lines)

jdat = {
    "file": proc_data,
}

output_file_path = os.path.join(OUTFILE_DIR, FILE_BASENAME + ".json")


print("Writing results to file...")
with open(output_file_path, 'w') as out:
    out.write(json.dumps(jdat, indent=4))

print("Done!")

