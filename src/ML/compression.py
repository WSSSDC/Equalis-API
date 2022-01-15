from bz2 import compress


def compresor(data):
    compressed_data = compress(str.encode(data))
    compression_ratio = len(data) / len(compressed_data)
    return compressed_data, compression_ratio


law_names = [
    "access_to_information",
    "canada_emergency_response_benefit",
    "canada_labour_code",
    "canadian_elections",
    "competition_act",
    "contraventions",
    "controlled_drugs_and_substances",
]

for law_name in law_names:
    print(law_name.replace("_", " ").title())
index = int(input("Enter the index of the law you want to summarize: "))

filepath = (
    "C:/Users/arjun/Desktop/Deltahacks stuff/law_summarization/law_text/"
    + law_names[index]
    + ".txt"
)

with open(filepath, "r", encoding="utf8") as f:
    law_text = f.read()
compressed_law_text, compression_ratio = compresor(law_text)
print("The compression ratio is: {:2f}%".format(compression_ratio))
