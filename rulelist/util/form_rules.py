def bind_conditions(subgroup2add, current_candidate_pattern):
    """Connects (with logical AND) conditions and creates a pattern
    and calculates the number of conditions per pattern."""
    condition_counter = 0
    for iit, item in enumerate(subgroup2add.pattern):
        current_candidate_pattern += item.description
        current_candidate_pattern += " AND " if iit < len(subgroup2add.pattern) - 1 else ""
        condition_counter += 1

    #print("|p|:", condition_counter)      # cardinality of conditions in a pattern

    return current_candidate_pattern

def bind_antecedent_consequent(subgroup2add, current_candidate_pattern, class_labels): # added if category == 1 because it has already been binarised
    """Binds the pattern with each corresponding probability distribution over all class labels"""
    current_candidate_rule = current_candidate_pattern
    n = subgroup2add.usage
    label = 0
    for varname, usage_per_class in subgroup2add.statistics.usage_per_class.items():
        # current_candidate_rule += " : target = {}\t".format(varname) #name of the class label
        if len(class_labels) == 2 and label == 0:
            for category, n_class in usage_per_class.items():
                current_candidate_rule += " ".join([" Pr({}) = {}".format(class_labels[label], n_class / n)])
                label += 1
        else:
            current_candidate_rule += " ".join(
                 [" Pr({}) = {}".format(class_labels[label], n_class / n) for category, n_class in
                  usage_per_class.items() if category == 1])
            label += 1

    return current_candidate_rule