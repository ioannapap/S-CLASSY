def fix_expert_knowledge_format(rulelist):
	"""Creates a machine-readable format of expert knowledge separating patterns from selectors by '*'.
	Input: One list of knowledge (both patterns and selectors)
	Output: Two lists; expert_pattern_list, expert_selector_list
	e.g. expert_pattern_list: e.g.: ['flavanoids < 1.2 AND hue >= 1.1','...']
	e.g. expert_selector_list: ['color_intensity', 'flavonoids', 'hue']
	"""
	# TODO: expert_pattern_list to differentiate from extra expert_conditions_list
	expert_pattern_list = []
	expert_selector_list = []
	pattern_section = True

	for cand in rulelist:

		if cand != "*\n" and pattern_section:

			cand = cand.strip("\n")
			expert_pattern_list.append(cand)

		elif cand != "*\n" and not pattern_section:

			cand = cand.strip("\n")
			expert_selector_list.append(cand)

		elif cand == "*\n":

			pattern_section = False
			pass

	#print("Expert pattern list:	", expert_pattern_list)		# in this implementation no expert pattern knowledge is needed or given
	print("Preferred variables:	", expert_selector_list)

	return expert_pattern_list, expert_selector_list