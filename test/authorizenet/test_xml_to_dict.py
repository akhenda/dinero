from lxml import etree
import unittest
from pprint import pprint

from dinero.ordereddict import OrderedDict

import dinero


barebones = ("<root><a>b</a></root>", OrderedDict([('a', 'b')]))

simple = (
    """
    <root>
      <x>
        <a>Text</a>
        <b>Something Else</b>
      </x>
    </root>
    """,
    OrderedDict([
        ('x', OrderedDict([
            ('a', 'Text'),
            ('b', 'Something Else'),
        ])),
    ])
)

list_example = (
    """
    <root>
      <messages>
        <message>1</message>
        <message>2</message>
        <message>3</message>
        <message>
          <a>Text</a>
        </message>
      </messages>
    </root>
    """,
    OrderedDict([
        ('messages', OrderedDict([
            ('message', [
                '1',
                '2',
                '3',
                OrderedDict([
                    ('a', 'Text'),
                ]),
            ]),
        ])),
    ])
)

comprehensive = (
    """
    <createTransactionResponse>
      <messages>
        <resultCode>Error</resultCode>
        <message>
          <code>E00027</code>
          <text>The transaction was unsuccessful.</text>
        </message>
      </messages>
      <transactionResponse>
        <responseCode>3</responseCode>
        <authCode/>
        <avsResultCode>P</avsResultCode>
        <cvvResultCode/>
        <cavvResultCode/>
        <transId>0</transId>
        <refTransID/>
        <transHash>D15F90A2DCF7B7FD7D15E220B7676708</transHash>
        <testRequest>0</testRequest>
        <accountNumber>XXXX1111</accountNumber>
        <accountType>Visa</accountType>
        <errors>
          <error>
            <errorCode>8</errorCode>
            <errorText>The credit card has expired.</errorText>
          </error>
        </errors>
      </transactionResponse>
    </createTransactionResponse>
    """,
    OrderedDict([
        ('messages', OrderedDict([
            ('resultCode', 'Error'),
            ('message', [
                OrderedDict([
                    ('code', 'E00027'),
                    ('text', 'The transaction was unsuccessful.'),
                ]),
            ]),
        ]),
        ),
        ('transactionResponse', OrderedDict([
            ('responseCode', '3'),
            ('authCode', ''),
            ('avsResultCode', 'P'),
            ('cvvResultCode', ''),
            ('cavvResultCode', ''),
            ('transId', '0'),
            ('refTransID', ''),
            ('transHash', 'D15F90A2DCF7B7FD7D15E220B7676708'),
            ('testRequest', '0'),
            ('accountNumber', 'XXXX1111'),
            ('accountType', 'Visa'),
            ('errors', OrderedDict([
                ('error', [
                    OrderedDict([
                        ('errorCode', '8'),
                        ('errorText', 'The credit card has expired.'),
                    ]),
                ])
            ]),
            ),
        ])),
    ])
)


class TestXmlToDict(unittest.TestCase):
    def _test(self, xml, should):
        xml = etree.XML(xml)
        actual = dinero.gateways.authorizenet_gateway.xml_to_dict(xml)

        if actual != should:
            pprint(actual)
            pprint(should)
        assert actual == should

    def test_barebones(self):
        self._test(*barebones)

    def test_simple(self):
        self._test(*simple)

    def test_list(self):
        self._test(*list_example)

    def test_comprehensive(self):
        self._test(*comprehensive)


class TestDictToXml(unittest.TestCase):
    def _test(self, should, dict, root):
        import textwrap
        xml = etree.XML(textwrap.dedent(should))
        actual = dinero.gateways.authorizenet_gateway._dict_to_xml(root, dict)

        assert etree.tostring(actual, pretty_print=True) == \
            etree.tostring(xml, pretty_print=True)

    def test_barebones(self):
        self._test(root='root', *barebones)

    def test_none_is_no_element(self):
        self._test(
            "<root></root>",
            OrderedDict([
                ('whatever', None),
            ]),
            root='root')

    def test_simple(self):
        self._test(root='root', *simple)

    def test_list(self):
        self._test(root='root', *list_example)

    def test_comprehensive(self):
        self._test(root='createTransactionResponse', *comprehensive)
