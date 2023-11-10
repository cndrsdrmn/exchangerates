import os
import scrapy
from datetime import datetime
from scrapy.http import Request, Response
from scrapy.selector.unified import SelectorList
from typing import Iterable, Optional

from crawler.items import ExchangeRateItem


class BankIndonesiaTransactionRateSpider(scrapy.Spider):
    name = 'bank_indonesia_transaction_rate'

    __contents: Optional[SelectorList] = None
    __currency_code_idr: str = 'IDR'
    __currency_code_usd: str = 'USD'

    def start_requests(self) -> Iterable[Request]:
        start_url: str = os.environ.get('SPIDER_BANK_INDONESIA_URL')
        yield Request(url=start_url, dont_filter=True)

    def parse(self, response: Response) -> any:
        self.__contents: SelectorList = response.css('#ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_GridView1 table tbody')

        last_updated: str = response.css('#tableData .search-box-wrapper span::text').extract_first()
        transaction_date: str = self._format_transaction_date(date=last_updated)

        usd_rate: float = self._get_rate(code=self.__currency_code_usd)

        for row in self.__contents.css('tr'):
            content: SelectorList = row.css('td::text')
            code: str = content[0].extract().strip()

            # Get USD transaction details
            usd_transaction_code: str = self.__currency_code_idr if code == self.__currency_code_usd else code
            usd_transaction_rate: float = round(1 / usd_rate, 6) if code == self.__currency_code_usd else self._get_rate(code=code, default_rate=usd_rate)

            # Append transaction items
            yield from [
                ExchangeRateItem(
                    transaction_date=transaction_date,
                    transaction_rate=usd_transaction_rate,
                    base_currency=self.__currency_code_usd,
                    currency=self.__currency_code_idr if code == self.__currency_code_usd else usd_transaction_code,
                ),
                ExchangeRateItem(
                    transaction_date=transaction_date,
                    transaction_rate=self._get_rate(code=code),
                    base_currency=self.__currency_code_idr,
                    currency=code,
                )
            ]

    def _calculate_rate(self, sell: float, buy: float, denomination: float) -> float:
        amount: float = (sell + buy) / (2 * denomination)

        return round(amount, 6)
    
    def _format_transaction_date(self, date: str) -> str:
        formatted: str = datetime.strptime(date, '%d %B %Y')

        return datetime.strftime(formatted, '%Y%m%d')
    
    def _format_to_float(self, string: str) -> float:
        return float(string.replace(',', ''))

    def _get_rate(self, code: str, default_rate: Optional[float] = None) -> float:
        content: SelectorList = self.__contents.css(f'tr:contains("{code}") td::text')

        if default_rate is None:
            default_rate = float(content[1].extract())

        return self._calculate_rate(
            sell=self._format_to_float(content[2].extract()),
            buy=self._format_to_float(content[3].extract()),
            denomination=default_rate
        )