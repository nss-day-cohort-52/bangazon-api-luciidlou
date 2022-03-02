"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all


class ProductListMin1000(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT
                *
                FROM
                PRODUCTS_MIN_1000
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the games_by_user list:
            #
            # [
            #   {
            #     "id": 1,
            #     "full_name": "Admina Straytor",
            #     "games": [
            #       {
            #         "id": 1,
            #         "title": "Foo",
            #         "maker": "Bar Games",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       },
            #       {
            #         "id": 2,
            #         "title": "Foo 2",
            #         "maker": "Bar Games 2",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       }
            #     ]
            #   },
            # ]

            product_list = []

            for row in dataset:
                
                product = {
                    "name": row['product_name'],
                    "price": row['product_price'],
                    "description": row['product_description'],
                    "quantity": row['quantity'],
                    "location": row['location'],
                    "category": row['category']
                }
                
                product_list.append(product)

        # The template string must match the file name of the html template
        template = 'products/product_list_min_1000.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "product_list": product_list
        }

        return render(request, template, context)