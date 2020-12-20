import wikipedia
import re


def scrape_topics(topic_list: dict):
    for topic, filename in topic_list.items():
        print("Scraping:", topic)
        try:
            # Get the Wiki page for the topic
            page = wikipedia.page(topic)
        except wikipedia.DisambiguationError as error:
            # Error occurs if multiple similar pages exist for that topic
            # Pick the first by default. Can be changed to pick randomly
            page = wikipedia.page(error.options[0])

        # Generate the topic name and create a file to store scraped data
        # Converts from Neural networks to neural_networks
        topic_file = open('./scraped_pages/' + filename +
                          '.txt', 'w', encoding='utf-8')

        # Write complete page data to file. Excludes lists and tables
        # Page can be stored as content or summary
        output = re.sub(r'\=\=+.*\n?', '', page.content)
        topic_file.write(output)

        # Close the file
        topic_file.close()
