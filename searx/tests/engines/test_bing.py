from collections import defaultdict
import mock
from searx.engines import bing
from searx.testing import SearxTestCase


class TestBingEngine(SearxTestCase):

    def test_request(self):
        query = 'test_query'
        dicto = defaultdict(dict)
        dicto['pageno'] = 0
        dicto['language'] = 'fr_FR'
        params = bing.request(query, dicto)
        self.assertTrue('url' in params)
        self.assertTrue(query in params['url'])
        self.assertTrue('bing.com' in params['url'])
        self.assertTrue('SRCHHPGUSR' in params['cookies'])
        self.assertTrue('fr' in params['cookies']['SRCHHPGUSR'])

        dicto['language'] = 'all'
        params = bing.request(query, dicto)
        self.assertTrue('SRCHHPGUSR' in params['cookies'])
        self.assertTrue('en' in params['cookies']['SRCHHPGUSR'])

    def test_response(self):
        self.assertRaises(AttributeError, bing.response, None)
        self.assertRaises(AttributeError, bing.response, [])
        self.assertRaises(AttributeError, bing.response, '')
        self.assertRaises(AttributeError, bing.response, '[]')

        response = mock.Mock(content='<html></html>')
        self.assertEqual(bing.response(response), [])

        response = mock.Mock(content='<html></html>')
        self.assertEqual(bing.response(response), [])

        html = """
        <div class="sa_cc" u="0|5109|4755453613245655|UAGjXgIrPH5yh-o5oNHRx_3Zta87f_QO">
            <div Class="sa_mc">
                <div class="sb_tlst">
                    <h3>
                        <a href="http://this.should.be.the.link/" h="ID=SERP,5124.1">
                        <strong>This</strong> should be the title</a>
                    </h3>
                </div>
                <div class="sb_meta"><cite><strong>this</strong>.meta.com</cite>
                    <span class="c_tlbxTrg">
                        <span class="c_tlbxH" H="BASE:CACHEDPAGEDEFAULT" K="SERP,5125.1">
                        </span>
                    </span>
                </div>
                <p><strong>This</strong> should be the content.</p>
            </div>
        </div>
        """
        response = mock.Mock(content=html)
        results = bing.response(response)
        self.assertEqual(type(results), list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'This should be the title')
        self.assertEqual(results[0]['url'], 'http://this.should.be.the.link/')
        self.assertEqual(results[0]['content'], 'This should be the content.')

        html = """
        <li class="b_algo" u="0|5109|4755453613245655|UAGjXgIrPH5yh-o5oNHRx_3Zta87f_QO">
            <div Class="sa_mc">
                <div class="sb_tlst">
                    <h2>
                        <a href="http://this.should.be.the.link/" h="ID=SERP,5124.1">
                        <strong>This</strong> should be the title</a>
                    </h2>
                </div>
                <div class="sb_meta"><cite><strong>this</strong>.meta.com</cite>
                    <span class="c_tlbxTrg">
                        <span class="c_tlbxH" H="BASE:CACHEDPAGEDEFAULT" K="SERP,5125.1">
                        </span>
                    </span>
                </div>
                <p><strong>This</strong> should be the content.</p>
            </div>
        </li>
        """
        response = mock.Mock(content=html)
        results = bing.response(response)
        self.assertEqual(type(results), list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'This should be the title')
        self.assertEqual(results[0]['url'], 'http://this.should.be.the.link/')
        self.assertEqual(results[0]['content'], 'This should be the content.')
