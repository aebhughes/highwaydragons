#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015 Alexander Hughes
# All Rights Reserved.

from settings import COUCHUSER,COUCHPW
import couchdb
couch = couchdb.Server()
couch.resource.credentials = (COUCHUSER, COUCHPW)
db = couch['academy']
from uuid import uuid4
from collections import OrderedDict


QUESTIONS = [
             {
               'question': 'How many BDMs does it take to change a light bulb?',
               'slug': 'how-many-bdms-does-it-take-to-change-a-light-bulb',
               'answers': [
                       ['None. That is the Franchisees job', True],
                       ['One, to tell the BP to do it', False],
                       ['All of them.  To create a policy document', False],
                       ['Two. One to load the policy document on the system and one '
                          'to tell the BP about it', False]
                     ],
             },
              {
               'question': 'How many BPs does it take to change a light bulb?',
               'slug': 'how-many-bps-does-it-take-to-change-a-light-bulb',
               'answers': [ 
                           ['None. They never notice they have to', True],
                           ['None. They seem to think that is Centre Managements job', False],
                           ['One, to get a staff member to do it', False],
                           ],
              }
       ]

DESIGN_DOCS = [
                {
                   '_id': '_design/store',
                   'language': 'javascript',
                   'views': {
                       'all': {
                           'map': 'function(doc) {\n  if (doc.type == "store") {\n  emit(doc.name, doc);}\n}'
                       }
                   }
                },
                {
                   '_id': '_design/admin',
                   'language': 'javascript',
                   'views': {
                       'all': {
                           'map': 'function(doc) {\n  if (doc.type == "admin") {\n  emit(doc.username, doc);}\n}'
                       }
                   }
                },
                {
                   '_id': '_design/course',
                   'language': 'javascript',
                   'views': {
                       'all': {
                           'map': 'function(doc) {\n  if (doc.type == "course") {\n  emit(doc.url, doc);}\n}'
                       },
                       'rank': {
                           'map': 'function(doc) {\n  if (doc.type == "course") {\n  emit([doc.rank,doc.url], doc);}\n}'
                       }
                   }
                },
                {
                   '_id': '_design/student',
                   'language': 'javascript',
                   'views': {
                       'all': {
                           'map': 'function(doc) {\n  if (doc.type == "student") {\n    emit(doc.name, doc);}\n}'
                       },
                       'store_id': {
                           'map': 'function(doc) {\n  if (doc.type == "student") {\n    emit(doc.store_id, doc);}\n}'
                       }
                   }
                }
]

STORES = [
            {
             '_id': uuid4().hex,
             'name': 'Demo Store',
             'username': 'demo@postnet.co.za',
             'password': 'password',
             'maint_user': 'demo@postnet.co.za',
             'maint_pw': 'password',
             'type': 'store',
            },
            {
             '_id': uuid4().hex,
             'name': 'Head Office',
             'username': 'headoffice@postnet.co.za',
             'password': 'password',
             'maint_user': 'headoffice@postnet.co.za',
             'maint_pw': 'password',
             'type': 'store',
            }
]

ADMINS = [
            {
             '_id': uuid4().hex,
             'name': 'Alex Hughes',
             'username': 'alex@postnet.co.za',
             'password': 'password',
             'type': 'admin',
            },
            {
             '_id': uuid4().hex,
             'name': 'Pieter Strydom',
             'username': 'pieters@postnet.co.za',
             'password': 'password',
             'type': 'admin',
            },
            {
             '_id': uuid4().hex,
             'name': 'Graeme Sanders',
             'username': 'graeme@postnet.co.za',
             'password': 'password',
             'type': 'admin',
            }
]

STUDENTS = [
            {
            'store_id': '',
            'name': 'Fred Bloggs',
            'progress': {},
            'password': 'password',
            'type': 'student',
            },
            {
            'store_id': '',
            'name': 'Jim Fish',
            'progress': {},
            'password': 'password',
            'type': 'student'
            },
            {
            'store_id': '',
            'name': 'Jane Smith',
            'progress': {},
            'password': 'password',
            'type': 'student',
            },
            {
            'store_id': '',
            'name': 'Wendy Doe',
            'progress': {},
            'password': 'password',
            'type': 'student',
            }
]

