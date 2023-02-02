from rulelist.util.read_from_file import read_file
from rulelist.search.beam.itemset_hybrid_search import find_best_data_mined_rule, find_best_hybrid_rule
from rulelist.util.fix_expert_knowledge import fix_expert_knowledge_format

def greedy_and_beamsearch_PRL(data, rulelist):
    """
    Probabilistic Rule List (PRL), CLASSY algorithm
    """

    while True:

        #print("Rule mining iteration: " + str(rulelist.number_rules + 1))
        subgroup2add = find_best_data_mined_rule(rulelist, data)
        #print('Local improvement (data structure) encoding: {}, support: {}\n'.format(subgroup2add.delta_data, subgroup2add.usage))
        #print('Variance : {} ; delta_data: {} ; support ; {}'.format(subgroup2add.statistics.variance, subgroup2add.delta_data,subgroup2add.usage ))
        if subgroup2add.score <= 0: break
        rulelist = rulelist.add_rule(subgroup2add, data)

    return rulelist

#-----------------------------------------------------------------------------------

def greedy_and_beamsearch_HRL(data, rulelist, expert_knowledge_filename):
    """
    Hybrid (Probabilistic) Rule List (HRL) S-CLASSY algorithm
    The user inserts the name of the file with expert knowledge; names such as: "expert_knowledge_top_K.csv", "expert_knowledge_bottom_K.csv", "expert_knowledge_random_K.csv"
    TODO: Transform this approach with yield so that it can be used also for data streams
    """

    expert_candidates = read_file(expert_knowledge_filename)
    expert_pattern_list, expert_selector_list = fix_expert_knowledge_format(expert_candidates)

    while True:

        #print("Rule mining iteration: " + str(rulelist.number_rules + 1))
        hybrid_subgroup2add, expert_selector_list= find_best_hybrid_rule(rulelist, data, expert_selector_list)
        #print('Local improvement (data structure) encoding: {}, support: {}\n'.format(hybrid_subgroup2add.delta_data, hybrid_subgroup2add.usage))
        #print('Variance : {} ; delta_data: {} ; support ; {}'.format(subgroup2add.statistics.variance, subgroup2add.delta_data, subgroup2add.usage ))
        if hybrid_subgroup2add.score <= 0: break
        rulelist = rulelist.add_rule(hybrid_subgroup2add, data)

    return rulelist

