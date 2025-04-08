from rest_framework.authentication import TokenAuthentication as BaseAuth


class TokenAuthentication(BaseAuth):
    """Default is Token"""

    keyword = "Bearer"
