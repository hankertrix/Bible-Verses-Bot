# Module that contains the lists of bible versions

# The tuple of accepted bible versions
bible_version_tuple = (

# English
"KJ21","ASV","AMP","AMPC","BRG","CSB","CEB","CJB","CEV","DARBY","DLNT","DRA","ERV","EHV","ESV","ESVUK","EXB","GNV","GW","GNT","HCSB","ICB","ISV","PHILLIPS","JUB","KJV","AKJV","LEB","TLB","MSG","MEV","NOG","NABRE","NASB","NASB1995","NCB","NCV","NET","NIRV","NIV","NIVUK","NKJV","NLV","NLT","NMB","NRSVUE","NRSVA","NRSVACE","NRSVCE","NTE","OJB","RGT","RSV","RSVCE","TLV","VOICE","WEB","WE","WYC","YLT",

# Chinese
"CCB","CCBT","ERV-ZH","CNVS","CNVT","CSBS","CSBT","CUVS","CUV","CUVMPS","CUVMPT","RCU17SS","RCU17TS")

# The set of accepted bible versions for faster checking
bible_version_set = {

# English
"KJ21","ASV","AMP","AMPC","BRG","CSB","CEB","CJB","CEV","DARBY","DLNT","DRA","ERV","EHV","ESV","ESVUK","EXB","GNV","GW","GNT","HCSB","ICB","ISV","PHILLIPS","JUB","KJV","AKJV","LEB","TLB","MSG","MEV","NOG","NABRE","NASB","NASB1995","NCB","NCV","NET","NIRV","NIV","NIVUK","NKJV","NLV","NLT","NMB","NRSVUE","NRSVA","NRSVACE","NRSVCE","NTE","OJB","RGT","RSV","RSVCE","TLV","VOICE","WEB","WE","WYC","YLT",

# Chinese
"CCB","CCBT","ERV-ZH","CNVS","CNVT","CSBS","CSBT","CUVS","CUV","CUVMPS","CUVMPT","RCU17SS","RCU17TS"}

# The tuple of bible versions that support apocrypha
apocrypha_supported = ("CEB","DRA","GNT","NABRE","NCB","NRSVUE","NRSVA","NRSVACE","NRSVCE","RSV","RSVCE","WYC")

# The set of bible versions that support apocrypha for faster checking
apocrypha_supported_set = {"CEB","DRA","GNT","NABRE","NCB","NRSVUE","NRSVA","NRSVACE","NRSVCE","RSV","RSVCE","WYC"}

# The set of bible versions that have additions
versions_w_additions = {

# Greek Esther
"CEB","NRSVUE","NRSVA","RSV",

# Esther
"NRSVACE","NRSVCE","RSVCE"

}

# The version mapping for old versions to new versions
version_map = {
  "NRSV" : "NRSVUE"
}