COURSES = [
            {
             'url': 'induction',
             '_id': uuid4().hex,
             'rank': 0,
             'published': True,
             'name': 'PostNet Induction',
             'desc': 'PostNet Orientation is a '
                     '<strong>required<strong> module that ' 
                     'must be completed before any of the other '
                     'modules can be attempted.',
             'type': 'course',
             'image_url': 'induction.jpg',
             'modules': 
                     { 
                       'about-postNet':
                                       {
                                         'name': 'About PostNet',
                                         'desc': 'Marked up module desc',
                                         'video_url': 'Thunderstruck.mp4',
                                         'pdf_url': 'about_postnet.pdf',
                                         'questions': QUESTIONS,
                                       },
                       'customer-service':
                                       {
                                         'name': 'Customer Service',
                                         'desc': 'Marked up module desc',
                                         'desc': 'Marked up module desc',
                                         'video_url': 'Thunderstruck.mp4',
                                         'pdf_url': 'about_postnet.pdf',
                                         'questions': QUESTIONS,
                                        },
                       'up-cross-selling':
                                        {
                                         'name': 'Up and Cross-selling',
                                         'desc': 'Marked up module desc',
                                         'desc': 'Marked up module desc',
                                         'video_url': 'Thunderstruck.mp4',
                                         'pdf_url': 'about_postnet.pdf',
                                         'questions': QUESTIONS,
                                        },
                       'single-sign-on':
                                        {
                                         'name': 'Single Sign On',
                                         'desc': 'Marked up module desc',
                                         'video_url': 'Thunderstruck.mp4',
                                         'pdf_url': 'about_postnet.pdf',
                                         'questions': QUESTIONS,
                                        }
                     },
             },
            {
             'url': 'courier',
             '_id': uuid4().hex,
             'rank': 1,
             'published': True,
             'name': 'Courier',
             'desc': 'Marked-up text here',
             'type': 'course',
             'image_url': 'courier.jpg',
             'modules': 
                   {
                       'postnet-to-postnet':
                                       {
                                         'name': 'PostNet to PostNet',
                                         'desc': 'Marked up module desc',
                                         'video_url': '',
                                         'pdf_url': '',
                                         'questions': QUESTIONS,
                                       },
                       'postnet-to-door':
                                       {
                                         'name': 'PostNet to Door',
                                         'desc': 'Marked up module desc',
                                         'video_url': '',
                                         'pdf_url': '',
                                         'questions': QUESTIONS,
                                       },
                       'pge':
                                       {
                                         'name': 'PGE',
                                         'desc': 'Marked up module desc',
                                         'video_url': '',
                                         'pdf_url': '',
                                         'questions': QUESTIONS,
                                       },
                       'express-easy':
                                       {
                                         'name': 'Express Easy',
                                         'desc': 'Marked up module desc',
                                         'video_url': '',
                                         'pdf_url': '',
                                         'questions': QUESTIONS,
                                       },
                       'international-courier':
                                       {
                                         'name': 'International Courier',
                                         'desc': 'Marked up module desc',
                                         'video_url': '',
                                         'pdf_url': '',
                                         'questions': QUESTIONS,
                                       },
                       'dangerous-goods':
                                       {
                                         'name': 'Dangerous Goods',
                                         'desc': 'Marked up module desc',
                                         'video_url': '',
                                         'pdf_url': '',
                                         'questions': QUESTIONS,
                                       },
                       'global-mail':
                                       {
                                         'name': 'Global Mail',
                                         'desc': 'Marked up module desc',
                                         'video_url': '',
                                         'pdf_url': '',
                                         'questions': QUESTIONS,
                                       },
                       'excess-baggage':
                                       {
                                         'name': 'Excess Baggage',
                                         'desc': 'Marked up module desc',
                                         'video_url': '',
                                         'pdf_url': '',
                                         'questions': QUESTIONS,
                                       },
                       'pri':
                                       {
                                         'name': 'PRI',
                                         'desc': 'Marked up module desc',
                                         'video_url': '',
                                         'pdf_url': '',
                                         'questions': QUESTIONS,
                                       },
                       'rate-calculator':
                                       {
                                         'name': 'Rate Calculator',
                                         'desc': 'Marked up module desc',
                                         'video_url': '',
                                         'pdf_url': '',
                                         'questions': QUESTIONS,
                                       },
                       'parcel-tracking':
                                       {
                                         'name': 'Parcel Tracking',
                                         'desc': 'Marked up module desc',
                                         'video_url': '',
                                         'pdf_url': '',
                                         'questions': QUESTIONS,
                                       }
                   },
             },
            { 
             'url': 'copy-and-print', 
             '_id': uuid4().hex,
             'rank': 2,
                'published': True,
              'name': 'Copy and Print',
              'desc': 'Marked-up text here',
              'type': 'course',
              'image_url': 'copy_print.jpg',
              'modules': 
                    {
                       'easy-photo':
                                        {
                                          'name': 'Easy Photo',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        },
                      'smart-device-printing-hp':
                                        {
                                          'name': 'Smart Device Printing - HP',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        },
                      'binding-and-laminating':
                                        {
                                          'name': 'Binding and Laminating',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        },
                       'banners-and-flags':
                                        {
                                          'name': 'Banners and Flags',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        },
                       'litho-printing':
                                        {
                                          'name': 'Litho Printing',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        },
                       'design':
                                        {
                                          'name': 'Design',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        }
                    },
             },
            {
               'url': 'digital', 
             '_id': uuid4().hex,
               'rank': 3,
                'published': True,
               'name': 'Digital',
                'desc': 'Marked-up text here',
                'type': 'course',
                'image_url': 'digital.jpg',
                'modules': 
                      {
                       'scanning':
                                        {
                                          'name': 'Scanning',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        },
                       'js-cafe':
                                        {
                                          'name': 'JS Cafe',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        }
                      },
             },
            {
             'url': 'stationery', 
             '_id': uuid4().hex,
             'rank': 4,
                'published': True,
             'name': 'Stationery',
             'desc': 'Marked-up text here',
             'type': 'course',
             'image_url': 'stationery.jpg',
             'modules': 
                     {
                       'rubber-stamps':
                                        {
                                          'name': 'Rubber Stamps',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        },
                       'name-badges':
                                        {
                                          'name': 'Name Badges',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        }
                     },
              },
             {
              'url': 'mailboxes',
             '_id': uuid4().hex,
              'rank': 5,
                'published': True,
              'name': 'Mailboxes',
              'desc': 'Marked-up text here',
              'type': 'course',
              'image_url': 'mailboxes.jpg',
              'modules': 
                    {
                       'mailbox-manager':
                                        {
                                          'name': 'Mailbox Manager',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        }
                    }
               },
               {
               'url': 'marketing',
             '_id': uuid4().hex,
               'rank': 6,
                'published': True,
               'name': 'Marketing',
               'desc': 'Marked-up text here',
               'type': 'course',
               'image_url': 'marketing.jpg',
               'modules': 
                     {
                        'flyer-allowance':
                                        {
                                          'name': 'Flyer Allowance',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                          'pdf_url': '',
                                        },
                        'above-the-line-campaigns':
                                        {
                                          'name': 'Above the line Campaigns',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        },
                        'emailer-database':
                                        {
                                          'name': 'Emailer Database',
                                          'desc': 'Marked up module desc',
                                          'video_url': '',
                                          'pdf_url': '',
                                          'questions': QUESTIONS,
                                        }
                     },
               },
               {
               'url': 'pos',
             '_id': uuid4().hex,
               'rank': 7,
                'published': True,
               'name': 'Point of Sale',
               'desc': 'Marked-up text here',
               'type': 'course',
               'image_url': 'pos.jpg',
               'modules': 
                     {
                        'cash-sales':
                                         {
                                           'name': 'Cash Sales',
                                           'desc': 'Marked up module desc',
                                           'video_url': '',
                                           'pdf_url': '',
                                           'questions': QUESTIONS,
                                         },
                        'account-sales':
                                         {
                                           'name': 'Account Sales',
                                           'desc': 'Marked up module desc',
                                           'video_url': '',
                                           'pdf_url': '',
                                           'questions': QUESTIONS,
                                         },
                        'end-of-day-proceedures':
                                         {
                                           'name': 'End of Day Proceedures',
                                           'desc': 'Marked up module desc',
                                           'video_url': '',
                                           'pdf_url': '',
                                           'questions': QUESTIONS,
                                         },
                        'end-of-month-proceedures':
                                         {
                                           'name': 'End of Month Proceedures',
                                           'desc': 'Marked up module desc',
                                           'video_url': '',
                                           'pdf_url': '',
                                           'questions': QUESTIONS,
                                         },
                        'end-of-year-proceedures':
                                         {
                                           'name': 'End of Year Proceedures',
                                           'desc': 'Marked up module desc',
                                           'video_url': '',
                                           'pdf_url': '',
                                           'questions': QUESTIONS,
                                         },
                        'stock':
                                         {
                                           'name': 'Stock',
                                           'desc': 'Marked up module desc',
                                           'video_url': '',
                                           'pdf_url': '',
                                           'questions': QUESTIONS,
                                         },
                        'debtors':
                                         {
                                           'name': 'Debtors',
                                           'desc': 'Marked up module desc',
                                           'video_url': '',
                                           'pdf_url': '',
                                           'questions': QUESTIONS,
                                         }
                     },
               },
               {
                'url': 'store-locator',
                '_id': uuid4().hex,
                'rank': 8,
                'published': True,
                'name': 'Store Locator',
                'desc': 'Marked-up text here',
                'type': 'course',
                'image_url': 'store_locator.jpg',
                'modules': 
                    {
                        'overview':
                                         {
                                           'name': 'Overview',
                                           'desc': 'Marked up module desc',
                                           'video_url': '',
                                           'pdf_url': '',
                                           'questions': QUESTIONS,
                                         }
                    },
                }
        ]

