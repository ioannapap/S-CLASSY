from rulelist.datastructure.subgroup import Subgroup
from rulelist.search.beam.beam import Beam
from rulelist.rulelistmodel.gain_add_rule import compute_delta_score, compute_statistics_newrules
from functools import reduce
import numpy as np
from gmpy2 import popcount, bit_mask

def find_best_data_mined_rule(rulelist, data):
    """ Finds the best rule using beam search given the rule list so far and the datastructure (bCLASSY)
    """
    subgroup2add = Subgroup()
    beam = Beam(rulelist.beam_width)

    for depth in range(rulelist.max_depth):  # stable to 5

        candidates = [pattern for ip, pattern in enumerate(beam.patterns)
                      if pattern not in beam.patterns[:ip]
                      and len(pattern) == depth
                      and beam.array_support[ip] > rulelist.min_support]
        beam = beam.clean()

        for candidate2refine in candidates:
            beam, subgroup2add = refine_subgroup(rulelist, data, candidate2refine, beam, subgroup2add)

    #print("Gain data structure: {}, gain model : {}, gain: {}".format(subgroup2add.delta_data, subgroup2add.delta_model, subgroup2add.score))

    return subgroup2add

def refine_subgroup(rulelist, data, candidate2refine, beam, subgroup2add):
    """ Expands a subgroup by adding an item from all other variables not included in the subgroup.
    """
    bitarray_candidate = reduce((lambda x, y: x & y), (item.bitarray for item in candidate2refine)) \
        if candidate2refine != [] else bit_mask(data.number_instances)
    bitarray_candidate = bitarray_candidate & rulelist.bitset_uncovered
    variable_list = [item.parent_variable for item in candidate2refine]

    for attribute in filter(lambda x: x.name not in variable_list, data.attributes):

        for item in attribute.generate_items(rulelist.bitset_uncovered & bitarray_candidate):
            bitarray_new_candidate = bitarray_candidate & item.bitarray
            usage = popcount(bitarray_new_candidate)

            if usage >= rulelist.min_support:
                new_subgroup_statistics, new_default_rule_statistics = \
                    compute_statistics_newrules(rulelist, data, bitarray_new_candidate)
                new_candidate = candidate2refine + [item]
                score, gain_data, gain_model = compute_delta_score(rulelist, new_candidate, new_subgroup_statistics, new_default_rule_statistics)

            else:
                score = np.NINF

            if score > subgroup2add.score:
                subgroup2add.update(new_candidate, new_subgroup_statistics, new_default_rule_statistics, gain_data, gain_model, score)
            if score > beam.min_score and set([item.description for item in new_candidate]) not in beam.set_patterns:
                beam.replace(new_candidate, score, usage)
                #print("CLASSY-Subgroup: {} ; score : {}".format([pat.parent_variable for pat in new_candidate], score))

    return beam, subgroup2add


def find_best_hybrid_rule(rulelist, data, expert_selector_list):
    """ Finds the best rule using expert knowledge and beam search given the rule list so far and the datastructure (S-CLASSY).
    """
    subgroup2add = Subgroup()
    beam = Beam(rulelist.beam_width)
    for depth in range(rulelist.max_depth):  # maximum number of conditions: stable to 5

        candidates = [pattern for ip, pattern in enumerate(beam.patterns)
                      if pattern not in beam.patterns[:ip]
                      and len(pattern) == depth
                      and beam.array_support[ip] > rulelist.min_support]
        beam = beam.clean()
        for candidate2refine in candidates:

            beam, subgroup2add, expert_selector_list = refine_hybrid_subgroup(rulelist, data, candidate2refine, beam, subgroup2add, expert_selector_list)

    #print("Gain data structure: {}, gain model : {}, gain: {}".format(subgroup2add.delta_data, subgroup2add.delta_model, subgroup2add.score))

    return subgroup2add, expert_selector_list


def refine_hybrid_subgroup(rulelist, data, candidate2refine, beam, subgroup2add, expert_selector_list):
    """ Selects the best rule between the bCLASSY candidate and the candidate that derives from preferred variables (hybrid cand) based on their score.
    """
    bitarray_candidate = reduce((lambda x, y: x & y), (item.bitarray for item in candidate2refine)) if candidate2refine != [] else bit_mask(data.number_instances)
    bitarray_candidate = bitarray_candidate & rulelist.bitset_uncovered
    variable_list = [item.parent_variable for item in candidate2refine]

    if variable_list and variable_list[0] in expert_selector_list:
        expert_selector_list.remove(variable_list[0])

    if expert_selector_list:

        for attribute in filter(lambda x: x.name not in variable_list and x.name in expert_selector_list, data.attributes):        # creates a focus area around the selectors as a head start: an item from all other variables not included in the variable list but included in the expert list

            for item in attribute.generate_items(rulelist.bitset_uncovered & bitarray_candidate):

                bitarray_new_candidate = bitarray_candidate & item.bitarray
                usage = popcount(bitarray_new_candidate)

                if usage >= rulelist.min_support:

                    new_subgroup_statistics, new_default_rule_statistics = compute_statistics_newrules(rulelist, data, bitarray_new_candidate)
                    new_candidate = candidate2refine + [item]
                    score, gain_data, gain_model = compute_delta_score(rulelist, new_candidate, new_subgroup_statistics, new_default_rule_statistics)
                else:
                    score = np.NINF

                if score > subgroup2add.score:
                    subgroup2add.update(new_candidate, new_subgroup_statistics, new_default_rule_statistics, gain_data, gain_model, score)

                if score > beam.min_score and set([item.description for item in new_candidate]) not in beam.set_patterns:
                    beam.replace(new_candidate, score, usage)     # set the new pattern
                    #print("(S-CLASSY) Subgroup: {} ; score : {}".format([pat.parent_variable for pat in new_candidate],score))

    else:   # if all the preferred variables (selectors) have been checked

        for attribute in filter(lambda x: x.name not in variable_list, data.attributes):
            for item in attribute.generate_items(rulelist.bitset_uncovered & bitarray_candidate):
                bitarray_new_candidate = bitarray_candidate & item.bitarray
                usage = popcount(bitarray_new_candidate)

                if usage >= rulelist.min_support:
                    new_subgroup_statistics, new_default_rule_statistics = compute_statistics_newrules(rulelist, data, bitarray_new_candidate)
                    new_candidate = candidate2refine + [item]
                    score, gain_data, gain_model = compute_delta_score(rulelist, new_candidate, new_subgroup_statistics, new_default_rule_statistics)
                else:
                    score = np.NINF

                if score > subgroup2add.score:
                    subgroup2add.update(new_candidate, new_subgroup_statistics, new_default_rule_statistics, gain_data, gain_model, score)

                if score > beam.min_score and set([item.description for item in new_candidate]) not in beam.set_patterns:
                    beam.replace(new_candidate, score, usage)
                    #print("(CLASSY) Subgroup: {} ; score : {}".format([pat.parent_variable for pat in new_candidate],score))

    return beam, subgroup2add, expert_selector_list
