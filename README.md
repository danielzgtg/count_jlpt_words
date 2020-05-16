# count_jlpt_words

Draws histograms for JLPT levels of words.

## Requirements

- Python 3.8
- The `anki` package installed
- Ubuntu 20.04 LTS (recommended)

## Setup

1. Create a folder called `res`
2. Add some data sets (see Data sets section)
3. Profit!

## Usage

The program is run like `./count.py`.

Input goes in stdin. Output comes out of stdout.

Analysis is done per continuous group of analyzable lines.
Non-analyzable lines pass through unchanged, while analyzable lines are replaced.
Whenever possible, words are extracted, classified into JLPT levels,
and are counted in a histogram that is printed out:

```
`N?: 18`

`N1: ###`

`N2: `

`N3: ####`

`N4: ###`

`N5: ######`

```

## Duolingo tree example

This project was used to generate https://forum.duolingo.com/comment/38712718

1. Go to https://forum.duolingo.com/comment/37599030
2. Select, copy, and paste the interesting part of the post and the comment into `input.txt`
3. Run the following code:
```shell script
cat input.txt |
  ./count.py |
  grep -v Tips |
  grep -v Number |
  grep -v Checkpoint |
  grep -v Words |
  sed -E 's/([^\n]+) \[test\]/## \1/' > \
  output.txt
```

## Data sets

Here is a list of lists of data sets that I found useful:

- https://ankiweb.net/shared/byauthor/391985566
- https://ankiweb.net/shared/byauthor/1315671747
- https://ankiweb.net/shared/byauthor/1914545596

Download the Kanji and Vocabulary decks. Do not download the grammar decks.

Here are the hashes of the data sets (verifying against this is optional):

```
$ sha256sum res/*
c07c2dde37f1e528b7bdd3977980e26429e305855bdb81f32396a0ab4bd248d7  res/JLPT_N1_-_Kanji_to_English.apkg
1860602b07e50be8d78175ab56ebd6b1879e66183aaf49f846c11958b38d8dbc  res/JLPT_N1_Vocabulary_-_Kanji_to_English.apkg
e90d5f5e4c11ac43643decdf24359a90d3ae8d46d7d63dd3900d554193dba006  res/JLPT-N1_words_in_jishoorg_2018.apkg
af92275bd053d66f13bd6450db7f456af61c28f4b6349cbf7cfaa27d0e04ee34  res/JLPT_N2_-_Kanji_to_English.apkg
ade1c99328342cdcd155a4edeed391b016fa4a75208a84c0294a5dcf630343e0  res/JLPT_N2_Vocabulary_-_Kanji_to_English.apkg
99f9dbd6288aa3247f8b0de47ad617e2810a978627e0a16866bd2a13319d17f6  res/JLPT-N2_words_in_jishoorg_2018.apkg
703d9467bb263f4d676146c430c19ee62039141d7b1013f8a03573d133f95959  res/JLPT-N3_words_in_jishoorg_2018.apkg
e12deddd6d33b4537544af264db3be1e6065cec6d1c0691d87a99cb9db6844f7  res/JLPT-N4_words_in_jishoorg_2018.apkg
406686c0b55147fba9ef0e1a6d25680fb4e9fad487affbe219361f8f2fbd0d4f  res/JLPT-N5_words_in_jishoorg_2018.apkg
16cf5eeb5ea7138cbe5431285bd158ad1129795cdc8a2958f23db73a1fef7d80  res/Pass_JLPT_N3_Kanji.apkg
832bb0a70905e91d38f362aa8cb7b9a6a82c8400fba144ada3bc095011e9b3ed  res/Pass_JLPT_N3_Vocabulary.apkg
aaa1f34e87f3ebf8e3af1163dda3bec770005b2086c8d9486ada5c4a5f5ddc39  res/Pass_JLPT_N4_Kanji.apkg
d0b85e4b19b385bb0d4a8e360591d5a3e8f96f49a8bc3750471594d306a6768f  res/Pass_JLPT_N4_Vocabulary.apkg
08cade46a97f58c2a91bc21e8f8cb6fa49a3abfc2bf206d894f3bc5e88435a9d  res/Pass_JLPT_N5_Kanji.apkg
7200340e9bdcc9598f2c673f1ca329e3010fa4c9f43d8fed68c8d7543d5c6dc0  res/Pass_JLPT_N5_Vocabulary.apkg
```

## Notes

- Do not use virtualenv
- The current working directory must be in the root of the Git repo
- Currently, it is the case that a large amount of words are not classified

## License

This project is licensed under the GNU General Public License v3.0 or any later version.
