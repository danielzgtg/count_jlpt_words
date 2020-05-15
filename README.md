# count_jlpt_words

## Requirements

- Python 3.8
- The `anki` package installed
- Ubuntu 20.04 LTS (recommended)

## Setup

1. Create a folder called `res`
2. Download the N5 to N1 Jisho Anki decks from https://ankiweb.net/shared/decks/jisho and place them inside
3. Verify the hashes against the Hashes section (optional)

## Usage

The program is run like `./count.py`.

Input goes in stdin. Output comes out of stdout.

Analysis is done per-line.
Non-analyzable lines pass through unchanged, while analyzable lines are replaced.
Whenever possible, words are extracted from each line, classified into JLPT levels,
and are counted in a histogram that is printed out:

```
N?: 18
N1: ###
N2: 
N3: ####
N4: ###
N5: ######
```

## Duolingo tree example

1. Go to https://forum.duolingo.com/comment/32529914
2. Select, copy, and paste everything between "Checkpoint 1" and "Total" into `input.txt`
3. Run the following code:
```shell script
cat input.txt |
  ./count.py |
  grep -v Tips |
  grep -v Number |
  grep -v Checkpoint |
  sed -E 's/([^\n]+) \[test\]/# \1/' > \
  output.txt
```

## Hashes

Here are the hashes of the `res` folder contents:

| Path | SHA256 |
| --- | --- |
| res/JLPT-N1_words_in_jishoorg_2018.apkg | e90d5f5e4c11ac43643decdf24359a90d3ae8d46d7d63dd3900d554193dba006 |
| res/JLPT-N2_words_in_jishoorg_2018.apkg | 99f9dbd6288aa3247f8b0de47ad617e2810a978627e0a16866bd2a13319d17f6 |
| res/JLPT-N3_words_in_jishoorg_2018.apkg | 703d9467bb263f4d676146c430c19ee62039141d7b1013f8a03573d133f95959 |
| res/JLPT-N4_words_in_jishoorg_2018.apkg | e12deddd6d33b4537544af264db3be1e6065cec6d1c0691d87a99cb9db6844f7 |
| res/JLPT-N5_words_in_jishoorg_2018.apkg | 406686c0b55147fba9ef0e1a6d25680fb4e9fad487affbe219361f8f2fbd0d4f |

## Notes

- Do not use virtualenv
- The current working directory must be in the root of the Git repo
- Currently, it is the case that a large amount of words are not classified