def load_courses():
    for row in db.view('course/all'):
        doc = db[row.id]
        db.delete(doc)
        print(doc['url'], 'deleted')
    for doc in COURSES:
        doc_id, rev = db.save(doc)
        print(doc_id, doc['url'], 'added')

def load_students():
    for row in db.view('student/all'):
        doc = db[row.id]
        db.delete(doc)
        print(doc['name'], 'deleted')
    for doc in STUDENTS:
        doc_id, rev = db.save(doc)
        print(doc_id, doc['name'], 'added')

def load_stores():
    for row in db.view('store/all'):
        doc = db[row.id]
        db.delete(doc)
        print(doc['username'], 'deleted')
    for doc in STORES:
        doc_id, rev = db.save(doc)
        print(doc_id, doc['username'], 'added')

def load_admins():
    for row in db.view('admin/all'):
        doc = db[row.id]
        db.delete(doc)
        print(doc['username'], 'deleted')
    for doc in ADMINS:
        doc_id, rev = db.save(doc)
        print(doc_id, doc['username'], 'added')

def test_load():
    print('*** Admins ***')
    for row in db.view('admin/all'):
        print(row.key)
    print('*** Courses ***')
    for row in db.view('course/all'):
        print(row.key)
    print('*** Stores ***')
    for row in db.view('store/all'):
        print(row.key)
    print('*** Students ***')
    for row in db.view('student/all'):
        print(row.key)

