# Third Party imports
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BlogPagination(PageNumberPagination):
    page_size = 5
    page_query_param = "page_size"


    def get_paginated_response(self, data):
        return Response(
            {
                "Links_Pagination": {
                    "Next_Page": self.get_next_link(),
                    "Previous": self.get_previous_link()
                },
                "Post_Count": self.page.paginator.count,
                "Total_Pages": self.page.paginator.num_pages,
                "results": data,
            }
        )