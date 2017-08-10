import requests
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings

__all__ = (
    'FacebookLoginAPIView',
)


class FacebookLoginAPIView(APIView):
    FACEBOOK_APP_ID = '359278334486847'
    FACEBOOK_SECRET_CODE = '49a96598e984ad9dc3086b394bbbade0'
    APP_ACCESS_TOKEN = '{}|{}'.format(
        FACEBOOK_APP_ID,
        FACEBOOK_SECRET_CODE
    )

    def post(self, request):
        token = request.data.get('token')
        if not token:
            raise APIException('token require')

        # 프론트로부터 전달받은 token을 Facebook의 debug_token API를 이용해
        # 검증한 결과를 debug_result에 할당
        debug_result = self.debug_token(token)
        return Response(debug_result)

    def debug_token(self, token):
        """
        주어진 token으로
        :param token:
        :return:
        """
        url_debug_token = "https://graph.facebook.com/debug_token"
        url_debug_token_params = {
            'input_token': token,
            'access_token': self.APP_ACCESS_TOKEN,
        }
        response = requests.get(url_debug_token, url_debug_token_params)
        result = response.json()
        if 'error' in result['data']:
            raise APIException('token invalid')
        else:
            return result