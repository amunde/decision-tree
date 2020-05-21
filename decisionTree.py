import sys


def read_file(filename):
    with open(filename, 'r') as file:
        file_data = file.read()

    rows_data = file_data.split('\n')

    rows_array = []  # rows_array is a 2D array of the string data

    for index in range(1, len(rows_data) - 1):  # Excluded 1st and last row as they are names and empty
        rows_array.append(rows_data[index].split('\t'))

    return rows_array



def column_names(filename):
    with open(filename, 'r') as file:
        file_data = file.read()

    rows_data = file_data.split('\n')

    column_name_array = rows_data[0].split('\t')  # 0 as we are only extracting the header

    return column_name_array


# Calculating the Gini Impurity
def gini_impurity(data_dictionary, total_samples):
    # THIS IS FOR A SINGLE NODE IN THE TREE

    local_data_dictionary = data_dictionary.copy()

    value_to_subtract = 0

    for key, value in local_data_dictionary.items():
        local_data_dictionary[key] = (value / total_samples) ** 2

        value_to_subtract = value_to_subtract + (local_data_dictionary[key])

        # print(value_to_subtract)

    return (1 - value_to_subtract)


def calculate_weighted_average(inner_dictionary):

    total_number_of_rows = 0

    gini_impurity_value_for_label = {}
    # To store the gini values of the data
    

    for key, value in inner_dictionary.items():

        samples_after_split = 0

        for count in value.values():
            total_number_of_rows = total_number_of_rows + count
            # To calculate total count for finding the weighted average
            # Eg - total rows 149

            samples_after_split = samples_after_split + count

        gini_impurity_value_for_label[key] = gini_impurity(inner_dictionary[key], samples_after_split)

    weighted_average = 0

    for key, value in inner_dictionary.items():

        count_for_label = 0

        for count in value.values():
            count_for_label = count_for_label + count
            # eg - for 'y' rows = 49
            # To calculate count for a particular label

        value_for_single_label = gini_impurity_value_for_label[key] * (count_for_label / total_number_of_rows)

        weighted_average = weighted_average + value_for_single_label

    return weighted_average


def calculate_gini_gain(file_data):
    # For calculating the gini impurity before the split
    dictionary_before_split = {}

    for row in file_data:

        if row[-1] in dictionary_before_split:

            dictionary_before_split[row[-1]] += 1

        else:
            dictionary_before_split[row[-1]] = 1

    gini_impurity_before_split = gini_impurity(dictionary_before_split, len(file_data))

    # print("Gini Impurity before split = ", gini_impurity_before_split)

    gini_gain_list = []
    # To store the gini gain for each attribute

    attribute_label_dictionary_list = []
    # List of the dictionaries for each attribute after split


    for i in range(0, (len(file_data[0]) - 1)):

        attribute_values_data = []

        label_values_data = []

        attribute_label_set = set()
        # To calculate the unique values in the attribute

        predict_label_set = set()
        # To calculate the unique values in the final label column

        for row in file_data:
            attribute_label_set.add(row[i])

            predict_label_set.add(row[-1])

        attribute_label_dictionary = {}
        # To store data in dictionary

        for label in attribute_label_set:

            inner_dictionary = {}
          

            for row in file_data:

                if (row[i] == label):  # To select a single class i.e. either y or n

                    if row[-1] in inner_dictionary:

                        inner_dictionary[row[-1]] += 1

                    else:

                        inner_dictionary[row[-1]] = 1

            # Calculating the Gini Index for the Dictionary for a particular label in the attribute

            number_of_rows_per_label = 0

            for value in inner_dictionary.values():
                number_of_rows_per_label = number_of_rows_per_label + value

            attribute_label_dictionary[label] = inner_dictionary

        attribute_label_dictionary_list.append(attribute_label_dictionary)

        weighted_average_for_attribute = calculate_weighted_average(attribute_label_dictionary)


        gini_gain = (gini_impurity_before_split - weighted_average_for_attribute)

        gini_gain_list.append(gini_gain)

        
    max_gini_gain_attribute = gini_gain_list.index(max(gini_gain_list))

    gini_gain_max = max(gini_gain_list)

    attribute_label_dictionary_for_max_gain = attribute_label_dictionary_list[gini_gain_list.index(max(gini_gain_list))]


    return max_gini_gain_attribute, gini_gain_max, attribute_label_dictionary_for_max_gain


def split_data(attribute, file_data):
    attribute_label_set = set()

    for row in file_data:
        attribute_label_set.add(row[attribute])

    attribute_label_dictionary = {}

    for label in attribute_label_set:

        attribute_label_dictionary[label] = []

        for row in file_data:

            if (row[attribute] == label):
                attribute_label_dictionary[label].append(row)

    return attribute_label_dictionary


def calculate_majority_label(value_dictionary):
    # print(value_dictionary)

    max_label = ""
    max_value = 0

    for inner_dictionary in value_dictionary:

        trial_dict = value_dictionary[inner_dictionary]

        for inner_key in trial_dict:

            if (trial_dict[inner_key] >= max_value):
                max_value = trial_dict[inner_key]

                max_label = inner_key

    return max_label


def convert_dictonary_format(dictionary_to_format):
    final_dictionary = {}

    for dictionary in dictionary_to_format.values():
        # print(dictionary)
        for inner_dictionary_key in dictionary.keys():
            # print(inner_dictionary_key)
            if inner_dictionary_key in final_dictionary:
                final_dictionary[inner_dictionary_key] = final_dictionary[inner_dictionary_key] + dictionary[
                    inner_dictionary_key]
            else:
                final_dictionary[inner_dictionary_key] = dictionary[inner_dictionary_key]
    return (final_dictionary)


