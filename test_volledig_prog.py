from test_module import find_title
from feature_fuzzy import feature_fuzzy
folder = "sbs16mining-linking-training-threads 2"
file = "thread_test.xml"
metadata_json = "sbs16mining.book-metadata.json"
ratio = 80

find_title(folder, metadata_json, ratio)

print(feature_fuzzy(file, ratio))