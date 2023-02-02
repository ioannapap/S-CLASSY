from rulelist.rulelistmodel.categoricalmodel.categoricalstatistic import CategoricalFreeStatistic, CategoricalFixedStatistic
from rulelist.rulelistmodel.categoricalmodel.mdl_categorical import length_rule_fixed_categorical, \
    length_rule_free_categorical
from rulelist.util.form_rules import bind_conditions, bind_antecedent_consequent
from rulelist.rulelistmodel.rulesetmodel import RuleSetModel
from rulelist.util.extra_maths import log2_0


default_rule_statistic_categorical = {
    "discovery": CategoricalFixedStatistic,
    "prediction": CategoricalFreeStatistic
}

compute_default_length_categorical = {
    "discovery": length_rule_fixed_categorical,
    "prediction": length_rule_free_categorical
}

class CategoricalRuleList(RuleSetModel):
    """ Categorical rule list model
    """

    def __init__(self, data, task, max_depth, beam_width, min_support, max_rules, alpha_gain):
        self.max_depth, self.l_combination_pattern, self.l_attribute_item, self.log_prior_class= \
            self._create_constants(data,max_depth)
        super().__init__(data, task, max_depth, beam_width, min_support, max_rules, alpha_gain)
        self.min_support = max(min_support, 4)

    def init_default_statistics(self, data):
        return default_rule_statistic_categorical[self.task](data)

    def init_subgroup_statistics(self, data):
        return CategoricalFreeStatistic(data)

    def compute_default_length(self, default_rule_statistics):
        return compute_default_length_categorical[self.task](self, default_rule_statistics)

    def _create_constants(self, data, max_depth):
        self.max_depth, self.l_combination_pattern, self.l_attribute_item =\
            RuleSetModel._create_constants(self,data,max_depth)
        # compute nml normalizing constant
        #self.log_nml_comp = {(n_points, n_classes): log2(multinomial_with_recurrence(n_classes,n_points))
        #                     if n_points != 0 else 0 for n_points in range(0,datastructure.number_instances+1)
        #                     for n_classes in datastructure.targets_info.number_classes.values()}
        self.log_prior_class = {varname:
                                {category: -log2_0(count/data.number_instances) for category, count in counts.items()}
                                for varname, counts in data.targets_info.counts.items()}
        return self.max_depth, self.l_combination_pattern, self.l_attribute_item, self.log_prior_class

    def _add_description_rules(self, class_labels):

        text2add = ""
        rule_counter = 1
        for isub, subgroup in enumerate(self.subgroups):
            text2add += "IF " if isub == 0 else "ELSE IF "

            text2add = bind_conditions(subgroup, text2add)

            text2add += " THEN " + \
                        "usage = " + str(subgroup.statistics.usage) + ";" + " "

            text2add = bind_antecedent_consequent(subgroup, text2add, class_labels)

            text2add += "".join("\t")
            rule_counter += 1

        #print("|R|:", rule_counter-1)       # minus the default rule (as defined in the definitions of the paper)
        return text2add

    def _add_description_lastrule(self, class_labels): 

        text2add = "ELSE " +\
                   "usage = " + str(self.default_rule_statistics.usage) + ";" + " "
        n = self.default_rule_statistics.usage
        label = 0       # position of the first class label in class_labels list
        if self.task == "discovery":
            for varname, prob_per_class in self.default_rule_statistics.prob_per_classes.items():
                #text2add += " : target = {}".format(varname)
                if len(class_labels) == 2 and label == 0:
                    for category, prob in prob_per_class.items():
                        text2add += " ".join([" Pr({}) = {}".format(class_labels[label], prob)])
                        label += 1

                else:
                    text2add += " ".join([" Pr({}) = {}".format(class_labels[label], prob)      # here, it had before category instead of class_labels[label]
                                 for category, prob in prob_per_class.items() if category == 1])
                    label += 1
        else:
            for varname, usage_per_class in self.default_rule_statistics.usage_per_class.items():
                #text2add += " : target = {}".format(varname)
                if len(class_labels) == 2 and label == 0:
                    for category, n_class in usage_per_class.items():
                        text2add += " ".join([" Pr({}) = {}".format(class_labels[label], n_class / n)])
                        label += 1
                else:
                    text2add += " ".join(
                        [" Pr({}) = {}".format(class_labels[label], n_class / n) for category, n_class in
                         usage_per_class.items() if category == 1])
                    label += 1
        return text2add

    def add_description(self, class_labels):
        
        self.description = self._add_description_rules(class_labels) + self._add_description_lastrule(class_labels)
        
        print("Rule list:", self.description)
        
        #with open("rule_list.txt", "w") as f:
            #f.write(str(self.description))

        return self.description

    #-----------------------------------------------------------------------------------------------------------