def create_decision_tree(file_data, node, current_depth, max_depth):
    # print("Current node label = ",node.label)

    current_depth = current_depth + 1

    attribute_to_split_on, gini_gain_max, attribute_dictionary = calculate_gini_gain(file_data)
    # This function returns the index of attribute with highest gini gain, value of gini gain and the
    # dictionary associated with splitting that attribute

    node.value["Attribute index to split on"] = attribute_to_split_on

    node.value["Attribute dictionary for node"] = convert_dictonary_format(attribute_dictionary)

    # In the current node, store the value of index to split on and the dictionary to display for that attribute

    # print("File Data = ", file_data)

    # print("Attribute dictionary - ", attribute_dictionary)

    # print("Attribute to split on " + str(attribute_to_split_on))

    inner_dictionary = split_data(attribute_to_split_on, file_data)

    # print("Inner dictionary - ",inner_dictionary)

    # print("\n")

    sorted_keys = sorted(inner_dictionary.keys())

    if (len(sorted_keys) < 2 or (current_depth >= max_depth)):
        # print("attribute_dictionary")
        node.value["label"] = calculate_majority_label(attribute_dictionary)

        # print("MAX LABEL = ", node.value["label"])

        # print("***********************")

        return node

    # To store keys in lexicographical order

    node.left = Node()

    node.left.value["branch"] = sorted_keys[0]

    node.left.value["Parent attribute index"] = node.value["Attribute index to split on"]

    # print("Branch LEFT = ",node.left.value["branch"])

    node.right = Node()

    node.right.value["branch"] = sorted_keys[1]

    node.right.value["Parent attribute index"] = node.value["Attribute index to split on"]


    if (gini_gain_max > 0):

        # print(sorted_keys)

        node.left = create_decision_tree(inner_dictionary[sorted_keys[0]], node.left, current_depth, max_depth)

        # print("LEFT SORTING DONE")

        node.right = create_decision_tree(inner_dictionary[sorted_keys[1]], node.right, current_depth, max_depth)

        # print("RIGHT SORTING DONE")


    else:


        node.left.value["label"] = calculate_majority_label(attribute_dictionary)

        node.left.value["Attribute index to split on"] = attribute_to_split_on

        # node.right = Node()

        node.right.value["label"] = calculate_majority_label(attribute_dictionary)

        node.right.value["Attribute index to split on"] = attribute_to_split_on

    return node


def printPreorder(root, depth, column_data_values):
    if root:

        # now print the data of node
        if "branch" in root.value:
            # if "label" in root.value:
            # print('\t |-'*depth,  column_data_values[root.value["Parent attribute index"]],'=',root.value["branch"], ' ', root.value["Attribute dictionary for node"], "LABEL =", root.value["label"])
            # else:
            print('\t |-' * depth, column_data_values[root.value["Parent attribute index"]], '=', root.value["branch"],
                  ' ', root.value["Attribute dictionary for node"])
        else:
            print('\t |-' * depth, root.value["Attribute dictionary for node"])

        # First recur on left child
        printPreorder(root.left, depth + 1, column_data_values)

        # the recur on right child
        printPreorder(root.right, depth + 1, column_data_values)



def write_output_to_file(file_to_create, data_to_write):

    index = 0

    with open(file_to_create, 'w+') as filehandle:

        for label in data_to_write:

            filehandle.write(label)

            if(index != (len(data_to_write)-1)):

                filehandle.write('\n')

            index = index + 1


def generate_result_and_accuracy(file_data, root):
    label_list = []

    incorrect = 0

    for row in file_data:

        label_for_row = calculate_label_for_row(row, root)

        label_list.append(label_for_row)

        if (label_for_row != row[-1]):
            incorrect = incorrect + 1

    return label_list, (incorrect / len(file_data))


def calculate_label_for_row(row, node):
    attribute_value = row[node.value["Attribute index to split on"]]
    # Value of the attribute to split on for the row

    if "label" in node.value:
        return node.value["label"]

    # compare this value with the
    if (attribute_value == node.left.value["branch"]):

        return calculate_label_for_row(row, node.left)

    elif (attribute_value == node.right.value["branch"]):

        return calculate_label_for_row(row, node.right)


class Node:

    def __init__(self):
        self.value = {"Attribute index to split on": "", "Attribute dictionary for node": ""}  # Changed
        self.left = None
        self.right = None
        self.label = None



if __name__ == '__main__':

    fileTrain = sys.argv[1]

    fileTest = sys.argv[2]

    max_depth = int(sys.argv[3])  # index of attribute on which data is split

    training_label_filename = sys.argv[4]

    testing_label_filename = sys.argv[5]

    metrics_output_filename = sys.argv[6]

    train_file_data = read_file(fileTrain)

    test_file_data = read_file(fileTest)

    column_data_values = column_names(fileTrain)

    current_depth = -1

    root = create_decision_tree(train_file_data, Node(), current_depth, max_depth)

    printPreorder(root, 0, column_data_values)

    training_result_labels, training_accuracy = generate_result_and_accuracy(train_file_data, root)

    testing_result_labels, testing_accuracy = generate_result_and_accuracy(test_file_data, root)


    # Writing outputs to file

    write_output_to_file(training_label_filename, training_result_labels)

    write_output_to_file(testing_label_filename, testing_result_labels)


    # Writing metrics output to file

    fileWrite = open(metrics_output_filename, "w+")

    fileWrite.write("error(train): " + str(training_accuracy) + '\n')

    fileWrite.write("error(test): " + str(testing_accuracy))

    fileWrite.close()






