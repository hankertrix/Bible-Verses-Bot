# Module containing the bible books lists and dictionaries

# The short form that I'll convert into the code name
bibleshort = (

# Standard chapters  
"gen","exo","ex","lev","num","deu","jos","judg","rut","1 sam","2 sam","1 kin","2 kin","1 chr","2 chr","ezr","neh","est","job","psa","ps","pro","ecc","son","sol","isa","jer","lam","eze","dan","hos","joe","amo","oba","jon","mic","nah","hab","zep","hag","zec","mal","mt","mat","mar","mk","luk","joh","jn","jhn","act","rom","1 cor","2 cor","gal","eph","phili","phil","col","1 the","2 the","1 tim","2 tim","tit","phile","phlm","heb","jam","1 pet","2 pet","1 joh","1 jhn","2 jhn","2 joh","3 joh","jude","rev",

# Apocryphas
"tob","judi","greek est","wis","sir","bar","of jer","aza","sus","bel","dra","1 mac","2 mac","1 esd","man","of man","3 mac","2 esd","4 mac","men","to est"
)

# The code name to extract the verses mentioned
biblecode = (

# Standard chapters  
"Gen","Exod","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Ps","Prov","Eccl","Song","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Matt","Mark","Mark","Luke","John","John","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Phlm","Heb","Jas","1Pet","2Pet","1John", "1John","2John","2John","3John","Jude","Rev",

# Apocryphas
"Tob","Jdt","GkEsth","Wis","Sir","Bar","EpJer","PrAzar","Sus","Bel","Bel","1Macc","2Macc","1Esd","PrMan","PrMan","3Macc","2Esd","4Macc","SgThree","AddEsth"
)

# The dictionary to unlock the code name for the bible book
bible_dict = dict(zip(bibleshort,biblecode))

# The tuple of bible chapters that can be accepted
bible_chapt = (

# Standard chapters  
"gen","genesis","ex","exodus","lev","leviticus","num","numbers","deut","deuteronomy","josh","joshua","judge","judges","ruth","1 sam","1 samuel","2 sam","2 samuel","1 king","1 kings","2 king","2 kings","1 chr","1 chron","1 chronicle","1 chronicles","2 chr","2 chron","2 chronicle","2 chronicles","ezra","neh","nehemiah","esth","esther","job","ps","psalm","psalms","prov","proverb","proverbs","ecc","eccl","ecclesiastes","of song","of songs","song","songs","of solomon","solomon","isa","isaiah","jer","jeremiah","lam","lamentation","lamentations","eze","ezek","ezekiel","ezekial","dan","daniel","hos","hosea","joel","amos","obad","obadiah","jon","jonah","micah","nah","nahum","hab","habakkuk","zep","zeph","zephaniah","hag","hagg","haggai","zec","zech","zechariah","mal","malachi","mt","mat","matt","matthew","mark","luk","luke","jn","jhn","john","acts","rom","romans","1 cor","1 corinthians","2 cor","2 corinthians","gal","galatians","eph","ephesians","phil","phili","philippians","col","colossians","1 thess","1 thes","1 thessalonians","1 tim","1 timothy","2 tim","2 timothy","tit","titus","phlm","phile","philemon","heb","hebrew","hebrews","jas","jame","james","1 pet","1 peter","2 pet","2 peter","1 jn","1 jhn","1 john","2 jn","2 jhn","2 john","3 jn","3 jhn","3 john","jude","rev","revelations","revelation",

# Apocryphas
"tob","tobit","jdt","judith","gk esth","gk esther","grk esth","grk esther","greek esth","greek esther","wis","wisdom","sir","sirach","bar","baruch","let of jer","letter of jer","letter of jeremiah","of azar","of azariah","azar","azariah","sus","susan","susanna","bel","drag","dragon","1 mac","1 macc","1 maccabees","2 mac","2 macc","2 maccabees","1 esd","1 esdra","1 esdras","man","of man","mana","of mana", "of manasseh","manasseh","3 mac","3 macc","3 maccabees","2 esd","2 esdra","2 esdras","4 mac","4 macc","4 maccabees","men","add to esth","add to esther","addition to esth","addition to esther","additions to esth","additions to esther"
)

# The tuple of bible codes to correspond to the list of bible chapters accepted
bible_chapt_code = (
  
# Standard chapters
"Gen","Gen","Exod","Exod","Lev","Lev","Num","Num","Deut","Deut","Josh","Josh","Judg","Judg","Ruth","1Sam","1Sam","2Sam","2Sam","1Kgs","1Kgs","2Kgs","2Kgs","1Chr","1Chr","1Chr","1Chr","2Chr","2Chr","2Chr","2Chr","Ezra","Neh","Neh","Esth","Esth","Job","Ps","Ps","Ps","Prov","Prov","Prov","Eccl","Eccl","Eccl","Song","Song","Song","Song","Song","Song","Isa","Isa","Jer","Jer","Lam","Lam","Lam","Ezek","Ezek","Ezek","Ezek","Dan","Dan","Hos","Hos","Joel","Amos","Obad","Obad","Jonah","Jonah","Mic","Nah","Nah","Hab","Hab","Zeph","Zeph","Zeph","Hag","Hag","Hag","Zech","Zech","Zech","Mal","Mal","Matt","Matt","Matt","Matt","Mark","Luke","Luke","John","John","John","Acts","Rom","Rom","1Cor","1Cor","2Cor","2Cor","Gal","Gal","Eph","Eph","Phil","Phil","Phil","Col","Col","1Thess","1Thess","1Thess","1Tim","1Tim","2Tim","2Tim","Titus","Titus","Phlm","Phlm","Phlm","Heb","Heb","Heb","Jas","Jas","Jas","1Pet","1Pet","2Pet","2Pet","1John","1John","1John","2John","2John","2John","3John","3John","3John","Jude","Rev","Rev","Rev",

# Apocryphas
"Tob","Tob","Jdt","Jdt","GkEsth","GkEsth","GkEsth","GkEsth","GkEsth","GkEsth","Wis","Wis","Sir","Sir","Bar","Bar","EpJer","EpJer","EpJer","PrAzar","PrAzar","PrAzar","PrAzar","Sus","Sus","Sus","Bel","Bel","Bel","1Macc","1Macc","1Macc","2Macc","2Macc","2Macc","1Esd","1Esd","1Esd","PrMan","PrMan","PrMan","PrMan","PrMan","PrMan","3Macc","3Macc","3Macc","2Esd","2Esd","2Esd","4Macc","4Macc","4Macc","SgThree","AddEsth","AddEsth","AddEsth","AddEsth","AddEsth","AddEsth"
)

# The dictionary to unlock the code for the bible book for full chapters
bible_chapt_dict = dict(zip(bible_chapt, bible_chapt_code))

# The set of bible books that only have one chapter
one_chapt_books = {"Obad", "Phlm", "Jude", "2John", "3John"}
