#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 AEB Hughes
# All Rights Reserved.

import os
from uuid import uuid4

from couchdb import Server
couch = Server()
couch.resource.credentials = (os.environ['COUCHUSER'],os.environ['COUCHPW'])
db = couch['highwaydragons']

def clear_existing():
    pass

def load_club():
    pass

def load_members():
    MEMBERS = (
                {
                 'name': 'Jo Boes ',
                 'chapter': 'Durban',
                 'alias': 'Megafone',
                 'telephone': '+27 (0)72 648 5572',
                 'email': 'megafone@highwaydragonsmc.co.za'
                 },
                {
                 'name': 'Les Boes ',
                 'chapter': 'Durban',
                 'alias': 'Madhatter',
                 'email': 'madhatter@highwaydragonsmc.co.za'
                 },
                {
                 'name': 'Shane Rain Bird',
                 'chapter': 'Gauteng',
                 'alias': '',
                 'email': 'chief@highwaydragonsmc.co.za'
                 },
                {
                 'name': 'Hank Jacobs',
                 'chapter': 'United Arab Emirates',
                 'email': 'salty@highwaydragonsmc.co.za'
                 },
                {
                 'name': 'Andrew Byrne ',
                 'alias': 'Tubs',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Marijke Byrne',
                 'alias': 'Boks',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Andrew Bezuidenhout',
                 'alias': 'Wetwet',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Morne Van Deventer',
                 'alias': 'Monty',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Nicolette Hailstone',
                 'alias': 'Keys',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Sean Mckinlay',
                 'alias': 'Clockie',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Kasia Mckinlay',
                 'alias': 'Kats',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Tony Olsen',
                 'alias': 'Bulldog',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Shane Reed',
                 'alias': 'Whizz',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Hugh Gordon',
                 'alias': 'Spock',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Jaque Bester',
                 'alias': 'Sticks',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Wendy Pool',
                 'alias': 'Picaso',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Francios Oosthuizen',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Dalene Oosthuizen',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Eddie Sehmel',
                 'chapter': 'Durban',
                 },
                {
                 'name': 'Andrew Spark',
                 'alias': 'Prof',
                 'chapter': 'Honorary Member',
                 }
                ) 
    for m in MEMBERS:
        doc = { 
                '_id': uuid4().hex,
                'type': 'member'}
        for key in m.keys():
            doc[key] = m[key]
        doc_id, rev = db.save(doc)
        print(doc_id, doc['name'])

if __name__ == '__main__':
    clear_existing()
    load_members()
    print('Setup Complete')
