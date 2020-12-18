import wikipedia

def scrape_topics():
	TOPICS_FILE = open('./topics.txt')

	for topic in TOPICS_FILE:
		try:
			# Get the Wiki page for the topic
			page = wikipedia.page(topic)
		except wikipedia.DisambiguationError as error:
			# Error occurs if multiple similar pages exist for that topic
			# Pick the first by default. Can be changed to pick randomly
			page = wikipedia.page(error.options[0])

		# Generate the topic name and create a file to store scraped data
		# Converts from Neural networks to neural_networks
		topic_name = topic.lower().replace(' ', '_').strip()
		topic_file = open('./scraped_pages/' + topic_name +
						  '.txt', 'w', encoding='utf-8')

		# Write complete page data to file. Excludes lists and tables
		# Page can be stored as content or summary
		topic_file.write(page.content)

		# Close the file
		topic_file.close()

	TOPICS_FILE.close()

scrape_topics()
