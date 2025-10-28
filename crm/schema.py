#!/usr/bin/env python3

import graphene
from .models import Customers
import re

class CRMQuery():
    hello = graphene.String(default_value='Hello, GraphQL!')


class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)


class CreateCustomer(graphene.Mutation):
    ok = graphene.Boolean()
    customer_name = graphene.String()
    customer_email = graphene.String()
    customer_phone = graphene.String()

    class Arguments():
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=False)

    def mutate(self, name, email, phone):
        # Email uniqueness
        if Customers.objects.filter(email=email).exists:
            raise Exception('Email already exists')

        # Validate the phone number
        if phone and not re.match(r'^(\+?\d{10, 15}|\d{3}-\d{3}-\d{4})$', phone):
            raise Exception('Phone number format: +1234567890 or 123-456-7890')
        
        # Save to DB
        customer = Customers(name=name, email=email, phone=phone)
        customer.save()

        return CreateCustomer(
            ok = True,
            customer_name=customer.name,
            customer_email=customer.email,
            customer_phone=customer.phone
        )


class BulkCreateCustomers():
    ok = graphene.Boolean()
    customer_list = 


class CreateProduct():
    pass


class CreateOrder():
    pass


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
