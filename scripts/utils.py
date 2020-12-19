def get_topic_list():
	topics_list = {}
	topics_file = open('./topics.txt')

	for topic in topics_file:
		topics_list[topic.strip()] = topic.lower().replace(' ', '_').strip()

	return topics_list
