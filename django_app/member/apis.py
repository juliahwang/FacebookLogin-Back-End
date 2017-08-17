import requests
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings

__all__ = (
    'FacebookLoginAPIView',
)

User = get_user_model()


class TokenUserInfoAPIView(APIView):
    def post(self, request):
        token_string = request.data.get('token')
        try:
            token = Token.objects.get(key=token_string)
        except Token.DoesNotExist:
            raise APIException('token invalid')
        user = token.user
        ret = {
            # 시리얼라이저
        }
        return Response(ret)


class FacebookLoginAPIView(APIView):
    FACEBOOK_APP_ID = ''
    FACEBOOK_SECRET_CODE = ''
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
        self.debug_token(token)
        user_info = self.get_user_info(token=token)

        # 이미 존재하면 가져오고 없으면 페이스북 유저 생성
        if User.objects.filter(username=user_info['id']).exists():
            user = User.objects.get(username=user_info['id'])
        else:
            user = User.objects.create_facebook_user(user_info)

        # DRF 토큰을 생성
        token, token_created = Token.objects.get_or_create(user=user)

        # 관련정보를 한번에 리턴
        ret = {
            'token': token.key,
            # 시리얼라이저를 거쳐서 출력하도록
            # 'user': UserSerializer(user).data,
        }
        return Response(ret)

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

    def get_user_info(user_id, token):
        url_user_info = 'https://graph.facebook.com/v2.9/me'
        url_user_info_params = {
            'access_token': token,
            # 권한을 요청하지 않아도 오는 기본 정보
            # 반드시 scope 내용을 적어줘야한다.
            'fields': ','.join([
                'id',
                'name',
                'first_name',
                'last_name',
                'picture.type(large)',
                'gender',
            ])
        }
        response = requests.get(url_user_info, params=url_user_info_params)
        result = response.json()
        return result