# Imposters dataset for the Cross-domain Authorship Attribution task at PAN-2019

This folder contains 4 subfolders, with standard collections of 5,000 imposter documents for each of the four languages (en, fr, it and sp) involved in the Cross-domain Authorship Attribution task at PAN 2019. Please note:
    - The imposter collections are not problem-specific and thus can be re-used for all problems inside one language.
    - Each language folder contains a metadata file with the `.json` extension. The metadata encodes the fandom of the imposter document, and thus offers topic-related information that can be exploited in your approaches. The fandom information will match the encoding in the development/evaluation problem folders (see the file "fandom-info.json" in each problem folder).
    - We offer the guarantee that the imposter document were not written by any of the authors who appear in the source or target sets for the problems in each language in the development/evaluation datasets. When selecting these texts, we have given preference to imposter texts from the fandoms covered in the development/evaluation problems, but if this selection was smaller than 5,000 texts, we have completed it with a random selection of other texts.

