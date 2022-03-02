"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

# Marketing needs a report showing all orders that have not been paid for yet. Order by the created_on date, oldest first

# Order Id
# Customer name
# Total cost of all items on the order
# created_on

class OrderListIncomplete(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT
                *
                FROM
                INCOMPLETE_ORDERS
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            order_list = []

            for row in dataset:
                
                order = {
                    "id": row['order_id'],
                    "customer": row['customer'],
                    "order_total": row['order_total'],
                    "created_on": row['created_on'],
                }
                
                order_list.append(order)

        # The template string must match the file name of the html template
        template = 'orders/order_list_not_completed.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "orders_incomplete": order_list
        }

        return render(request, template, context)