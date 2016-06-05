import math
import operator
import re

from django.core.exceptions import ObjectDoesNotExist

from search.models import Page, Word, Match
from src.build_index import BuildIndex
from src.html_to_text_converter import HtmlToTextConverter

EPS = 1e-6

class SearchEngine:
    def create_index(self, url):
        # url = "http://fapl.ru/"
        htmlToTextConverter = HtmlToTextConverter()
        text = htmlToTextConverter.transform_html_into_text(url)
        buildIndex = BuildIndex(text)
        index = buildIndex.getIndex()
        try:
            document = Page.objects.get(url=url)
            for match in Match.objects.filter(page=document):
                word = match.word
                match.delete()
                if not word.pages.all():
                    word.delete()
        except ObjectDoesNotExist:
            document = Page(url=url)
            document.save()
        for word in index.keys():
            positions = " ".join(str(x) for x in index[word])
            try:
                word = Word.objects.get(value=word)
            except ObjectDoesNotExist:
                word = Word(value=word)
                word.save()
            match = Match(word=word, page=document, positions=positions)
            match.save()

    def search_one_word(self, value):
        # import pdb; pdb.set_trace()
        pattern = re.compile(r'[-\[\].?!)(,:]')
        value = pattern.sub('', value)
        result_pages = []
        try:
            word = Word.objects.get(value=value)			
        except ObjectDoesNotExist:
            return result_pages

        matches = Match.objects.filter(word=word)
        for match in matches:
            page = Page.objects.get(id=match.page_id)
            result_pages.append(page.url)

        return result_pages

    def _split_text_on_words(self, text):
        pattern = re.compile(r'[-\[\].?!)(,:]')
        return pattern.sub(' ', text).split()

    def search_text(self, text):
        list_of_results = []
        words = self._split_text_on_words(text.lower())
        if not words:
            return list_of_results
        for word in words:
                list_of_results.append(self.search_one_word(word))
        return list(set(list_of_results[0]).intersection(*list_of_results))

    def search_phrase(self, phrase):
        # import pdb; pdb.set_trace()
        list_of_results = []
        words = self._split_text_on_words(phrase.lower())
        if not words:
            return list_of_results
        for word in words:
            list_of_results.append(self.search_one_word(word))
        setted = set(list_of_results[0]).intersection(*list_of_results)
        result = []
        for url in setted:
            temp = []
            page = Page.objects.get(url=url)
            for word in words:
                w = Word.objects.get(value=word)
                match = Match.objects.get(page=page, word=w)
                positions=[]
                for pos in match.positions.split():
                    positions.append(int(pos))
                temp.append(positions)
            for i in xrange(len(temp)):
                for j in xrange(len(temp[i])):
                    temp[i][j] -= i
            if set(temp[0]).intersection(*temp):
                result.append(url)
        return result

    def _count_idf(self, N, n):
        res = math.log((N - n + 0.5) * 1.0 / (n + 0.5))
        if res < 0:
            res = EPS
        return res

    def rank_results(self, words, urls):
        # import pdb; pdb.set_trace()
        scores = {}
        pages = Page.objects.all()
        N = len(pages)
        k1 = 2.0
        b = 0.75
        average_size_of_document = 0
        for page in pages:
            average_size_of_document += page.word_set.count()
        average_size_of_document /= N
        for url in urls:
            score = 0.0
            for w in words:
                word = Word.objects.get(value=w)
                n = word.pages.count()
                idf = self._count_idf(N, n)
                if idf < 0:
                    continue
                page = Page.objects.get(url=url)
                number_of_words_on_page = page.word_set.count()
                number_of_occurrences = len(Match.objects.get(page=page,
                                            word=word).positions.split())
                frequency = number_of_occurrences * 1.0 / number_of_words_on_page
                r = frequency * (k1 + 1) / (frequency + \
                    k1 * (1 - b + b * number_of_words_on_page * 1.0 \
                    / average_size_of_document))
                score += r * idf
            scores[url] = score
        sorted_by_score_urls = sorted(scores.items(), key=operator.itemgetter(1),
                                    reverse=True)
        res = []
        for i in sorted_by_score_urls:
            res.append(i[0])
        return res
