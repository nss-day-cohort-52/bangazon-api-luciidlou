"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

# Marketing needs to know if users are actually using the favorited feature.
# Create a report showing all users that have favorited a store.

# Customer name header
# Bulleted list of store names


class FavoriteSellersList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT
                *
                FROM
                FAV_SELLERS
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            customers = []

            for row in dataset:

                store = {
                    "id": row['store_id'],
                    "name": row['store']
                }


                user_dict = next(
                    (
                        customer for customer in customers
                        if customer['user_id'] == row['user_id']
                    ),
                    None
                )
                
                if user_dict:
                    # If the user_dict is already in the customers list, append the store to the stores list
                    user_dict['stores'].append(store)
                else:
                    # If the user is not on the customers list, create and add the user to the list
                    customers.append({
                        "user_id": row['user_id'],
                        "full_name": row['customer'],
                        "stores": [store]
                    })

        # The template string must match the file name of the html template
        template = 'customers/favorite_sellers.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "customers": customers
        }

        return render(request, template, context)
