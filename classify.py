import json
import pandas
import re
import ast

db = pandas.read_csv("recipes.csv")

kilo = re.compile("(?:\d+|\d+\.\d{1,3}) ?(?:kg|kilo)")
grams = re.compile("(\d+)g")
ml= re.compile()
litre = re.compile()

def check_amounts(ingredients, labels):
    global kilo, grams
    ingredients = json.loads(ingredients)
    labels = [int(x) for x in ast.literal_eval(labels)]
    valid = []
    amounts = []
    for i in range(len(labels)):
        if labels[i] != -1:
            valid.append(i)
    ing = list(ingredients.values())
    for x in valid:
        if ing[x] == "None":
            amount = None
            continue
        k = re.search(kilo, ing[x])
        g = re.search(grams, ing[x])

        if not k and not g:
            print(ing[x])
            amount = int(input("Input amount manually"))

        else:
            if g:
                try:
                    amount = int(g.group(1))
                except IndexError as e:
                    try:
                        print(g.groups())
                        amount = int(input("Input amount manually"))
                    except AttributeError as a:
                        print(ing[x])
                        amount = int(input("Input amount manually"))
            elif k:
                try:
                    amount = int(k.group(1)) * 1000
                except IndexError as e:
                    try:
                        print(g.groups())
                        amount = int(input("Input amount manually"))
                    except AttributeError as a:
                        print(ing[x])
                        amount = int(input("Input amount manually"))

        amounts.append(amount)
    return amounts


amounts = []

for index, row in db.iterrows():
    # ing = json.loads(row)
    amounts.append(check_amounts(row["Ingredients"], row["id_list"]))

db["amounts"] = amounts

db.to_csv("amounts_test.csv")
