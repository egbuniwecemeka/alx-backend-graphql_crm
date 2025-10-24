#!/usr/bin/env python3

import graphene

class CRMQuery():
    hello = graphene.String(default_value='Hello, GraphQL!')


class CreateCustomer(graphene.Mutation):
    ok = graphene.Boolean()
    customer_name = graphene.String()
    customer_email = graphene.String()
    customer_phone = graphene.String()

    class Arguments():
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, name, email):
        ok = True
        return CreateCustomer(customer_name=name, customer_email=email, ok=ok)
