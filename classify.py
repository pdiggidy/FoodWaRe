import json
import pandas
import re
import ast
import pickle

db = pandas.read_csv("recipes.csv")

kilo = re.compile("(?:\d+|\d+\.\d{1,3}) ?(?:kg|kilo)")
grams = re.compile("(\d+)g")
tbsp = re.compile("(\d) (?:tbsp)")
tsp = re.compile("^(\d) (?:tsp)")

total = 118


def check_amounts(ingredients, labels, index):
    global kilo, grams, total
    ingredients = json.loads(ingredients)
    labels = [int(x) for x in ast.literal_eval(labels)]
    valid = []
    amounts = []
    for i in range(len(labels)):
        if labels[i] != -1:
            valid.append(i)
    ing = list(ingredients.values())
    for x in valid:
        try:
            amount = int(ing[x])
        except:
            if ing[x] == "None":
                amount = -1
                continue
            if ing[x] == "freshly ground":
                amount = -1
                continue
            k = re.search(kilo, ing[x])
            g = re.search(grams, ing[x])
            t = re.search(tbsp, ing[x])
            p = re.search(tsp, ing[x])

            if not k and not g and not t and not p:
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
                elif t:
                    try:
                        amount = int(t.group(1)[0]) * 15
                    except IndexError as e:
                        try:
                            print(g.groups())
                            amount = int(input("Input amount manually"))
                        except AttributeError as a:
                            print(ing[x])
                            amount = int(input("Input amount manually"))
                elif p:
                    try:
                        amount = int(p.group(1)[0]) * 15
                    except IndexError as e:
                        try:
                            print(g.groups())
                            amount = int(input("Input amount manually"))
                        except AttributeError as a:
                            print(ing[x])
                            amount = int(input("Input amount manually"))

            amounts.append(amount)
    print(amounts, f'{(index / total) * 100}% Complete')

    return amounts


amounts = []
with open("indexes", "rb") as infile:
    dic = pickle.load(infile)

for index, row in db.iterrows():
    if index <= max(list(dic.keys())):
        continue
    print(index)
    m = check_amounts(row["Ingredients"], row["id_list"], index)
    amounts.append(m)
    dic[index] = m
    with open("indexes", 'wb') as file:
        pickle.dump(dic, file)

db["amounts"] = list(dic.values())

db.to_csv("Recipes_new.csv")