def set_store_student():
    stores = []
    for row in db.view('store/all'):
        stores.append(row.id)
    print(stores)
    for ndx, row in enumerate(db.view('student/all')):
        doc = db[row.id]
        doc['store_id'] = stores[ndx % 2]
        db[doc.id] = doc
        print(ndx, row.key, stores[ndx % 2])

def set_student_progress():
    for row in db.view('student/all'):
        doc = db[row.id]
        progress = {}
        print(row.key, '****')
        for course in db.view('course/all'):
            print('   {}'.format(course.key))
            modules = course.value['modules']
            mods = {}
            for key in modules.keys():
                print('      {}'.format(key))
                mods[key] = 0
            progress[course.key] = mods
        doc['progress'] = progress
        db[doc.id] = doc
        print('Progress Dict:{}'.format(progress))

def load_all():
    load_courses()
    load_students()
    load_stores()
    load_admins()
    set_store_student()
    set_student_progress()

def stores_from_extract():
    import csv
    reader = csv.DictReader(open('stores.csv'))
    for row in reader:
        print(row)
 
def add_published():
    for row in db.view('course/all'):
        doc = db[row.id]
        doc['published'] = True
        db[doc.id] = doc
        print(row.id, doc['name'])

if __name__ == '__main__':
    add_published()
