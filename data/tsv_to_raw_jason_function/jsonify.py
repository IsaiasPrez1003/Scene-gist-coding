import json
import os

INFILE_DIR = r"C:\Users\isaia\OneDrive\Desktop\Academic work\Scholarly activities\Research voluntering\Research voluntering 2024 Dr. Sanocki\Scene gist coding\data\tsv\Ad_Final_cleaned_14_scenes.tsv"
OUTFILE_DIR = r"C:\Users\isaia\OneDrive\Desktop\Academic work\Scholarly activities\Research voluntering\Research voluntering 2024 Dr. Sanocki\Scene gist coding\data\raw_json"
FILE_BASENAME = "Ad_final_cleaned_14_scenes"

DATA_IDX = (2, 51)

# Windoes encoding since I generated the tsv files on a Windows machine this
# time.
lines = open(INFILE_DIR, "r", encoding='windows-1252').read().splitlines()

data_lines = lines[DATA_IDX[0]:DATA_IDX[1]+1]

def process_lines(lines):
    dat = []
    for line in lines:
        elems = line.split('\t')
        print(line)
        assert(len(elems) == 16)
        pid, gender, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14 = elems
        dat.append({
            "pid": pid,
            "gender": gender,
            "response_texts": {
                "S1": S1,
                "S2": S2,
                "S3": S3,
                "S4" : S4,
                "S5" : S5,
                "S6" : S6,
                "S7" : S7,
                "S8" : S8,
                "S9" : S9,
                "S10": S10,
                "S11": S11,
                "S12": S12,
                "S13": S13,
                "S14": S14
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

