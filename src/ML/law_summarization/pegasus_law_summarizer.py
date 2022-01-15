import time
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

start_time = time.time()
tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

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
tokens = tokenizer.encode(
    law_text, truncation=True, padding="longest", return_tensors="pt"
)

summary = model.generate(tokens, max_length=200)

summarized_text = tokenizer.decode(summary[0])

print(summarized_text)
print("--- {:.2f} seconds ---".format(time.time() - start_time))