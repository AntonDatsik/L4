from django.core.exceptions import ObjectDoesNotExist

from search.models import Page, Word, Match
from src.build_index import BuildIndex
from src.html_to_text_converter import HtmlToTextConverter

class SearchEngine:
	def createIndex(self, url):
		url = "http://fapl.ru/"

		htmlToTextConverter = HtmlToTextConverter()


		text = htmlToTextConverter.transform_html_into_text(url)

		print text

		buildIndex = BuildIndex(text)
		index = buildIndex.getIndex()
		
		document = Page(url=url)
		document.save()
		for word in index.keys():
			positions = " ".join(str(x) for x in index[word])
			try:
				word = Word.objects.get(value=word)
				word.pages.add(document)
				word.save()
			except ObjectDoesNotExist:
				word = Word(value=word)
				word.save()
				word.pages.add(document)

			match = Match(word=word, pageId=document.id, positions=positions)
			match.save()

	def search_one_word(self, word):
		result_pages = list()
		word = str()
		try:
			word = Word.objects.get(value=word)			
		except ObjectDoesNotExist:
			return result_pages
			
		matches = Match.objects.filter(word=word)
		for match in matches:
			page = Page.objects.get(id=match.pageId)
			result_pages.add(page.url)

		return result_pages

	def search_many_words(self, words):
		pass
