from coincap import CoinCap

AVAILABLE_CURRENCIES = ['usd', 'eur', 'btc', 'ltc', 'zec', 'eth']


class CryptoBot(object):

    def __init__(self, webhook_url, currency='usd'):
        self.webhook_url = webhook_url
        self.coincap = CoinCap()
        if currency.lower() in AVAILABLE_CURRENCIES:
            self.currency = currency.lower()
        else:
            # Fallback to USD
            self.currency = 'usd'

    def _create_error(self, message):
        """

        """
        payload = {
            'response_type': "ephemeral",
            'text': message
        }
        return payload

    def _single_coin_post(self, coin_ticker):
        """

        """
        coin = self.coincap.get_coin_detail(coin_ticker)
        if coin:
            payload = {
                'response_type': 'in_channel',
                'text': '*<http://coincap.io/{}|{}>* - ({})\n\n*Current Price: ${:0.2f}*'.format(
                    coin['id'], coin['display_name'], coin['id'], coin['price_' + self.currency]),
                'attachments': [self._create_attachment_with_coin_details(coin)]
            }
            return payload
        else:
            return self._create_error('That does not seem to be a valid ticker')

    def _create_attachment_with_coin_details(self, coin):
        """

        """
        attachment = {
            'fallback': '{}, current price: {}, 24 hour change: {}'.format(
                coin['display_name'], coin['price_' + self.currency], coin['cap24hrChange']),
            'color': '#008000' if coin['cap24hrChange'] > 0 else '#FF0000',
            'fields': [
                {
                    'value': '*24 Hour Change:* {:>}%\n'.format(str(coin['cap24hrChange'])),
                    'short': 'false'
                },
                {
                    'value': '*Market Cap:* ${:,}\n'.format(coin['market_cap']),
                    'short': 'false'
                },
                {
                    'value': '*24 Hour Volume:* ${:,}\n'.format(coin['volume']),
                    'short': 'false'
                },
                {
                    'value': '*Available Supply:* {:,}\n'.format(coin['supply']),
                    'short': 'false'
                }
                    ]
            }
        return attachment

    def get_list_of_coins(self, limit=None):
        """

        :return:
        """
        coins = []
        top_coins = self.coincap.get_front()[:limit]
        response_string = "\n"
        for coin in top_coins:
            coins.append([coin['long'], coin['short']])
            response_string = response_string + '{} - `{}` *|* '.format(coin['long'], coin['short'])

        payload = {
            "response_type": "ephemeral",
            'attachments': [{
                "fallback": "List of coins",
                "color": "#008000",
                "text": response_string,
                "title": "Coins and tickers",
            }]
        }
        return payload

    def create_help_request(self):
        """
        """
        payload = {"text": "You can ask me things like \n*@cryptobot coins* - shows list of coin tickers","mrkdw": "true"}
        return payload

    def handle_request_for_coin(self, coin_ticker):
        """

        """
        return self._single_coin_post(coin_ticker)