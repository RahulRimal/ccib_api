from rest_framework.response import Response
from rest_framework import status

import logging

logger = logging.getLogger(__name__)

def api_response_success(data, status=status.HTTP_200_OK):

    return Response(data, status)


def api_response_error(data, status=status.HTTP_400_BAD_REQUEST):
    logger.error(data)
    return Response(data, status)
