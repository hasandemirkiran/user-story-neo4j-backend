import os
import string
import zeyrek
import nltk
import re
import csv


def all_functions():
    nltk.download('punkt')
    analyzer = zeyrek.MorphAnalyzer()

    stopwords = []
    id_count = 0
    # $sentence: [$role, $action, $action_object, $action_place, $action_tool, $benefit_action, $benefit_object, $benefit_place, $benefit_tool]
    # if not exist => 'null'
    sentence_dictionary = {}

    with open("./files/turkish_stopwords.txt", 'r', encoding='utf-8') as file:
        stopwords = file.read().splitlines()

    with open('./files/separated_sentences.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "ActionRole", "ActionObject", "ActionPlace", "ActionTool", "ActionTime", "Action",
                        "BenefitObject", "BenefitPlace", "BenefitTool", "BenefitTime", "BenefitAction"])

    with open("./files/uploaded_file.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for words in lines:
            words = words.split()

            for i in range(len(words)):
                if not ("\'" or "-") in words[i]:
                    table = words[i].maketrans(
                        string.punctuation, (len(string.punctuation)) * " ")
                    words[i] = words[i].translate(table).lower().strip()
                    words[i] = words[i].replace(" ", "")
            words_sw = [word for word in words if not word in stopwords]
            role_index = words_sw.index("olarak")
            role = " ".join(words_sw[0:role_index])
            action_index = words_sw.index("istiyorum") - 1
            action = words_sw[action_index]

            # item of action may include - object, place, tool
            action_item = words_sw[role_index + 1: action_index]
            flag_action_object = False
            flag_action_place = False
            flag_action_tool = False
            flag_action_time = False
            last_item = ''

            action_object_list = []
            action_place_list = []
            action_tool_list = []
            action_time_list = []

            action_tool_found = False

            for item in reversed(action_item):
                index_of_item = action_item.index(item)

                x = re.search("[i, ı, u , ü]$", item)
                y = re.search("de$|da$|te$|ta$|e$|a$|dan$|den$", item)
                z = re.search("le$|la$|ile$", item)
                k = re.search("ğında$|ğinde$|ğunda$|ğünde$", item)

                # check if the type is new for this item
                is_new_type = False

                lemmatized = analyzer.lemmatize(item)[0][1][0].replace("-", "")
                analyzed = analyzer.analyze(item)[0][0][2].lower()

                if lemmatized.lower() != item.lower():
                    if x and not flag_action_object and not action_tool_found:
                        last_item = 'action_object'
                        flag_action_object = True
                        action_object_list.append(item)
                        is_new_type = True

                    elif k and not flag_action_time and not action_tool_found:
                        last_item = 'action_time'
                        flag_action_time = True
                        action_time_list.append(item)
                        is_new_type = True

                    elif z and not flag_action_tool:
                        last_item = 'action_tool'
                        flag_action_tool = True
                        action_tool_list.append(item)
                        is_new_type = True
                        action_tool_found = not action_tool_found

                    elif y and not flag_action_place and not action_tool_found:
                        lemmatized_verb_check = re.search(
                            "mak$|mek$", lemmatized)
                        item_verb_check = re.search("ma$|me$", item)
                        if lemmatized_verb_check and item_verb_check:
                            pass
                        else:
                            last_item = 'action_place'
                            flag_action_place = True
                            action_place_list.append(item)
                            is_new_type = True

                elif index_of_item == len(action_item) - 1 and analyzed == "noun":
                    last_item = 'action_object'
                    flag_action_object = True
                    action_object_list.append(item)
                    is_new_type = True

                if not is_new_type:
                    if last_item == 'action_object' or last_item == '':
                        action_object_list.append(item)
                    elif last_item == 'action_place':
                        action_place_list.append(item)
                    elif last_item == 'action_tool':
                        action_tool_list.append(item)
                    elif last_item == 'action_time':
                        action_time_list.append(item)

            action_object = " ".join(reversed(action_object_list))
            action_place = " ".join(reversed(action_place_list))
            action_tool = " ".join(reversed(action_tool_list))
            action_time = " ".join(reversed(action_time_list))

            print(words_sw)
            if "böylece" in words_sw:
                benefit_action = analyzer.lemmatize(words_sw[-1])[0][1][-1]
                boylece_index = words_sw.index("böylece") + 1
                benefit_action_item = words_sw[boylece_index: -1]

                flag_benefit_action_object = False
                flag_benefit_action_place = False
                flag_benefit_action_tool = False
                flag_benefit_action_time = False
                last_benefit_item = ''

                action_benefit_object_list = []
                action_benefit_place_list = []
                action_benefit_tool_list = []
                action_benefit_time_list = []

                action_benefit_tool_found = False

                for item in reversed(benefit_action_item):
                    x = re.search("[i, ı, u , ü]$", item)
                    y = re.search("de$|da$|te$|ta$|e$|a$|dan$|den$", item)
                    z = re.search("le$|la$|ile$", item)
                    k = re.search("ğında$|ğinde$|ğunda$|ğünde$", item)

                    # check if the type is new for this item
                    is_new_benefit_type = False

                    lemmatized_benefit = analyzer.lemmatize(
                        item)[0][1][0].replace("-", "")
                    analyzed_benefit = analyzer.analyze(item)[0][0][2].lower()

                    if lemmatized_benefit.lower() != item.lower():
                        if x and not flag_benefit_action_object and not action_benefit_tool_found:
                            last_benefit_item = 'action_benefit_object'
                            flag_benefit_action_object = True
                            action_benefit_object_list.append(item)
                            is_new_benefit_type = True

                        elif k and not flag_benefit_action_time and not action_benefit_tool_found:
                            last_benefit_item = 'action_benefit_time'
                            flag_benefit_action_time = True
                            action_benefit_time_list.append(item)
                            is_new_benefit_type = True

                        elif z and not flag_benefit_action_tool:
                            last_benefit_item = 'action_benefit_tool'
                            flag_benefit_action_tool = True
                            action_benefit_tool_list.append(item)
                            is_new_benefit_type = True
                            action_benefit_tool_found = not action_benefit_tool_found

                        elif y and not flag_benefit_action_place and not action_benefit_tool_found:
                            lemmatized_benefit_verb_check = re.search(
                                "mak$|mek$", lemmatized_benefit)
                            item_benefit_verb_check = re.search(
                                "ma$|me$", item)
                            if lemmatized_benefit_verb_check and item_benefit_verb_check:
                                pass
                            else:
                                last_benefit_item = 'action_benefit_place'
                                flag_benefit_action_place = True
                                action_benefit_place_list.append(item)
                                is_new_benefit_type = True

                    elif index_of_item == len(benefit_action_item) - 1 and analyzed_benefit == "noun":
                        last_benefit_item = 'action_benefit_object'
                        flag_benefit_action_object = True
                        action_benefit_object_list.append(item)
                        is_new_benefit_type = True

                    if not is_new_benefit_type:
                        if last_benefit_item == 'action_benefit_object' or last_benefit_item == '':
                            action_benefit_object_list.append(item)
                        elif last_benefit_item == 'action_benefit_place':
                            action_benefit_place_list.append(item)
                        elif last_benefit_item == 'action_benefit_tool':
                            action_benefit_tool_list.append(item)
                        elif last_benefit_item == 'action_benefit_time':
                            action_benefit_time_list.append(item)

                action_benefit_object = " ".join(
                    reversed(action_benefit_object_list))
                action_benefit_place = " ".join(
                    reversed(action_benefit_place_list))
                action_benefit_tool = " ".join(
                    reversed(action_benefit_tool_list))
                action_benefit_time = " ".join(
                    reversed(action_benefit_time_list))

                with open('./files/separated_sentences.csv', 'a', encoding='UTF8', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(
                        ["US" + str(id_count), role, action_object, action_place, action_tool, action_time, action,
                         action_benefit_object, action_benefit_place, action_benefit_tool, action_benefit_time,
                         benefit_action])
                id_count += 1
            else:
                with open('./files/separated_sentences.csv', 'a', encoding='UTF8', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(
                        ["US" + str(id_count), role, action_object, action_place, action_tool, action_time, action, "", "", "", "", ""])
                id_count += 1
