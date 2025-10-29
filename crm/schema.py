#!/usr/bin/env python3

import graphene
from .models import Customer
import re


class Meta:
    model = Customer
    fields = ("id", "name", "email", "phone")


class CRMQuery():
    hello = graphene.String(default_value='Hello, GraphQL!')


class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)


class CreateCustomer(graphene.Mutation):
    # Inputs
    ok = graphene.Boolean()
    customer = graphene.Field(CustomerType)

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=False)

    # Validations
    def mutate(self, name, email, phone):
        # Email uniqueness
        if Customer.objects.filter(email=email).exists():
            raise Exception('Email already exists')

        # Validate the phone number
        if phone and not re.match(r'^(\+?\d{10, 15}|\d{3}-\d{3}-\d{4})$', phone):
            raise Exception('Phone number format: +1234567890 or 123-456-7890')
        
        # Save to DB
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()

        return CreateCustomer(
            ok = True,
            customer=customer
        )


class CustomerInput(graphene.InputObjectType):
    """ Customer structure """
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)


class BulkCreateCustomers(graphene.Mutation):
    """ """
    ok = graphene.Boolean()
    customer_list = graphene.List(
        graphene.NonNull(graphene.String)
    )

    class Argument:
        """  """
        ok = graphene.Boolean()
        customer_list = graphene.List(
            graphene.NotNull(CustomerInput, required=True)
        )
    
    def mutate(self, info, customer_list):
        """ """
        created_customers = []

        for customer_info in customer_list:
            name = customer_info.name
            email = customer_info.email
            phone = customer_info.phone
        
        # Email validation
        if Customer.object.filter(email=email).exists():
            raise Exception(f'{email} already exists')
        
        # Phone number validation 
        if phone and re.match(r'^\+?\d{10, 15}\d{3}-\d{3}-d{4}$'):
            raise Exception(f'Invalid phone no. {name}: Input eg +123456789 or +123-456-7890')
        
        # Save to DB
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()

        created_customers.append(customer)

        return BulkCreateCustomers(ok=True, customer_list=created_customers)
    

class CreateProduct(graphene.Mutation):
    """ """
    ok = graphene.Boolean()
    name = graphene.String()
    price = graphene.Float()
    stock = graphene.Int()


    class Arguments:
        ok = graphene.Boolean()
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(required=False, default_value=0)
    
    def mutate(self, info, price, stock):
        if price >= 0 and stock > 0:
            return Exception('Price and stock must be positive')


class CreateOrder():
    pass


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
