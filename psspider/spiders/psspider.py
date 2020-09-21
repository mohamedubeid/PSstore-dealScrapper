import scrapy
from psspider.items import PsspiderItem


class Pspsider(scrapy.Spider):
    name = 'psspider'
    start_urls = ['https://store.playstation.com/en-us']

    def parse(self, response):
        for sale in response.css('div.left-panel ul.list a.listItem'):
            next_page = ''
            sidepanel = sale.css('a::text').get()
            if "Sale" in sidepanel or "Under" in sidepanel or "Deal" in sidepanel or "Discounts" in sidepanel:
                next_page = sale.css('a::attr(href)').get()
            if next_page is None:
                quit()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_games_lis)

    def parse_games_lis(self, response):
        sales = PsspiderItem()
        for row in response.css('div.grid-cell-row__container'):
            for eachgame in row.css(
                        'div.ember-view div.ember-view div.__desktop-presentation__grid-cell__base__0ba9f.ember-view'):
                for game in eachgame.css('div.grid-cell.grid-cell--game div.grid-cell__body'):
                    OGprice = game.css(
                            'div.grid-cell__bottom div.grid-cell__footer span.grid-cell__prices-container a div span div.price::text').get()
                    AfterCut = game.css(
                            'div.grid-cell__bottom div.grid-cell__footer span.grid-cell__prices-container a div h3::text').get()
                    GameName = game.css('a.internal-app-link.ember-view div.grid-cell__title span::text').get()
                    url = response.urljoin(game.css('a.internal-app-link.ember-view::attr(href)').get())
                    sales['name'] = cleaning(GameName)
                    sales['OGprice'] = cleaning(OGprice)
                    sales['AfterCut'] = cleaning(AfterCut)
                    sales['url'] = url
                    yield sales

        for footer in response.css('div.grid-body div.grid-cell-container div.grid-footer-controls'):
            for next in footer.css('div.paginator-control.__shared-presentation__paginator-control__b0a73 div.paginator-control__container'):
                next_page = next.css('a.paginator-control__next.paginator-control__arrow-navigation.internal-app-link.ember-view::attr(href)').get()
                if next_page is not None:
                    yield response.follow(next_page, callback=self.parse_games_lis)

def cleaning(data_extract):
    if data_extract is not None:
      replacable = ('-','+', '.', ')', '(')
      replace = ''
      executed = False
      is_there = False
      for letter in replacable:
        if letter in data_extract and executed == False:
          executed = True
          is_there = True
          replace = data_extract.replace(letter, '\\'+letter)
        elif letter in replace and executed == True:
          replace = replace.replace(letter, '\\'+letter)
      if is_there == False:
        replace = data_extract
      encodename = replace.encode('ascii', 'ignore')
      decodename = encodename.decode()
      return decodename.lower()